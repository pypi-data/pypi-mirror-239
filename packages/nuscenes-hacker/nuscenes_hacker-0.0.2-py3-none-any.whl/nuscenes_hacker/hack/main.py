"""
Author: wind windzu1@gmail.com
Date: 2023-11-03 14:25:39
LastEditors: wind windzu1@gmail.com
LastEditTime: 2023-11-03 14:34:33
Description: 
Copyright (c) 2023 by windzu, All Rights Reserved. 
"""

import os
from argparse import ArgumentParser

from .hack import Hack


def add_arguments(parser):
    parser.add_argument(
        "--config",
        type=str,
        help="Path to the configuration file",
    )

    # do something
    parser.set_defaults(func=main)


def main(args, unknown_args):
    config_path = args.config

    # check config_path if exists
    if not os.path.exists(config_path):
        print("config_path not exists")
        return

    hack = Hack(config_path)
    hack.hack()
