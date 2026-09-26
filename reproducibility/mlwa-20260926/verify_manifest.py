#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the portable release manifest; --write is for release assembly only."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS.txt"
IGNORED_PARTS = {"__pycache__", ".git"}


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def files() -> dict[str, Path]:
    result = {}
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if path.is_symlink():
            raise ValueError(f"Symlinks are not release inputs: {relative.as_posix()}")
        if not path.is_file() or path == MANIFEST or IGNORED_PARTS.intersection(relative.parts):
            continue
        result[relative.as_posix()] = path
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Generate the manifest after final assembly.")
    args = parser.parse_args()
    actual = files()
    if args.write:
        MANIFEST.write_text("".join(f"{digest(actual[name])}  {name}\n" for name in sorted(actual)), encoding="utf-8")
        print(f"Manifest written: {len(actual)} files. Run again without --write to check.")
        return 0
    if not MANIFEST.is_file():
        print("HOLD: SHA256SUMS.txt is missing; release assembly is not finalized.")
        return 1
    expected = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        sha, name = line.split("  ", 1)
        safe_name = PurePosixPath(name)
        if len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha) or safe_name.is_absolute() or ".." in safe_name.parts or "\\" in name or ":" in name or name in expected:
            raise ValueError("Invalid or duplicate manifest entry")
        expected[name] = sha
    problems = [f"Missing: {name}" for name in sorted(expected.keys() - actual.keys())]
    problems += [f"Unexpected: {name}" for name in sorted(actual.keys() - expected.keys())]
    problems += [f"Hash mismatch: {name}" for name in sorted(actual.keys() & expected.keys()) if digest(actual[name]) != expected[name]]
    if problems:
        print("FAIL: release manifest mismatch")
        print("\n".join(problems))
        return 1
    print(f"PASS: {len(expected)}/{len(expected)} manifest hashes match; no unexpected files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
