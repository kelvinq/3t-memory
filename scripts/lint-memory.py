#!/usr/bin/env python3
"""Lint the workspace memory system (generic / domain-neutral).

Checks:
  - canonical files and directories exist
  - core memory size policy (16KB target / 20KB warn / 24KB error)
  - core memory contains the generated-block markers
  - every project file has YAML frontmatter and required metadata
  - every project file has the expected narrative headings/lines
  - document paths referenced from project files resolve on disk
  - generated project index exists
  - date consistency between core 'Last updated' and project status lines

This script is domain-neutral: it does not assume any particular section names,
footer text, or business domain. Exit code is non-zero only on ERRORs.

Usage:
    python3 scripts/lint-memory.py
    python3 scripts/lint-memory.py --strict
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "memory" / "core.md"
AGENTS = ROOT / "AGENTS.md"
PROJECT_DIR = ROOT / "memory" / "projects"
ARCHIVE_DIR = PROJECT_DIR / "archive"
WATCHLIST = ROOT / "memory" / "watchlist.json"
PROJECT_INDEX = PROJECT_DIR / "README.md"

START_MARKER = "<!-- memory-sections:start -->"
END_MARKER = "<!-- memory-sections:end -->"

DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
LAST_UPDATED_RE = re.compile(r"\*\*Last updated:\*\*\s*(\d{4}-\d{2}-\d{2})")
STATUS_LINE_RE = re.compile(r"\*\*Status:\*\*\s*(\d{4}-\d{2}-\d{2})")
# Frontmatter field detection (covers both quoted and unquoted scalar values).
FM_FIELD_RE = {
    "status_date": re.compile(r"^status_date:\s*[\"']?(\d{4}-\d{2}-\d{2})[\"']?\s*$", re.I | re.M),
    "next_action": re.compile(r"^next_action:\s*[\"']?(.+?)[\"']?\s*$", re.I | re.M),
    "next_review_date": re.compile(r"^next_review_date:\s*[\"']?(\d{4}-\d{2}-\d{2})[\"']?\s*$", re.I | re.M),
    "core_section": re.compile(r"^core_section:\s*[\"']?(\S+?)[\"']?\s*$", re.I | re.M),
    "archive_status": re.compile(r"^archive_status:\s*[\"']?(\S+?)[\"']?\s*$", re.I | re.M),
}


@dataclass
class Finding:
    level: str
    message: str


findings: list[Finding] = []


def add(level: str, message: str) -> None:
    findings.append(Finding(level, message))


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


# --------------------------------------------------------------------------- #

def lint_canonical_files() -> None:
    if not AGENTS.exists():
        add("ERROR", "Missing canonical instruction file: AGENTS.md")
    if not CORE.exists():
        add("ERROR", "Missing canonical core memory file: memory/core.md")
    if not PROJECT_DIR.exists():
        add("ERROR", "Missing canonical project memory directory: memory/projects/")
    if not ARCHIVE_DIR.exists():
        add("WARN", "Missing memory/projects/archive/ directory")
    if not WATCHLIST.exists():
        add("WARN", "Missing watchlist source: memory/watchlist.json")
    if not PROJECT_INDEX.exists():
        add("WARN", "Missing generated project index: memory/projects/README.md")
    if not (ROOT / "memory" / "_sections.json").exists():
        add("ERROR", "Missing section schema: memory/_sections.json")


def lint_core_memory() -> str:
    text = read_text(CORE)
    if not text:
        return ""

    size = len(text.encode("utf-8"))
    if size > 24 * 1024:
        add("ERROR", f"memory/core.md exceeds 24KB hard stop ({size} bytes)")
    elif size > 20 * 1024:
        add("WARN", f"memory/core.md exceeds 20KB warning threshold ({size} bytes)")
    elif size > 16 * 1024:
        add("INFO", f"memory/core.md exceeds 16KB target but below warning ({size} bytes)")

    if START_MARKER not in text or END_MARKER not in text:
        add("ERROR", "memory/core.md is missing the generated-block markers")
    elif text.index(START_MARKER) > text.index(END_MARKER):
        add("ERROR", "memory/core.md generated-block markers are in the wrong order")

    return text


def lint_project_files(core_text: str) -> None:
    core_last_updated = None
    m = LAST_UPDATED_RE.search(core_text)
    if m:
        core_last_updated = m.group(1)

    for path in sorted(PROJECT_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        text = read_text(path)
        name = path.name

        if not text.startswith("---\n"):
            add("WARN", f"Project file has no YAML frontmatter: {name}")
        else:
            for field, pattern in FM_FIELD_RE.items():
                if not pattern.search(text):
                    add("WARN", f"Project frontmatter missing {field}: {name}")

        if LAST_UPDATED_RE.search(text) is None:
            add("WARN", f"Project file missing '**Last updated:** YYYY-MM-DD': {name}")
        if "**Status:**" not in text:
            add("WARN", f"Project file missing '**Status:**' line: {name}")
        if "## Open items" not in text:
            add("WARN", f"Project file missing '## Open items' section: {name}")
        if "## Key documents" not in text:
            add("WARN", f"Project file missing '## Key documents' section: {name}")

        # Date consistency: a project status date newer than core's last-updated
        # suggests the core index is stale.
        status_match = STATUS_LINE_RE.search(text)
        if status_match and core_last_updated:
            if status_match.group(1) > core_last_updated:
                add(
                    "WARN",
                    f"Project status date {status_match.group(1)} is newer than core "
                    f"Last updated {core_last_updated}: {name}",
                )

        # Resolve referenced document paths.
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("- `"):
                continue
            try:
                doc = line.split("`", 2)[1]
            except IndexError:
                continue
            # Only check repo-relative paths.
            if not (doc.startswith("materials/") or doc.startswith("memory/")):
                continue
            if not (ROOT / doc).exists():
                add("WARN", f"Referenced document path not found in {name}: {doc}")


def render(strict: bool) -> int:
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for finding in sorted(findings, key=lambda f: (order[f.level], f.message)):
        print(f"[{finding.level}] {finding.message}")

    errors = sum(1 for f in findings if f.level == "ERROR")
    warnings = sum(1 for f in findings if f.level == "WARN")
    infos = sum(1 for f in findings if f.level == "INFO")
    print(f"\nSummary: {errors} error(s), {warnings} warning(s), {infos} info item(s)")

    if errors:
        return 1
    if strict and warnings:
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint the memory workspace.")
    parser.add_argument("--strict", action="store_true", help="return non-zero on warnings")
    args = parser.parse_args()

    lint_canonical_files()
    core_text = lint_core_memory()
    if PROJECT_DIR.exists():
        lint_project_files(core_text)

    return render(args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
