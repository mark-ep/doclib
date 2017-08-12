from doclib.version import __version__
from doclib.cli.create_parser import create_parser


name = "doclib"
desc = "Tool for managing and filing documents"

def main() -> None:
    global name, desc

    parser = create_parser(name, desc, __version__)
    args = parser.parse_args()

    if args.command_name and args.command_class:
        name = args.command_name
        command = args.command_class()

        command.execute(args)
