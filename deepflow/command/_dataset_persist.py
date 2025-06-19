from dataclasses import dataclass
from ._base_command import BaseCommand

_DATASET_PERSIST_PREFIX = "/tenant/dataset-persist"


@dataclass(frozen=True)
class DatasetPersistOpenContext(BaseCommand):
    _method = "POST"
    _action_path = _DATASET_PERSIST_PREFIX + "/open-context"

    datasetName: str
    extension: str | None = None


@dataclass(frozen=True)
class DatasetPersistCommitAsync(BaseCommand):
    _method = "POST"
    _action_path = _DATASET_PERSIST_PREFIX + "/commit-async"

    contextId: str


@dataclass(frozen=True)
class DatasetPersistCancel(BaseCommand):
    _method = "POST"
    _action_path = _DATASET_PERSIST_PREFIX + "/cancel"

    contextId: str


@dataclass(frozen=True)
class DatasetPersistGetContextStatus(BaseCommand):
    _method = "POST"
    _action_path = _DATASET_PERSIST_PREFIX + "/get-context-status"

    contextId: str


__all__ = [
    "DatasetPersistOpenContext",
    "DatasetPersistCommitAsync",
    "DatasetPersistCancel",
    "DatasetPersistGetContextStatus",
]
