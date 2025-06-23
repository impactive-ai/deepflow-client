def render_validation_error(errors: list[any]):
    from prettytable import PrettyTable

    table = PrettyTable(["FileId", "Position(Line:Col)", "Message"])
    table.align = "l"

    for err in errors:
        table.add_row([err["fileId"], err["pos"], err["msg"]])

    return table


def render_affected_partitions(partitions: list[any]):
    from prettytable import PrettyTable

    table = PrettyTable(["Partition key", "Data count"])

    for v in partitions:
        table.add_row([v["pkey"], v["count"]])

    return table
