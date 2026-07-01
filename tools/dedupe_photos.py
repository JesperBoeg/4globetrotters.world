# -*- coding: utf-8 -*-
"""
Remove duplicate photos from a folder by content hash (exact byte match).

Safe re-run tool: when the same file has been uploaded multiple times (often as
"IMG_1234 (1).HEIC", "IMG_1234 (2).HEIC", ...), this keeps ONE copy per unique
content and deletes the rest.

Keep-priority within a duplicate group:
  1. the name WITHOUT a "(N)" suffix (the canonical original), else
  2. the smallest "(N)", else
  3. shortest name, then alphabetical — deterministic tie-break.

Usage:
  python tools/dedupe_photos.py "G:\\My Drive\\Pictures\\2026 Labuan Bajo"          # dry run (default)
  python tools/dedupe_photos.py "G:\\My Drive\\Pictures\\2026 Labuan Bajo" --delete # actually delete
"""
import sys, re, hashlib
from pathlib import Path
from collections import defaultdict

def file_hash(p, chunk=1 << 20):
    h = hashlib.md5()
    with open(p, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

SUFFIX_RE = re.compile(r"^(?P<stem>.*?)(?: \((?P<n>\d+)\))?(?P<ext>\.[^.]+)$")

def keep_rank(path: Path):
    """Lower rank = more preferred to keep."""
    m = SUFFIX_RE.match(path.name)
    n = m.group("n") if m else None
    has_suffix = 1 if n is not None else 0          # prefer no "(N)" suffix
    num = int(n) if n is not None else -1           # then smallest N
    return (has_suffix, num, len(path.name), path.name)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_delete = "--delete" in sys.argv
    if not args:
        print("Usage: python tools/dedupe_photos.py <folder> [--delete]")
        sys.exit(1)
    folder = Path(args[0])
    if not folder.is_dir():
        print(f"Not a folder: {folder}")
        sys.exit(1)

    files = [p for p in folder.iterdir() if p.is_file()]
    print(f"Scanning {len(files)} files in {folder} ...")

    by_hash = defaultdict(list)
    for p in files:
        by_hash[file_hash(p)].append(p)

    groups = {h: ps for h, ps in by_hash.items() if len(ps) > 1}
    total_dupes = sum(len(ps) - 1 for ps in groups.values())

    print(f"\nUnique contents: {len(by_hash)}")
    print(f"Duplicate groups: {len(groups)}")
    print(f"Redundant files to remove: {total_dupes}\n")

    deleted = 0
    for h, ps in sorted(groups.items(), key=lambda kv: kv[1][0].name):
        ps_sorted = sorted(ps, key=keep_rank)
        keep, remove = ps_sorted[0], ps_sorted[1:]
        print(f"KEEP  {keep.name}")
        for r in remove:
            print(f"  DEL {r.name}")
            if do_delete:
                r.unlink()
                deleted += 1

    if do_delete:
        print(f"\nDeleted {deleted} duplicate files.")
    else:
        print(f"\nDRY RUN — nothing deleted. Re-run with --delete to remove the {total_dupes} files above.")

if __name__ == "__main__":
    main()
