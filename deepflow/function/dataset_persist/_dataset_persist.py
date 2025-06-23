import os
import logging
from ...client import DeepflowClient

logger = logging.getLogger("dataset-persist")
logger.addHandler(logging.NullHandler())


def _check_file_exists(file_path: str):
    abspath = os.path.abspath(file_path)
    return os.path.exists(abspath)


def execute_dataset_persist(
    client: DeepflowClient, *, dataset: str, file_path: str, verbose: bool = True
):
    from ...command import (
        DatasetPersistOpenContext,
        DatasetPersistCommitAsync,
    )

    _, ext = os.path.splitext(file_path)
    abspath = os.path.abspath(file_path)

    if not (ext == ".jsonl" or ext == ".csv"):
        raise RuntimeError("지원하지 않는 확장자 입니다.")

    logger.info(f"Input filepath: {abspath}")

    # 파일 경로 유효성 확인
    if not _check_file_exists(file_path):
        raise RuntimeError(f"File does not exist: {abspath}")

    # [API] open-context
    upload_resp = client.send(
        DatasetPersistOpenContext(datasetName=dataset, extension=ext[1:])
    )
    if upload_resp["_status"] == 500:
        raise RuntimeError(f"Dataset does not exist: {dataset}")

    signed_url = upload_resp["uploadUrl"]
    context_id = upload_resp["contextId"]
    logger.info(f"Context ID: {context_id}")

    # Upload file
    with open(file_path, "rb") as f:
        import requests

        logger.info("Uploading file...")
        put_resp = requests.put(
            signed_url, data=f, headers={"Content-Type": "application/octet-stream"}
        )
        put_resp.raise_for_status()
        logger.info("Uploading file... DONE")

    # [API] commit-async
    commit_resp = client.send(DatasetPersistCommitAsync(contextId=context_id))
    if commit_resp["_status"] == 500:
        import json

        raise RuntimeError(f"Commit request error: {json.dumps(commit_resp)}")

    # [API] get-context-status
    from ._wait_process_done import wait_process_done

    last_status = wait_process_done(client, context_id, verbose=verbose)
    close_reason = last_status["closeReason"]
    logger.info(f"Close reason: {close_reason}")

    return last_status
