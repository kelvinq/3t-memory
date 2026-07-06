#!/usr/bin/env python3
"""Run workspace hygiene checks.

This is the broader-brother of `lint-memory.py`. It catches what lint does not:

- `inbox/` items that are not yet tracked in `inbox/index.md`.
- `inbox/` items older than 7 days and `inbox/pending-user/` items older
  than 14 days (the "staleness policy"). Stale items are WARN by default
  and ERROR with `--strict`.
- Loose files at the workspace root that have not been routed.
- Trash archives whose 90-day (or configured) expiry has passed.

Usage:
    python3 scripts/workspace_check.py
    python3 scripts/workspace_check.py --skip-refresh
    python3 scripts/workspace_check.py --strict

Exit codes:
  0  no ERROR findings (WARN allowed unless --strict)
  1  at least one ERROR
  2  --strict and at least one WARN
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
PENDING = INBOX / "pending-user"
INBOX_INDEX = INBOX / "index.md"
DEFAULT_TRASH_ARCHIVE = Path.home() / ".3t-memory-trash"

ROOT_ALLOWED_FILES = {
    ".gitignore",
    "AGENTS.md",
    "OPERATOR.md",
    "QUICKSTART.md",
    "MIGRATING-FROM-CLAUDE-AND-CHATGPT.md",
    "README.md",
    "LICENSE",
    "Makefile",
    "reference",
    # The follow-up files outside the workspace's content directories that
    # the in-package workspace check defaults to allowing at the root:
    "prompts",
}
ROOT_ALLOWED_PREFIXES = ("tidy_", "HANDOFF-")
INBOX_CONTROL_FILES = {"README.md", "index.md", "intake-note.md"}
PENDING_CONTROL_FILES = {"README.md"}
INBOX_WARN_AGE_DAYS = 7
PENDING_WARN_AGE_DAYS = 14


@dataclass
class Finding:
    level: str
    message: str


findings: list[Finding] = []


def add(level: str, message: str) -> None:
    findings.append(Finding(level, message))


def run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(cmd)}", flush=True)
    return subprocess.run(cmd, cwd=ROOT).returncode


def file_age_days(path: Path) -> int:
    mtime = datetime.fromtimestamp(path.stat().st_mtime).date()
    return (date.today() - mtime).days


def scan_root_loose_files() -> None:
    """Look for top-level files that should probably live in `materials/`.

    Anything not in the explicit allowlist triggers a WARN. The allowlist
    is intentionally small; users with a richer root should add files to
    `ROOT_ALLOWED_FILES` in their fork.
    """
    loose: list[str] = []
    for path in sorted(ROOT.iterdir()):
        # Top-level *directories* are not loose files; they are part of
        # the structure. Only flag FILES and SYMLINKS to files.
        if not (path.is_file() or path.is_symlink()):
            continue
        name = path.name
        if name in ROOT_ALLOWED_FILES:
            continue
        if any(name.startswith(prefix) for prefix in ROOT_ALLOWED_PREFIXES):
            continue
        loose.append(name)

    if loose:
        add("WARN", "Loose root files need routing: " + ", ".join(loose))
    else:
        add("INFO", "No unexpected loose files at workspace root")


def parse_index_paths() -> set[str]:
    """Find the path-bearing column in `inbox/index.md` by header, not position.

    Different users keep different column orders. The first row in a
    Markdown table whose cells start with `|` is the header row. We pick
    the column whose header matches one of the known path-column names
    (`current path`, `path`, `file`) and use that column's data rows
    to populate the tracked-paths set.
    """
    if not INBOX_INDEX.exists():
        add("WARN", "Missing inbox/index.md")
        return set()
    paths: set[str] = set()
    PATH_HEADERS = {"current path", "path", "file"}

    rows = [line for line in INBOX_INDEX.read_text(encoding="utf-8").splitlines()
            if line.startswith("|") and "---" not in line]

    # Header row: first row that is not a separator.
    header: list[str] = []
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if all(c.replace(":", "").replace("-", "").strip() == "" for c in cells):
            continue
        if not header:
            header = [c.lower() for c in cells]
            break

    if not header:
        return paths

    path_idx: int | None = next(
        (i for i, h in enumerate(header) if h.strip() in PATH_HEADERS),
        None,
    )
    if path_idx is None:
        # No recognisable path column. Empty set is the safer default —
        # the script will then WARN on every inbox item not tracked,
        # which forces the operator to add the column header.
        return paths

    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if not cells:
            continue
        if all(c.replace(":", "").replace("-", "").strip() == "" for c in cells):
            continue
        if len(cells) <= path_idx:
            continue
        if cells[path_idx]:
            paths.add(cells[path_idx].strip("`").strip())
    return paths


def scan_inbox(strict: bool) -> None:
    """Walk inbox/ and inbox/pending-user/ for missing index entries and stale items."""
    if not INBOX.exists():
        add("INFO", "No inbox/ folder present")
        return

    indexed_paths = parse_index_paths()
    active_paths: list[Path] = []

    for path in sorted(INBOX.iterdir()):
        if path.name in INBOX_CONTROL_FILES or path.name == "pending-user":
            continue
        if path.is_file():
            active_paths.append(path)
            rel = path.relative_to(ROOT).as_posix()
            if rel not in indexed_paths:
                add("WARN", f"Inbox item not tracked in inbox/index.md: {rel}")
            age = file_age_days(path)
            if age > INBOX_WARN_AGE_DAYS:
                level = "ERROR" if strict else "WARN"
                add(level, f"Inbox item older than {INBOX_WARN_AGE_DAYS} days: {rel} ({age} days)")

    if PENDING.exists():
        for path in sorted(PENDING.iterdir()):
            if path.name in PENDING_CONTROL_FILES:
                continue
            if path.is_file():
                active_paths.append(path)
                rel = path.relative_to(ROOT).as_posix()
                if rel not in indexed_paths:
                    add("WARN", f"Pending-user item not tracked in inbox/index.md: {rel}")
                age = file_age_days(path)
                if age > PENDING_WARN_AGE_DAYS:
                    level = "ERROR" if strict else "WARN"
                    add(level, f"Pending-user item older than {PENDING_WARN_AGE_DAYS} days: {rel} ({age} days)")

    if not active_paths:
        add("INFO", "Inbox queue is empty")


def scan_trash_archive() -> None:
    """Warn about archived trash zips that are past their expiry date.

    Expiry is read from each JSON manifest next to the zip; the warning
    is exact rather than based on mtime. This is a warning only -
    nothing is auto-deleted. 90 days is the default expiry recorded by
    `scripts/trash_archive.py`; users with custom `--keep-days` will
    have different thresholds.
    """
    trash_archive_root = Path(os.environ.get(
        "THREET_MEMORY_TRASH_ARCHIVE", str(DEFAULT_TRASH_ARCHIVE)))
    if not trash_archive_root.exists():
        return

    manifests = sorted(trash_archive_root.glob("trash-*.manifest.json"))
    if not manifests:
        return

    today = date.today()
    for manifest in manifests:
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            add("WARN", f"Unreadable trash-archive manifest: {manifest}")
            continue
        try:
            expiry = date.fromisoformat(data["expiry_date"])
        except (KeyError, ValueError):
            add("WARN", f"Trash-archive manifest missing/invalid expiry_date: {manifest}")
            continue
        days_left = (expiry - today).days
        zip_name = data.get("zip", manifest.stem)
        zip_full = trash_archive_root / zip_name
        if days_left < 0:
            add(
                "WARN",
                f"Trash archive EXPIRED {-days_left}d ago: {zip_full} "
                f"(review and delete with: rm {zip_full} {manifest})",
            )
        elif days_left <= 14:
            add("WARN", f"Trash archive expiring in {days_left}d: {zip_full}")


def render(strict: bool, command_rc: int) -> int:
    print("\nWorkspace check findings:")
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for finding in sorted(findings, key=lambda f: (order.get(f.level, 9), f.message)):
        print(f"[{finding.level}] {finding.message}")

    errors = sum(1 for f in findings if f.level == "ERROR")
    warnings = sum(1 for f in findings if f.level == "WARN")
    infos = sum(1 for f in findings if f.level == "INFO")
    print(f"\nWorkspace check summary: {errors} error(s), {warnings} warning(s), {infos} info item(s)")

    if command_rc:
        return command_rc
    if errors:
        return 1
    if strict and warnings:
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-refresh", action="store_true",
                        help="Skip running scripts/memory_refresh.py first.")
    parser.add_argument("--strict", action="store_true",
                        help="Pass --strict to memory lint; promote stale-inbox WARN to ERROR.")
    args = parser.parse_args()

    rc = 0
    if not args.skip_refresh:
        cmd = [sys.executable, "scripts/memory_refresh.py"]
        if args.strict:
            cmd.append("--strict")
        rc = run(cmd)

    scan_inbox(args.strict)
    scan_root_loose_files()
    scan_trash_archive()
    return render(args.strict, rc)


if __name__ == "__main__":
    raise SystemExit(main())
