import os

from ..client import DeepflowClient


def _check_file_exists(file_path: str):
    abspath = os.path.abspath(file_path)
    return os.path.exists(abspath)


def _csv_to_jsonl(file_path: str):
    import csv
    import json

    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield json.dumps(row) + "\r\n"


def execute(
    client: DeepflowClient,
    *,
    dataset: str,
    file_path: str,
):
    from ..command import RequestUploadParam, CommitUploadParam
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

        upload_resp = client.send(RequestUploadParam(datasetName=dataset))
        if upload_resp["_status"] == 500:
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

    commit_resp = client.send(CommitUploadParam(uploadId=upload_id))
    if commit_resp["_status"] == 500:
        print(commit_resp, file=sys.stderr)
        exit(1)

    if commit_resp["error"]:
        print(f"Status=FAILED ({commit_resp['error']})")

        errors = commit_resp["validate"]["errors"]
        from prettytable import PrettyTable

        table = PrettyTable(["line", "column", "error"])
        for err in errors:
            table.add_row([err["line"], err["path"][1:], err["params"]])

        print(table)
    else:
        print("Status=SUCCESS")
        persist_result = commit_resp["persist"]["result"]
        print(persist_result)
