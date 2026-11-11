#!/usr/bin/env python3
"""Consistency check of the sets under sets/: icons.toml against files, names, licences, index.theme.
Usage: check_sets.py <repo root>
"""
import re
import sys
import tomllib
from pathlib import Path

FREE = {"MIT", "Apache-2.0", "Apache-2.0 OR MIT", "MIT OR Apache-2.0", "ISC", "BSD-2-Clause", "BSD-3-Clause",
        "CC0-1.0", "CC-BY-4.0", "CC-BY-SA-4.0", "GPL-3.0-or-later", "GPL-3.0-only", "LGPL-3.0-or-later"}
NAMING = {"spec", "common", "own"}
REQUIRED = ["name", "file", "context", "naming", "meaning", "sizes"]


def check_set(d: Path) -> list[str]:
    errs = []
    data = tomllib.loads((d / "icons.toml").read_text())
    s = data.get("set", {})
    for k in ["id", "name", "kind", "version", "license", "license_files", "origin"]:
        if not s.get(k):
            errs.append(f"[set] {k} missing")
    if s.get("license") not in FREE:
        errs.append(f"licence {s.get('license')!r} is not on the free list")
    for lf in s.get("license_files", []):
        if not (d / lf).is_file():
            errs.append(f"licence file {lf} missing")
    if s.get("id") != d.name:
        errs.append(f"set id {s.get('id')!r} differs from directory {d.name}")
    seen = set()
    for i in data.get("icon", []):
        n = i.get("name", "?")
        for k in REQUIRED:
            if not i.get(k):
                errs.append(f"{n}: {k} missing")
        if n in seen:
            errs.append(f"{n}: duplicate name")
        seen.add(n)
        if not (d / i.get("file", "-")).is_file():
            errs.append(f"{n}: file {i.get('file')} not found")
        if i.get("naming") not in NAMING:
            errs.append(f"{n}: naming must be one of {sorted(NAMING)}")
        if (i.get("naming") == "own") != n.startswith("freesynergy-"):
            errs.append(f"{n}: own names (and only those) start with freesynergy-")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n):
            errs.append(f"{n}: name must be lowercase words joined by '-'")
    listed = {i.get("file") for i in data.get("icon", [])}
    for f in sorted((d / "scalable").rglob("*.svg")) if (d / "scalable").is_dir() else []:
        if str(f.relative_to(d)) not in listed:
            errs.append(f"{f.relative_to(d)}: not listed in icons.toml")
    if s.get("kind") == "icon-theme":
        idx = d / "index.theme"
        if not idx.is_file():
            errs.append("index.theme missing")
        else:
            t = idx.read_text()
            dirs = re.search(r"^Directories=(.*)$", t, re.M)
            for sub in (dirs.group(1).split(",") if dirs else []):
                if f"[{sub}]" not in t:
                    errs.append(f"index.theme: section [{sub}] missing")
                if not (d / sub).is_dir():
                    errs.append(f"index.theme: directory {sub} missing")
    return errs


def main(root: Path) -> int:
    bad = 0
    sets = sorted(p.parent for p in (root / "sets").glob("*/icons.toml"))
    for d in sets:
        for e in check_set(d):
            print(f"{d.name}: {e}")
            bad += 1
    print(f"check_sets: {len(sets)} sets, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
