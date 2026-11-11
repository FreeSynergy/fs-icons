#!/usr/bin/env python3
"""Export the glyphs of fs-components-styles (glyph.rs) into the FreeSynergy theme.

usage: import_glyphs.py <path to glyph.rs> [sets/freesynergy]

Writes scalable/<context>/<standard-name>.svg and icons.toml. One-way bridge while the glyphs still live in
Rust; once the SVG files here are the source, the frontend reads them from this package and this script goes.
"""
import re
import sys
from pathlib import Path

# glyph name -> (freedesktop name, context, standard)   standard: spec | common | own
MAP = {
    "mail": ("freesynergy-mail", "actions", "own"),
    "phone": ("freesynergy-phone", "actions", "own"),
    "person": ("freesynergy-person", "actions", "own"),
    "place": ("mark-location", "actions", "spec"),
    "calendar": ("x-office-calendar", "mimetypes", "spec"),
    "search": ("edit-find", "actions", "spec"),
    "plus": ("list-add", "actions", "spec"),
    "close": ("window-close", "actions", "spec"),
    "check": ("freesynergy-check", "status", "own"),
    "warning": ("dialog-warning", "status", "spec"),
    "copy": ("edit-copy", "actions", "spec"),
    "folder": ("folder", "places", "spec"),
    "file-image": ("image-x-generic", "mimetypes", "spec"),
    "file-text": ("text-x-generic", "mimetypes", "spec"),
    "file-archive": ("package-x-generic", "mimetypes", "spec"),
    "file-audio": ("audio-x-generic", "mimetypes", "spec"),
    "file-video": ("video-x-generic", "mimetypes", "spec"),
    "file-pdf": ("application-pdf", "mimetypes", "common"),
    "file-sheet": ("x-office-spreadsheet", "mimetypes", "spec"),
    "file-doc": ("x-office-document", "mimetypes", "spec"),
    "file-slides": ("x-office-presentation", "mimetypes", "spec"),
    "file-code": ("text-x-script", "mimetypes", "spec"),
    "file-unknown": ("application-octet-stream", "mimetypes", "common"),
    "cut": ("edit-cut", "actions", "spec"),
    "paste": ("edit-paste", "actions", "spec"),
    "rename": ("freesynergy-rename", "actions", "own"),
    "share": ("freesynergy-share", "actions", "own"),
    "trash": ("user-trash", "places", "spec"),
    "sort": ("freesynergy-sort", "actions", "own"),
    "view-list": ("view-list-details", "actions", "common"),
    "view-grid": ("view-grid", "actions", "common"),
    "details": ("freesynergy-details", "actions", "own"),
    "back": ("go-previous", "actions", "spec"),
    "forward": ("go-next", "actions", "spec"),
    "up": ("go-up", "actions", "spec"),
    "reload": ("view-refresh", "actions", "spec"),
    "home": ("go-home", "actions", "spec"),
    "drive": ("drive-harddisk", "devices", "spec"),
    "upload": ("freesynergy-upload", "actions", "own"),
    "download": ("freesynergy-download", "actions", "own"),
    "filter": ("freesynergy-filter", "actions", "own"),
    "transfers": ("freesynergy-transfers", "actions", "own"),
    "info": ("dialog-information", "status", "spec"),
}

SVG = ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" '
       'stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">'
       '<path d="{d}"/></svg>\n')


def parse(src: str):
    """Return [(glyph name, doc, path data)] in enum order."""
    variants = re.findall(r"///\s*(.+)\n\s*(\w+),", src.split("impl Glyph")[0])
    docs = {v: d.strip() for d, v in variants}
    paths = {}
    body = src.split("pub const fn path")[1].split("pub const fn name")[0]
    for m in re.finditer(r"Glyph::(\w+)\s*=>\s*(?:\{\s*)?\"([^\"]+)\"", body):
        paths[m.group(1)] = m.group(2)
    names = {}
    nbody = src.split("pub const fn name")[1]
    for m in re.finditer(r"Glyph::(\w+)\s*=>\s*\"([^\"]+)\"", nbody):
        names[m.group(1)] = m.group(2)
    return [(names[v], docs[v], paths[v]) for v in names]


def main() -> int:
    glyph_rs = Path(sys.argv[1])
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "sets/freesynergy")
    glyphs = parse(glyph_rs.read_text())
    toml = []
    for name, doc, path in glyphs:
        std, ctx, kind = MAP[name]
        f = out / "scalable" / ctx / f"{std}.svg"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(SVG.format(d=path))
        toml.append(
            f'[[icon]]\nname = "{std}"\nfile = "scalable/{ctx}/{std}.svg"\ncontext = "{ctx}"\n'
            f'naming = "{kind}"\nsource_name = "{name}"\nmeaning = "{doc}"\n'
            f'purpose = ""\nused_in = ["fs-files"]\nsizes = ["scalable"]\n'
        )
    header = (out / "icons.header.toml").read_text()
    (out / "icons.toml").write_text(header + "\n" + "\n".join(toml))
    print(f"{len(glyphs)} glyphs written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
