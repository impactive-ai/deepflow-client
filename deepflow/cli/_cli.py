def cli():
    from ._build_argparse import build_argparse

    parser = build_argparse()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(1)

    from ..client import DeepflowClient

    client = DeepflowClient(api_key=args.api_key, tenant_id=args.tenant_id)

    if args.command == "dataset-info":
        from ._dataset_info import execute

        execute(client)
