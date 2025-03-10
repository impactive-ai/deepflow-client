import os

from ..client import DeepflowClient


def _check_file_exists(file_path: str):
    abspath = os.path.abspath(file_path)
    return os.path.exists(abspath)


def _csv_to_jsonl(file_path: str):
    import csv
    import json

    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield json.dumps(row) + "\r\n"


def _print_validation_error(errors: list[any]):
    from prettytable import PrettyTable

    table = PrettyTable(["line", "column", "error"])
    for err in errors:
        table.add_row([err["line"], err["path"][1:], err["params"]])

    print(table)


def execute(
    client: DeepflowClient,
    *,
    dataset: str,
    file_path: str,
):
    from ..command import (
        DatasetUpdateStartParam,
        DatasetUpdateValidateParam,
        DatasetUpdateCommitParam,
    )
    import sys

    abspath = os.path.abspath(file_path)

    print(f"Input filepath: {abspath}")

    # 파일 경로 유효성 확인
    if not _check_file_exists(file_path):
        print(f"File does not exist: {abspath}", file=sys.stderr)
        exit(1)

    import tempfile

    with tempfile.NamedTemporaryFile("w+", suffix=".jsonl", newline="\r\n") as tmp:
        tmp.writelines(_csv_to_jsonl(abspath))
        tmp.flush()

        upload_resp = client.send(
            DatasetUpdateStartParam(groupId=client.tenant_id, datasetName=dataset)
        )
        if upload_resp["_status"] == 500:
            print(upload_resp)
            print(f"Dataset does not exist: {dataset}", file=sys.stderr)
            exit(1)

        signed_url = upload_resp["signedUrl"]
        upload_id = upload_resp["uploadId"]

        tmp.seek(0)
        import requests

        put_resp = requests.put(
            signed_url, data=tmp, headers={"Content-Type": "application/octet-stream"}
        )
        put_resp.raise_for_status()

    validate_resp = client.send(DatasetUpdateValidateParam(uploadId=upload_id))
    if validate_resp["hasError"]:
        _print_validation_error(validate_resp["error"]["details"])
        exit(1)

    commit_resp = client.send(DatasetUpdateCommitParam(uploadId=upload_id))
    if commit_resp["_status"] == 500:
        print(commit_resp, file=sys.stderr)
        exit(1)

    if commit_resp["hasError"]:
        print(f"Unknown error: {commit_resp}", file=sys.stderr)
        exit(1)

    print(
        "RequestId={} Matched={} Updated={} Inserted={}".format(
            upload_id,
            commit_resp["matched"],
            commit_resp["updated"],
            commit_resp["inserted"],
        )
    )
