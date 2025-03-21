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

    table = PrettyTable(["Column", "Type", "Nullable", "Format", "Description"])
    for col, type_spec in props.items():
        type_format = type_spec.get("format", "")
        description = type_spec.get("description", "")
        types = type_spec.get("type", "")
        nullable = "null" in types
        if isinstance(types, list):
            types.remove("null")

        if type_format == "date":
            type_format = "yyyy-MM-dd"

        table.add_row(
            [
                col,
                types if isinstance(types, str) else ",".join(types),
                "Y" if nullable else "",
                type_format,
                description,
            ]
        )
    print(table)


def execute(client: DeepflowClient):
    from ..command import GetDatasetListParam
    import json

    command = GetDatasetListParam()

    resp = client.send(command)
    datasets = resp["datasets"]

    print("# Datasets")
    _print_info(datasets)

    print("\n# Schemas")
    for row in resp["datasets"]:
        json_schema = row["jsonSchema"]
        name = row["name"]
        print(f"\n## {name}")
        _print_schema(json_schema)
