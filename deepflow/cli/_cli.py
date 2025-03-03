import sys


def cli():
    from ._build_argparse import build_argparse

    parser = build_argparse()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(1)

    from ..client import DeepflowClient

    client = DeepflowClient(api_key=args.api_key, tenant_id=args.tenant_id)

    param = dict(**vars(args))
    del param["command"]
    del param["api_key"]
    del param["tenant_id"]

    if args.command == "dataset-info":
        from ._dataset_info import execute

        execute(client)
    elif args.command == "dataset-update":
        from ._dataset_update import execute

        execute(client, **param)
    else:
        print("Unknown command", file=sys.stderr)
        exit(1)
