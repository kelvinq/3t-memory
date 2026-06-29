#!/usr/bin/env python3
"""Rebuild generated memory views from structured sources (generic / domain-neutral).

This script is config-driven. It does NOT hardcode any section names, column
layouts, footer text, or dates. Everything rendered comes from:

  - project frontmatter in `memory/projects/*.md`
  - `memory/watchlist.json`
  - the section schema in `memory/_sections.json`

Outputs:
  - memory/core.md           : generated section tables injected between markers
  - memory/projects/README.md: generated project index

The generated block in `memory/core.md` is delimited by:
    <!-- memory-sections:start -->
    ... generated content ...
    <!-- memory-sections:end -->

Everything between those markers is fully replaced on each run, so the file is
idempotent: running twice produces an identical file (within the same calendar
day, because the `**Last updated:**` line is stamped with today's date).

Usage:
    python3 scripts/rebuild-memory-core.py
    python3 scripts/rebuild-memory-core.py --date 2026-05-16
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CORE = ROOT / "memory" / "core.md"
PROJECT_DIR = ROOT / "memory" / "projects"
ARCHIVE_DIR = PROJECT_DIR / "archive"
WATCHLIST = ROOT / "memory" / "watchlist.json"
SECTIONS_SCHEMA = ROOT / "memory" / "_sections.json"
PROJECT_INDEX = PROJECT_DIR / "README.md"

START_MARKER = "<!-- memory-sections:start -->"
END_MARKER = "<!-- memory-sections:end -->"


# --------------------------------------------------------------------------- #
# Parsing helpers
# --------------------------------------------------------------------------- #

def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_frontmatter(path: Path) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None
    fm = parts[0]
    data: dict[str, Any] = {}
    for line in fm.splitlines()[1:]:
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = parse_scalar(value)
    return data


def load_schema() -> dict[str, Any]:
    if not SECTIONS_SCHEMA.exists():
        raise FileNotFoundError(
            f"Missing section schema: {SECTIONS_SCHEMA}. "
            "Create memory/_sections.json (see the example workspace)."
        )
    data = json.loads(SECTIONS_SCHEMA.read_text(encoding="utf-8"))
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        raise ValueError("memory/_sections.json must define a non-empty 'sections' array")
    return data


def load_watchlist() -> list[dict[str, Any]]:
    if not WATCHLIST.exists():
        return []
    data = json.loads(WATCHLIST.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise RuntimeError("memory/watchlist.json must contain a top-level list")
    return sorted(
        data,
        key=lambda x: (int(x.get("order", 9999)), str(x.get("project", x.get("title", "")))),
    )


# --------------------------------------------------------------------------- #
# Section data collection
# --------------------------------------------------------------------------- #

def collect_projects_for_section(section_id: str) -> list[tuple[int, str, dict[str, Any]]]:
    items: list[tuple[int, str, dict[str, Any]]] = []
    for path in sorted(PROJECT_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        meta = parse_frontmatter(path)
        if not meta:
            continue
        if str(meta.get("archive_status", "")).lower() != "active":
            continue
        if str(meta.get("core_section", "")).strip() != section_id:
            continue
        order = int(meta.get("core_order", 9999))
        items.append((order, path.name, meta))
    items.sort(key=lambda x: (x[0], x[1]))
    return items


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

def cell_value(col: dict[str, Any], record: dict[str, Any], slug: str | None) -> str:
    """Return the string value of one cell.

    `record` is either a project frontmatter dict or a watchlist item dict.
    `slug` is the project filename (without path) when rendering a project row,
    used for link columns.
    """
    keys = col.get("compose") or [col.get("key")]
    parts: list[str] = []
    for key in keys:
        if key == "_link":
            continue
        val = record.get(key, "")
        if val == "" or val is None:
            continue
        parts.append(str(val))
    text = " — ".join(parts).strip()
    if col.get("link") and slug:
        rel = f"projects/{slug}"
        return f"[`link`]({rel})"
    return text.replace("|", "\\|") or " "


def render_table(columns: list[dict[str, Any]], rows: list[tuple[Any, ...]]) -> str:
    header = "| " + " | ".join(c.get("header", c.get("key", "")).replace("|", "\\|") for c in columns) + " |"
    sep = "|" + "|".join("---" for _ in columns) + "|"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def render_section(section: dict[str, Any]) -> str:
    title = section.get("title", section.get("id", "Section"))
    source = section.get("source", "projects")
    columns = section.get("columns") or []
    rows: list[tuple[Any, ...]] = []

    if source == "projects":
        for _order, slug, meta in collect_projects_for_section(section["id"]):
            row = tuple(cell_value(c, meta, slug) for c in columns)
            rows.append(row)
    elif source == "watchlist":
        for item in load_watchlist():
            row = tuple(cell_value(c, item, None) for c in columns)
            rows.append(row)
    else:
        raise ValueError(f"Unknown section source '{source}' for section '{section['id']}'")

    table = render_table(columns, rows)
    return f"## {title}\n\n{table}"


def render_generated_block(schema: dict[str, Any]) -> str:
    sections = schema["sections"]
    # Optional explicit ordering; otherwise preserve declaration order.
    def order_key(s: dict[str, Any], idx: int) -> tuple[int, int]:
        return (int(s.get("order", idx)), idx)
    ordered = sorted(enumerate(sections), key=lambda pair: order_key(pair[1], pair[0]))
    bodies = [render_section(s) for _, s in ordered]
    inner = "\n\n".join(bodies)
    return f"{START_MARKER}\n{inner}\n{END_MARKER}"


def inject_generated_block(core_text: str, block: str) -> str:
    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.S,
    )
    if not pattern.search(core_text):
        raise RuntimeError(
            f"memory/core.md is missing the generated-block markers:\n"
            f"  {START_MARKER}\n  {END_MARKER}\n"
            "Add them where you want the generated section tables to appear."
        )
    return pattern.sub(block.replace("\\", "\\\\"), core_text, count=1)


def stamp_last_updated(core_text: str, stamp_date: str) -> str:
    return re.sub(
        r"(\*\*Last updated:\*\*\s*)\d{4}-\d{2}-\d{2}",
        rf"\g<1>{stamp_date}",
        core_text,
        count=1,
    )


# --------------------------------------------------------------------------- #
# Project index
# --------------------------------------------------------------------------- #

def build_project_index(schema: dict[str, Any]) -> str:
    project_sections = [s for s in schema["sections"] if s.get("source", "projects") == "projects"]

    parts: list[str] = [
        "# Project index",
        "",
        "_Generated by `scripts/rebuild-memory-core.py`. Do not edit by hand._",
        "",
    ]

    if project_sections:
        for section in project_sections:
            title = section.get("title", section.get("id", "Projects"))
            parts.append(f"## {title}")
            parts.append("")
            parts.append("| Project | Stage | Next review | File |")
            parts.append("|---|---|---|---|")
            for _order, slug, meta in collect_projects_for_section(section["id"]):
                parts.append(
                    f"| {meta.get('title', '')} | {meta.get('stage', '')} | "
                    f"{meta.get('next_review_date', '')} | [`link`]({slug}) |"
                )
            parts.append("")

    archive_count = len(list(ARCHIVE_DIR.glob("*.md"))) if ARCHIVE_DIR.exists() else 0
    parts.append("## Archive")
    parts.append("")
    if ARCHIVE_DIR.exists():
        parts.append(
            f"Archived project files live in [`memory/projects/archive/`](archive/) "
            f"({archive_count} file(s))."
        )
    else:
        parts.append("No `memory/projects/archive/` directory yet.")
    parts.append("")
    parts.append("Rebuild with:")
    parts.append("")
    parts.append("```bash")
    parts.append("python3 scripts/rebuild-memory-core.py")
    parts.append("```")
    parts.append("")
    return "\n".join(parts)


# --------------------------------------------------------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild generated memory views.")
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Date to stamp into memory/core.md 'Last updated' line.",
    )
    args = parser.parse_args()

    schema = load_schema()

    core_text = CORE.read_text(encoding="utf-8")
    core_text = stamp_last_updated(core_text, args.date)
    block = render_generated_block(schema)
    core_text = inject_generated_block(core_text, block)
    CORE.write_text(core_text, encoding="utf-8")

    PROJECT_INDEX.write_text(build_project_index(schema), encoding="utf-8")

    print(f"Rebuilt memory/core.md and memory/projects/README.md (date stamp: {args.date})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
