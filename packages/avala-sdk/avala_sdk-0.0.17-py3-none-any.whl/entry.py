import argparse
from avala.client import APIClient
from avala.utils import ConfigValidator

def main():
    parser = argparse.ArgumentParser(description='Avala Client SDK.')

    subparsers = parser.add_subparsers(title="Operations", dest="operation")

    import_parser = subparsers.add_parser("import", help="Import a dataset")

    import_parser.add_argument("--name", required=True, help="Name of dataset")
    import_parser.add_argument('--slug', default=None, help='Slug for the dataset')
    import_parser.add_argument('--visibility', default='public', help='Visibility of the dataset')
    import_parser.add_argument('--industry', default=0, type=int, help='Industry code')
    import_parser.add_argument('--license', default=0, type=int, help='License code')
    import_parser.add_argument('--citation', default="string", help='Citation for the dataset')
    import_parser.add_argument('--creator', default="string", help='Creator of the dataset')
    import_parser.add_argument('--description', default="string", help='Description of the dataset')

    license_parser = subparsers.add_parser("get-licenses", help="Get available licenses")
    industry_parser = subparsers.add_parser("get-industries", help="Get available industries")

    list_datasets_parser = subparsers.add_parser("get-datasets", help="List my datasets")
    list_projects_parser = subparsers.add_parser("get-projects", help="List my projects")

    annotations_parser = subparsers.add_parser("import-annotations", help="Import annotations of an existing dataset")
    annotations_parser.add_argument("--owner", required=False, help="Owner name (or login email of user) of dataset")
    annotations_parser.add_argument("--slug", required=False, help="Slug or small unique alias for dataset")
    annotations_parser.add_argument("--dataset-uid", required=True, help="Unique identifier for dataset")
    annotations_parser.add_argument("--annotations-file", required=True, help="The path to json file containing annotations in Coco format")
    annotations_parser.add_argument("--keep-annotations", required=False, default=False, help="Whether to keep any previous annotations for the project")
    annotations_parser.add_argument("--project-name", required=True, help="The Avala project to link these imported annotations to")

    list_exports_parser = subparsers.add_parser("get-exports", help="List my results")

    args = parser.parse_args()

    validator = ConfigValidator()
    if not validator.validate_config():
        print("Invalid config.json file. Please fix it")
        exit()

    client = APIClient(validator.get_config())

    if args.operation == "import":
        client.import_dataset(args)
    elif args.operation == "get-licenses":
        response = client.get_licenses()
        client.show(response)
    elif args.operation == "get-industries":
        response = client.get_industries()
        client.show(response)
    elif args.operation == "get-datasets":
        response = client.get_datasets()
        client.show(response)
    elif args.operation == "get-projects":
        response = client.get_projects()
        client.show(response)
    elif args.operation == "import-annotations":
        client.import_annotations(args)
    elif args.operation == "get-exports":
        response = client.get_exports()
        print(response)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

