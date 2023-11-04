"""Functional testing framework for command line applications"""
import sys

import frysk.cli


def main():
    try:
        sys.exit(frysk.cli.main())
    except (BrokenPipeError, KeyboardInterrupt):
        sys.exit(2)


if __name__ == "__main__":
    main()
