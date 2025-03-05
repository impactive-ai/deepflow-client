import sys


def _date_type(s):
    from datetime import date

    try:
        return date.fromisoformat(s)
    except ValueError:
        print("날짜 타입은 yyyy-MM-dd 형태여야 합니다.", file=sys.stderr)
        sys.exit(1)


def dataset_info(sub_parser):
    sub_parser.add_parser("dataset-info")


def dataset_update(sub_parser):
    parser = sub_parser.add_parser("dataset-update")
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
    )
    parser.add_argument("--input", "-i", type=str, required=True, dest="file_path")


def build_argparse():
    import argparse
    from ..util import EnvDefault

    parser = argparse.ArgumentParser(prog="deepflow", description="Deepflow API Client")
    parser.add_argument(
        "--tenant-id",
        type=str,
        action=EnvDefault,
        envvar="DEEPFLOW_TENANT_ID",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        action=EnvDefault,
        envvar="DEEPFLOW_API_KEY",
    )

    sub_parsers = parser.add_subparsers(dest="command")
    dataset_info(sub_parsers)
    dataset_update(sub_parsers)

    return parser
