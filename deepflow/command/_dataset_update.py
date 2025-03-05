from dataclasses import dataclass
from ._base_command import BaseCommand


@dataclass(frozen=True)
class DatasetUpdateStartParam(BaseCommand):
    _method = "POST"
    _action_path = "/dataset-update/start"

    groupId: str
    datasetName: str


@dataclass(frozen=True)
class DatasetUpdateValidateParam(BaseCommand):
    _method = "POST"
    _action_path = "/dataset-update/validate"

    uploadId: str


@dataclass(frozen=True)
class DatasetUpdateCommitParam(BaseCommand):
    _method = "POST"
    _action_path = "/dataset-update/commit"

    uploadId: str


__all__ = [
    "DatasetUpdateStartParam",
    "DatasetUpdateValidateParam",
    "DatasetUpdateCommitParam",
]
