#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import sys
from pathlib import Path

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent / "app"))
    from manage_backend import main

    main()
