#!/usr/bin/env python3
"""Archive the contents of trash/ into a timestamped zip with a configurable expiry.

Workflow:
  1. Zip everything currently in trash/ into a single timestamped archive.
  2. Write a JSON manifest next to the archive (file list, sizes, sha256,
     expiry date) so a tidy-up pass can read it without unzipping.
  3. Append a line to today's `tidy_YYYY-MM-DD.log`.
  4. Empty trash/ (only after a successful zip + manifest).
  5. Print a one-line summary plus how to recover items.

The archive lives outside the repo by default at `~/.3t-memory-trash/`,
so the zips do not show up in repo-wide searches. Override with
`--archive-dir` or the `THREET_MEMORY_TRASH_ARCHIVE` environment variable
if you want them in-repo.

Exit codes:
  0  success, or trash was already empty (no-op)
  1  zip or manifest write failed (trash/ is left untouched)
  2  zip succeeded but trash/ could not be emptied (archive preserved)
  3  nothing to do (trash/ missing or empty)

Usage:
    python3 scripts/trash_archive.py
    python3 scripts/trash_archive.py --dry-run
    python3 scripts/trash_archive.py --keep-days 60
    python3 scripts/trash_archive.py --archive-dir /path/to/archive
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRASH = ROOT / "trash"
DEFAULT_EXPIRY_DAYS = 90
DEFAULT_ARCHIVE_DIR = Path.home() / ".3t-memory-trash"


def now_stamp() -> str:
    """Local-time timestamp safe for filenames: YYYY-MM-DD-HHMMSS."""
    return dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")


def log_path_for(today: dt.date) -> Path:
    return ROOT / f"tidy_{today.isoformat()}.log"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files() -> tuple[list[Path], list[Path], int]:
    files = sorted(p for p in TRASH.rglob("*") if p.is_file())
    dirs = sorted(p for p in TRASH.rglob("*") if p.is_dir())
    total_bytes = sum(p.stat().st_size for p in files)
    return files, dirs, total_bytes


def zip_trash(archive_dir: Path, expiry_days: int) -> tuple[Path, Path, dict]:
    """Zip the contents of TRASH into a fresh archive. Return (zip, manifest, meta)."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    stamp = now_stamp()
    zip_path = archive_dir / f"trash-{stamp}.zip"
    manifest_path = archive_dir / f"trash-{stamp}.manifest.json"

    if zip_path.exists():
        raise FileExistsError(f"Archive already exists: {zip_path}")

    files, dirs, total_bytes = collect_files()

    file_records: list[dict] = []
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in files:
            rel = path.relative_to(TRASH).as_posix()
            zf.write(path, arcname=rel)
            file_records.append({
                "path": rel,
                "size": path.stat().st_size,
            })

        # Embed a human-readable manifest inside the zip as well.
        manifest_lines = [
            f"Trash archive manifest - {stamp}",
            f"Files: {len(files)}",
            f"Bytes: {total_bytes}",
            "",
        ]
        manifest_lines.extend(f"{rec['size']:>12}  {rec['path']}" for rec in file_records)
        zf.writestr("MANIFEST.txt", "\n".join(manifest_lines) + "\n")

    expiry = dt.date.today() + dt.timedelta(days=expiry_days)
    meta = {
        "zip": zip_path.name,
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "trash_root": str(TRASH.relative_to(ROOT)),
        "file_count": len(files),
        "dir_count": len(dirs),
        "total_bytes": total_bytes,
        "zip_bytes": zip_path.stat().st_size,
        "zip_sha256": sha256_of(zip_path),
        "expiry_date": expiry.isoformat(),
        "expiry_days": expiry_days,
        "files": file_records,
    }
    manifest_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return zip_path, manifest_path, meta


def empty_trash() -> None:
    for entry in TRASH.iterdir():
        if entry.is_dir() or entry.is_symlink():
            shutil.rmtree(entry, ignore_errors=True)
        else:
            try:
                entry.unlink()
            except FileNotFoundError:
                pass


def append_log(meta: dict, archive_dir: Path) -> Path:
    log = log_path_for(dt.date.today())
    rel_zip = archive_dir / meta["zip"]
    rel_manifest = archive_dir / Path(meta["zip"]).with_suffix(".manifest.json").name
    lines = [
        f"trash-archive {meta['created_at']} - zipped {meta['file_count']} files / "
        f"{meta['total_bytes']:,} bytes from trash/ -> {rel_zip}",
        f"  expiry: {meta['expiry_date']} ({meta['expiry_days']} days; "
        f"recover with: unzip -l {rel_zip}  /  unzip -d /tmp/restore {rel_zip})",
        f"  manifest: {rel_manifest}",
        f"  sha256: {meta['zip_sha256']}",
        "",
    ]
    with log.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return log


def resolve_archive_dir(arg_dir: Path | None) -> Path:
    """Return the user's preferred archive dir, env -> flag -> default."""
    if arg_dir is not None:
        return arg_dir
    env = os.environ.get("THREET_MEMORY_TRASH_ARCHIVE")
    if env:
        return Path(env).expanduser()
    return DEFAULT_ARCHIVE_DIR


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Archive the contents of trash/ into a timestamped zip with a configurable expiry.",
    )
    parser.add_argument(
        "--archive-dir", type=Path, default=None,
        help="Where to write the zip (default: $THREET_MEMORY_TRASH_ARCHIVE or ~/.3t-memory-trash/).",
    )
    parser.add_argument(
        "--keep-days", type=int, default=DEFAULT_EXPIRY_DAYS,
        help=f"Expiry in days, written to the manifest (default: {DEFAULT_EXPIRY_DAYS}).",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would happen but do not zip, log, or delete.",
    )
    args = parser.parse_args()
    archive_dir = resolve_archive_dir(args.archive_dir)

    if not TRASH.exists() or not any(TRASH.iterdir()):
        print("trash/ is empty or missing. Nothing to do.")
        return 3

    files, _dirs, total = collect_files()
    print(f"trash/ contains {len(files)} files, {total:,} bytes")

    if args.dry_run:
        target = archive_dir / f"trash-{now_stamp()}.zip"
        print(f"Would zip to:    {target}")
        print(f"Would log to:    {log_path_for(dt.date.today())}")
        print(f"Would empty:     {TRASH}/")
        print(f"Keep-days:       {args.keep_days}")
        return 0

    try:
        zip_path, manifest_path, meta = zip_trash(archive_dir, args.keep_days)
    except Exception as e:
        print(f"ERROR: zipping failed: {e}", file=sys.stderr)
        return 1

    try:
        empty_trash()
    except Exception as e:
        print(f"ERROR: emptying trash/ failed after zip: {e}", file=sys.stderr)
        print(f"Archive preserved at: {zip_path}", file=sys.stderr)
        return 2

    log = append_log(meta, archive_dir)
    print()
    print(f"Archived:  {zip_path}")
    print(f"Manifest:  {manifest_path}")
    print(f"Logged:    {log}")
    print(f"Expires:   {meta['expiry_date']} (>{meta['expiry_days']} days triggers a warning)")
    print(f"Recover:   unzip -d /tmp/restore {zip_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
