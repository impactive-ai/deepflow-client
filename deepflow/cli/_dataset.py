from ..client import DeepflowClient


def _print_info(datasets):
    from prettytable import PrettyTable

    table = PrettyTable(["Name", "Type", "Partition", "RefDate Column", "Description"])
    for row in datasets:
        table.add_row(
            [
                row["datasetName"],
                row["type"],
                row.get("partition", ""),
                row.get("refDateColumn", ""),
                row["description"],
            ]
        )

    print(table)


def _print_schema(column_specs):
    from prettytable import PrettyTable

    table = PrettyTable(["Column", "Type", "Nullable", "Format", "Description"])
    for c in column_specs:
        col = c.get("column")
        data_type = c.get("type", "")
        description = c.get("desc", "")
        is_nullable = c.get("nullable")
        data_format = ""

        if data_type == "DATE":
            data_format = "yyyy-MM-dd"

        table.add_row(
            [
                col,
                data_type,
                "Y" if is_nullable else "",
                data_format,
                description,
            ]
        )
    print(table)


def _print_partition(partition_info):
    from prettytable import PrettyTable

    table = PrettyTable(
        ["Partition Key", "Data count", "Replace count", "Last updated at"]
    )
    for c in partition_info:
        pkey = c.get("pkey")
        data_count = c.get("dataCount")
        replace_count = c.get("replaceCount")

        table.add_row([pkey, data_count, replace_count, ""])
    print(table)


def execute(client: DeepflowClient, *, dataset_name: str):
    if dataset_name == "":
        from ..command import DatasetGetList

        resp = client.send(DatasetGetList())
        datasets = resp["datasets"]

        print("# Datasets")
        _print_info(datasets)
    else:
        from ..command import DatasetGetInfo

        resp = client.send(DatasetGetInfo(datasetName=dataset_name))
        name = resp["datasetName"]

        print(f"# Dataset: {name}")
        print(f"## General info")
        _print_info([resp])

        print(f"## Schema")
        _print_schema(resp["columnSpecs"])

        print(f"## Partition info")
        _print_partition(resp["partitionDetails"])
