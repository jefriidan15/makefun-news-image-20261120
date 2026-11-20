#!/usr/bin/env python3
"""news-image-20261120 entry: copy the bundled front page to the output dir.

The image (entry.png, 1024x1024) is a newspaper front page summing up the
world news of Friday 20 November 2026. This program only copies it, so both
grader runs write byte-identical output. Standard library only, no network.
"""
import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    with open(SOURCE, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_MAGIC):
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(data) > 1048576:
        print("entry.png exceeds the 1 MiB limit", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(dest, "wb") as fh:
        fh.write(data)
    with open(dest, "rb") as fh:
        written = fh.read()
    if written != data or hashlib.sha256(written).hexdigest() != digest:
        print("read-back verification failed", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)" % (dest, len(data), digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
