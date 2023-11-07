#!/usr/bin/python
"""
@Author  :  Lijiawei
@Date    :  2023/11/6 7:29 PM
@Desc    :  main line.
"""
import argparse
import os
import sys

from qatools import __description__
from qatools import __version__
from qatools.adb import decryption
from qatools.adb import get_adb_path
from qatools.adb import get_host_ip

adb = get_adb_path()


def main():
    parser = argparse.ArgumentParser(description=__description__)

    parser.add_argument(
        "-v", "--version", dest="version", action="store_true", help="show version"
    )
    subparsers = parser.add_subparsers(help="sub-command help")
    subparsers.add_parser("clear", help="clear app cache data).")
    subparsers.add_parser("adb", help="complete adb debugging capability.")
    subparsers.add_parser(
        "remote", help="open Android device remote debugging port(5555)."
    )
    subparsers.add_parser(
        "proxy", help=f"enable device global proxy({get_host_ip()}:8888)."
    )
    subparsers.add_parser("unproxy", help=f"disable device global proxy.")

    if len(sys.argv) == 1:
        # qa
        parser.print_help()
        sys.exit(0)
    elif len(sys.argv) == 2:
        # print help for sub-commands
        if sys.argv[1] in ["-v", "--version"]:
            # qa -v
            print(f"{__version__}")

        elif sys.argv[1] == "remote":
            # qa remote
            os.system(f"{adb} tcpip 5555")

        elif sys.argv[1] == "proxy":
            # qa proxy
            os.system(
                f'{adb} {decryption(b"c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5")} {get_host_ip()}:8888'
            )

        elif sys.argv[1] == "unproxy":
            # qa proxy
            os.system(
                f'{adb} {decryption(b"c2hlbGwgc2V0dGluZ3MgcHV0IGdsb2JhbCBodHRwX3Byb3h5IDow")}'
            )

        elif sys.argv[1] == "adb":
            # qa adb
            os.system(f"{adb}")

        elif sys.argv[1] in ["-h", "--help"]:
            # qa -h
            parser.print_help()
        else:
            parser.print_help()
        sys.exit(0)

    elif len(sys.argv) == 3:
        if sys.argv[1] == "clear":
            os.system(f"{adb} shell pm clear {sys.argv[2]}")
        sys.exit(0)

    elif sys.argv[1] == "adb":
        del sys.argv[0:2]
        args = " ".join([str(i) for i in sys.argv])
        os.system(f"{adb} {args}")
        sys.exit(0)

    args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)
