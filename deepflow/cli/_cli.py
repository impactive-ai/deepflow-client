import sys


def cli():
    from ._build_argparse import build_argparse

    parser = build_argparse()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(1)

    from ..client import DeepflowClient

    client = DeepflowClient(api_key=args.api_key)

    param = dict(**vars(args))
    del param["command"]
    del param["api_key"]

    if args.command == "dataset":
        from ._dataset import execute

        execute(client, **param)
    elif args.command == "dataset-persist":
        from ._dataset_persist import execute

        execute(client, **param)
    elif args.command == "dataset-update":
        print(
            "데이터셋 저장 커맨드가 변경되었습니다. dataset-persist 를 사용하십시오.",
            file=sys.stderr,
        )
        exit(1)
    else:
        print("Unknown command", file=sys.stderr)
        exit(1)
