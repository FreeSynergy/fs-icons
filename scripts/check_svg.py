#!/usr/bin/env python3
"""SVG safety check for icon sets. Usage: check_svg.py [--max-bytes N] <file or directory>...

Fails (exit 1) on: <script>, on* attributes, external href / xlink:href (only #fragment and data:image/ allowed),
url(http...) references, <foreignObject>, <iframe>/<embed>/<object>/<use> to other files, DOCTYPE with ENTITY
(XML bombs), files over the size limit, files that are not well-formed XML with an <svg> root.
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

MAX_BYTES = 64 * 1024
FORBIDDEN_TAGS = {"script", "foreignobject", "iframe", "embed", "object", "audio", "video"}


def local(name: str) -> str:
    return name.rsplit("}", 1)[-1].lower()


def check_bytes(data: bytes, max_bytes: int = MAX_BYTES) -> list[str]:
    """Return the problems found in one SVG document (empty list = fine)."""
    problems = []
    if len(data) > max_bytes:
        problems.append(f"too large: {len(data)} bytes (limit {max_bytes})")
    text = data.decode("utf-8", errors="replace")
    if re.search(r"<!ENTITY", text, re.I):
        problems.append("ENTITY declaration")
        return problems
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        return problems + [f"not well-formed XML: {e}"]
    if local(root.tag) != "svg":
        problems.append(f"root element is <{local(root.tag)}>, not <svg>")
    for el in root.iter():
        tag = local(el.tag)
        if tag in FORBIDDEN_TAGS:
            problems.append(f"forbidden element <{tag}>")
        for attr, value in el.attrib.items():
            a = local(attr)
            if re.fullmatch(r"on[a-z]+", a):
                problems.append(f"event attribute {a}")
            if a == "href" and not (value.startswith("#") or value.lower().startswith("data:image/")):
                problems.append(f"external reference {a}={value[:60]!r}")
            if re.search(r"url\(\s*['\"]?\s*(https?:|//|file:|javascript:)", value, re.I):
                problems.append(f"external url() in {a}")
            if value.strip().lower().startswith("javascript:"):
                problems.append(f"javascript: in {a}")
        if tag == "style" and el.text and re.search(r"(@import|url\(\s*['\"]?\s*(https?:|//))", el.text, re.I):
            problems.append("external reference in <style>")
    return problems


def collect(paths: list[str]) -> list[Path]:
    files = []
    for p in map(Path, paths):
        files += sorted(p.rglob("*.svg")) if p.is_dir() else [p]
    return files


def main(argv: list[str]) -> int:
    max_bytes = MAX_BYTES
    if argv[:1] == ["--max-bytes"]:
        max_bytes, argv = int(argv[1]), argv[2:]
    if not argv:
        print(__doc__)
        return 2
    bad = 0
    files = collect(argv)
    for f in files:
        for problem in check_bytes(f.read_bytes(), max_bytes):
            print(f"{f}: {problem}")
            bad += 1
    print(f"check_svg: {len(files)} files, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
