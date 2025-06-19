import os

from ..client import DeepflowClient


def _check_file_exists(file_path: str):
    abspath = os.path.abspath(file_path)
    return os.path.exists(abspath)


def _print_validation_error(errors: list[any]):
    from prettytable import PrettyTable

    table = PrettyTable(["FileId", "Position(Line:Col)", "Message"])
    table.align = "l"

    for err in errors:
        table.add_row([err["fileId"], err["pos"], err["msg"]])

    print(table)


def _print_affected_partitions(partitions: list[any]):
    from prettytable import PrettyTable

    table = PrettyTable(["Partition key", "Data count"])

    for v in partitions:
        table.add_row([v["pkey"], v["count"]])

    print(table)


def execute(
    client: DeepflowClient,
    *,
    dataset: str,
    file_path: str,
):
    from ..command import (
        DatasetPersistOpenContext,
        DatasetPersistCommitAsync,
    )
    import sys

    _, ext = os.path.splitext(file_path)
    abspath = os.path.abspath(file_path)

    if not (ext == ".jsonl" or ext == ".csv"):
        print(f"지원하지 않는 확장자 입니다.", file=sys.stderr)
        exit(1)

    print(f"Input filepath: {abspath}")

    # 파일 경로 유효성 확인
    if not _check_file_exists(file_path):
        print(f"File does not exist: {abspath}", file=sys.stderr)
        exit(1)

    # [API] open-context
    upload_resp = client.send(
        DatasetPersistOpenContext(datasetName=dataset, extension=ext[1:])
    )
    if upload_resp["_status"] == 500:
        print(upload_resp)
        print(f"Dataset does not exist: {dataset}", file=sys.stderr)
        exit(1)

    signed_url = upload_resp["uploadUrl"]
    context_id = upload_resp["contextId"]
    print(f"Context ID: {context_id}")

    # Upload file
    with open(file_path, "rb") as f:
        import requests

        print("Uploading file...")
        put_resp = requests.put(
            signed_url, data=f, headers={"Content-Type": "application/octet-stream"}
        )
        put_resp.raise_for_status()
        print("Uploading file... DONE")

    # [API] commit-async
    commit_resp = client.send(DatasetPersistCommitAsync(contextId=context_id))
    if commit_resp["_status"] == 500:
        print(commit_resp, file=sys.stderr)
        exit(1)

    # [API] get-context-status
    last_status = _wait_process_end(client, context_id)
    close_reason = last_status["closeReason"]
    print(f"Close reason: {close_reason}")

    if close_reason == "SUCCESS":
        affected_partitions = last_status["affectedPartitions"]
        if len(affected_partitions) > 0:
            print("\n# Affected partitions")
            _print_affected_partitions(affected_partitions)

    else:
        _print_validation_error(last_status["validation"]["errorDetails"])
        exit(1)


def _wait_process_end(
    client: DeepflowClient, context_id: str, polling_interval: float = 1
):
    from ..command import DatasetPersistGetContextStatus
    import time

    while True:
        resp = client.send(DatasetPersistGetContextStatus(context_id))

        status = resp["status"]
        validate_processed = resp["validation"]["processed"]
        validate_error = resp["validation"]["errorCount"]
        persist_stat = resp["persistence"]
        persist_processed = persist_stat["processed"]
        persist_skipped = persist_stat["skipped"]

        message = f"\r[{status:10}] Validating: {validate_processed} / Validation error: {validate_error} / Persisting: {persist_processed} / Skipped: {persist_skipped}"

        print(message, end="", flush=True)

        if status == "DONE":
            print()
            return resp

        time.sleep(polling_interval)
