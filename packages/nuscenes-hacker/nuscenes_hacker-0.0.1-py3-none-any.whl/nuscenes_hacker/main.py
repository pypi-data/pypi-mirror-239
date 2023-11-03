"""
Author: wind windzu1@gmail.com
Date: 2023-11-03 11:43:12
LastEditors: wind windzu1@gmail.com
LastEditTime: 2023-11-03 11:50:50
Description: 
Copyright (c) 2023 by windzu, All Rights Reserved. 
"""
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description="Nuscenes Hacker")
    subparsers = parser.add_subparsers(title="commands")

    # hack
    hack_parser = subparsers.add_parser("hack", help="hack mode")
    from .hack import main as hack_main

    hack_main.add_arguments(hack_parser)

    # restore
    restore_parser = subparsers.add_parser("restore", help="restore mode")
    from .restore import main as restore_main

    restore_main.add_arguments(restore_parser)

    args, unknown = parser.parse_known_args()

    if hasattr(args, "func"):
        args.func(args, unknown)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
