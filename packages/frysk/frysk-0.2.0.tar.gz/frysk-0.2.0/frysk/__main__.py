"""Main module (invoked by "python3 -m frysk")"""
import sys

import frysk.cli

try:
    sys.exit(frysk.cli.main())
except (BrokenPipeError, KeyboardInterrupt):
    sys.exit(2)
