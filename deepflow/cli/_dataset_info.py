from ..client import DeepflowClient


def _print_info(datasets):
    from prettytable import PrettyTable

    table = PrettyTable(["Name", "Freq", "Partition", "Description"])
    for row in datasets:
        table.add_row([row["name"], row["freq"], row["partition"], row["description"]])

    print(table)


def _print_schema(json_schema):
    from prettytable import PrettyTable

    required_fields = set(json_schema["required"])
    props = json_schema["properties"]

    table = PrettyTable(["Column", "Required", "Type", "Format"])
    for col, type_spec in props.items():
        type_format = type_spec.get("format", "")

        if type_format == "date":
            type_format = "yyyy-MM-dd"

        table.add_row(
            [
                col,
                "*" if col in required_fields else "",
                type_spec.get("type", ""),
                type_format,
            ]
        )
    print(table)


def execute(client: DeepflowClient):
    from ..command import GetDatasetInfoParam
    import json

    command = GetDatasetInfoParam()

    resp = client.send(command)
    datasets = resp["datasets"]

    print("# Datasets")
    _print_info(datasets)

    print("\n# Schemas")
    for row in resp["datasets"]:
        json_schema = json.loads(row["jsonSchema"])
        name = row["name"]
        print(f"\n## {name}")
        _print_schema(json_schema)
