#!/usr/bin/env python
import os
import sys
from pathlib import Path


def main() -> None:
    # Garante que o Python enxergue a pasta backend no path
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.append(str(BASE_DIR))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
