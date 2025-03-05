from dataclasses import dataclass
from ._base_command import BaseCommand


@dataclass(frozen=True)
class GetDatasetListParam(BaseCommand):
    _method = "GET"
    _action_path = "/datasets"


@dataclass(frozen=True)
class GetDatasetSchemaParam(BaseCommand):
    _method = "GET"
    _action_path = "/datasets/{datasetName}/schema"
    _path_var_props = ["datasetName"]

    datasetName: str


__all__ = [
    "GetDatasetListParam",
    "GetDatasetSchemaParam",
]
