#!/usr/bin/env python3

import argparse
import subprocess
import sys
from os import environ
from typing import List

from identify.identify import tags_from_path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("tool", help="Executable of the tool to run")
    parser.add_argument("types", nargs="+")
    return parser.parse_args()


def _git_all_files() -> List[str]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
        encoding="utf-8",
    )
    if not proc.stdout:
        return []
    return proc.stdout.strip("\0").split("\0")


def main():
    args = _parse_args()
    paths_matching_type = [
        p for p in _git_all_files() if any(t in args.types for t in tags_from_path(p))
    ]
    # suppress warning about pre-commit's virtualenv
    env = environ.copy()
    del env["VIRTUAL_ENV"]
    proc = subprocess.run(
        [
            "uv",
            "run",
            args.tool,
            *paths_matching_type,
        ],
        env=env,
    )
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
