import argparse
import sys

from aiohttp_simple.utils.manual import ManualHelper


def main_shell():
    helper = ManualHelper()
    parser = argparse.ArgumentParser("options:")
    subparsers = parser.add_subparsers(title="command", help="支持的方法")
    parse_1 = subparsers.add_parser("init_config", )
    parse_1.add_argument("-p", default=None, help="path")
    parse_1.set_defaults(func=helper.init_config)
    parse_1 = subparsers.add_parser("example")
    parse_1.add_argument("-p", default=None, help="path")
    parse_1.set_defaults(func=helper.example)
    args = parser.parse_args()
    args.func(args.p)


if __name__ == "__main__":
    sys.exit(main_shell())
