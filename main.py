#!/usr/bin/env python3
"""Entry program for the make.fun competition "news-image-20261119".

Copies the pre-drawn entry.png (bundled in this repo) to the output
directory requested by the grader. Python 3 standard library only.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        sys.stderr.write("entry.png not found next to main.py\n")
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
