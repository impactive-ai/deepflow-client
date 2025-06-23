import sys

from ..client import DeepflowClient


def execute(
    client: DeepflowClient,
    *,
    dataset: str,
    file_path: str,
):
    from deepflow.function.dataset_persist import execute_dataset_persist
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.StreamHandler()],
    )

    try:
        last_status = execute_dataset_persist(
            client, dataset=dataset, file_path=file_path
        )
        close_reason = last_status["closeReason"]

        if close_reason == "SUCCESS":
            affected_partitions = last_status["affectedPartitions"]
            if len(affected_partitions) > 0:
                from ..function.dataset_persist import render_affected_partitions

                print("\n# Affected partitions")
                print(render_affected_partitions(affected_partitions))
        else:
            from ..function.dataset_persist import render_validation_error

            print(render_validation_error(last_status["validation"]["errorDetails"]))
            raise RuntimeError("Validation Error")
    except RuntimeError as e:
        print(e, file=sys.stderr)
        exit(1)
