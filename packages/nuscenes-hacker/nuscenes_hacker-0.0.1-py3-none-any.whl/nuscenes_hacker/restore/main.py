"""
Author: wind windzu1@gmail.com
Date: 2023-11-03 11:51:33
LastEditors: wind windzu1@gmail.com
LastEditTime: 2023-11-03 13:48:44
Description: reinstall nuscenes-devkit
Copyright (c) 2023 by windzu, All Rights Reserved. 
"""


import shutil
import subprocess
import sys


def add_arguments(parser):
    parser.set_defaults(func=main)


def main(args, unknown_args):
    # use pip or pip3 reinstall nuscenes-devkit

    pip_path = shutil.which("pip")
    pip3_path = shutil.which("pip3")

    if pip_path is not None:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--force-reinstall",
                "nuscenes-devkit",
            ]
        )
    elif pip3_path is not None:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip3",
                "install",
                "--force-reinstall",
                "nuscenes-devkit",
            ]
        )
    else:
        print("pip3 not exists")
        return
