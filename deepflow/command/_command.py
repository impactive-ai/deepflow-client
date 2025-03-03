from dataclasses import dataclass
from ._base_command import BaseCommand


@dataclass(frozen=True)
class RequestUploadParam(BaseCommand):
    _method = "POST"
    _action_path = "/request-upload"

    datasetName: str


@dataclass(frozen=True)
class CommitUploadParam(BaseCommand):
    _method = "POST"
    _action_path = "/commit-upload"

    uploadId: str


@dataclass(frozen=True)
class GetDatasetInfoParam(BaseCommand):
    _method = "GET"
    _action_path = "/dataset-info"


__all__ = ["RequestUploadParam", "CommitUploadParam", "GetDatasetInfoParam"]
