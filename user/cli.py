import sys
import argparse
import config
from engine import Engine

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode")
    subparsers.add_parser("execute", help="Read entire stdin as input script")
    view_parser = subparsers.add_parser("view", help="View items by ID")
    view_parser.add_argument("--id", required=True)
    view_parser.add_argument("items", nargs="+")
    args = parser.parse_args()
    if args.mode is None:
        parser.print_help()
        sys.exit()
    
    engine = Engine(config.SERIES_DATA_PATH, config.OUTPUT_ROOT_PATH)
    if args.mode == "execute":
        script = sys.stdin.read()
        try:
            output_id = engine.run_engine(script)
        except (ValueError, KeyError) as _:
            sys.exit("Invalid Script")
        print("Script sucessfully executed:", output_id)
    else:
        try:
            res = engine.view(args.id, args.items)
        except (FileNotFoundError, KeyError):
            sys.exit("Invalid Input")

        for name, vals in res.items():
            print(name + ":")
            print(vals)
            print()



if __name__ == "__main__":
    main()