import sys


def _date_type(s):
    from datetime import date

    try:
        return date.fromisoformat(s)
    except ValueError:
        print("날짜 타입은 yyyy-MM-dd 형태여야 합니다.", file=sys.stderr)
        sys.exit(1)


def dataset(sub_parser):
    parser = sub_parser.add_parser("dataset")
    parser.description = "데이터셋 목록 및 상세 정보를 조회합니다."
    parser.add_argument("dataset_name", nargs="?", type=str, default="")


def dataset_persist(sub_parser):
    parser = sub_parser.add_parser("dataset-persist")
    parser.description = "데이터를 전송 합니다."
    parser.add_argument(
        "dataset",
        type=str,
    )
    parser.add_argument("--input", "-i", type=str, required=True, dest="file_path")


def dataset_update(sub_parser):
    parser = sub_parser.add_parser("dataset-update")


def build_argparse():
    import argparse
    from ..util import EnvDefault
    from ..version import VERSION

    parser = argparse.ArgumentParser(prog="deepflow", description="Deepflow API Client")
    parser.add_argument("--version", action="version", version=f"deepflow {VERSION}")

    parser.add_argument(
        "--api-key",
        type=str,
        action=EnvDefault,
        envvar="DEEPFLOW_API_KEY",
    )

    sub_parsers = parser.add_subparsers(dest="command")
    dataset(sub_parsers)
    dataset_persist(sub_parsers)
    dataset_update(sub_parsers)

    return parser
