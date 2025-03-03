import os

from ..client import DeepflowClient


def _check_file_exists(file_path: str):
    if not os.path.exists(file_path):
        raise RuntimeError(f"File does not exist: {file_path}")


def _put_file(put_url: str, file_path: str):
    import requests

    with open(file_path, "r") as f:
        put_resp = requests.put(
            put_url, data=f, headers={"Content-Type": "application/octet-stream"}
        )

    put_resp.raise_for_status()


def execute(
    client: DeepflowClient,
    *,
    dataset: str,
    file_path: str,
):
    from ..command import RequestUploadParam

    # 파일 경로 유효성 확인
    _check_file_exists(file_path)

    upload_resp = client.send(RequestUploadParam(datasetName=dataset))

    signed_url = upload_resp["signedUrl"]
    upload_id = upload_resp["uploadId"]
    print(upload_id, signed_url)

    # _put_file(signed_url, file_path)
