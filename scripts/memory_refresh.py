#!/usr/bin/env python3
"""Run memory rebuild then lint as a single maintenance command (generic).

Resolves sibling scripts relative to this file's location, so the same script
works whether it lives at the package root or inside an `example/` workspace.

Usage:
    python3 scripts/memory_refresh.py
    python3 scripts/memory_refresh.py --date 2026-05-16
    python3 scripts/memory_refresh.py --strict
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = SCRIPTS_DIR.parent


def run(cmd: list[str]) -> int:
    return subprocess.run(cmd, cwd=ROOT).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild generated memory views then lint.")
    parser.add_argument("--date", help="Date to stamp into memory/core.md during rebuild")
    parser.add_argument("--strict", action="store_true", help="Pass --strict to lint-memory.py")
    args = parser.parse_args()

    rebuild_cmd = [sys.executable, str(SCRIPTS_DIR / "rebuild-memory-core.py")]
    if args.date:
        rebuild_cmd.extend(["--date", args.date])

    lint_cmd = [sys.executable, str(SCRIPTS_DIR / "lint-memory.py")]
    if args.strict:
        lint_cmd.append("--strict")

    rc = run(rebuild_cmd)
    if rc != 0:
        return rc

    rc = run(lint_cmd)
    if rc == 0:
        print("Memory refresh complete.")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
