from ...client import DeepflowClient


def wait_process_done(
    client: DeepflowClient,
    context_id: str,
    polling_interval: float = 1,
    verbose: bool = False,
):
    from ...command import DatasetPersistGetContextStatus
    import time

    while True:
        resp = client.send(DatasetPersistGetContextStatus(context_id))

        status = resp["status"]
        validate_processed = resp["validation"]["processed"]
        validate_error = resp["validation"]["errorCount"]
        persist_stat = resp["persistence"]
        persist_processed = persist_stat["processed"]
        persist_skipped = persist_stat["skipped"]

        if verbose:
            message = f"\r[{status:10}] Validating: {validate_processed} / Validation error: {validate_error} / Persisting: {persist_processed} / Skipped: {persist_skipped}"
            print(message, end="", flush=True)

        if status == "DONE":
            if verbose:
                print()

            return resp

        time.sleep(polling_interval)
