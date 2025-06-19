from dataclasses import dataclass
from ._base_command import BaseCommand

_DATASET_PERSIST_PREFIX = "/tenant/datasets"


@dataclass(frozen=True)
class DatasetGetList(BaseCommand):
    _method = "GET"
    _action_path = _DATASET_PERSIST_PREFIX


@dataclass(frozen=True)
class DatasetGetInfo(BaseCommand):
    _method = "POST"
    _action_path = _DATASET_PERSIST_PREFIX + "/get-info"

    datasetName: str


__all__ = [
    "DatasetGetList",
    "DatasetGetInfo",
]
