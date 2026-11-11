#!/usr/bin/env python3
"""Export the glyphs of fs-components-styles (glyph.rs) into the FreeSynergy theme.

usage: import_glyphs.py <path to glyph.rs> [sets/freesynergy-theme]

Writes scalable/<context>/<name>.svg (coloured variant, still the line drawing: status draft-colour), the
-symbolic variant (single colour, currentColor) and icons.toml. One-way bridge while the glyphs still live in
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
    "place": ("mark-location", "actions", "common"),
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


# glyph name -> (purpose EN, purpose DE). Short; the frontend agent corrects where the real use differs.
PURPOSE = {
    "mail": ("Mail address of a person or a message button.", "E-Mail-Adresse einer Person oder Schaltfläche für Nachrichten."),
    "phone": ("Phone number of a person.", "Telefonnummer einer Person."),
    "person": ("A person or a name field.", "Eine Person oder ein Namensfeld."),
    "place": ("A place or postal address.", "Ein Ort oder eine Postanschrift."),
    "calendar": ("A date, a calendar file or a date field.", "Ein Datum, eine Kalenderdatei oder ein Datumsfeld."),
    "search": ("Start a search or mark the search field.", "Suche starten oder Suchfeld kennzeichnen."),
    "plus": ("Add or create something new.", "Etwas hinzufügen oder neu anlegen."),
    "close": ("Close a window, panel or dialog.", "Fenster, Leiste oder Dialog schließen."),
    "check": ("Done, confirmed or selected.", "Erledigt, bestätigt oder ausgewählt."),
    "warning": ("Warn about something that needs attention.", "Auf etwas hinweisen, das Beachtung braucht."),
    "copy": ("Copy the selection.", "Auswahl kopieren."),
    "folder": ("A folder in lists, trees and places.", "Ein Ordner in Listen, Bäumen und Orten."),
    "file-image": ("File kind: picture.", "Dateiart: Bild."),
    "file-text": ("File kind: plain text.", "Dateiart: einfacher Text."),
    "file-archive": ("File kind: archive or package.", "Dateiart: Archiv oder Paket."),
    "file-audio": ("File kind: sound or music.", "Dateiart: Ton oder Musik."),
    "file-video": ("File kind: video.", "Dateiart: Video."),
    "file-pdf": ("File kind: PDF document.", "Dateiart: PDF-Dokument."),
    "file-sheet": ("File kind: spreadsheet.", "Dateiart: Tabellenkalkulation."),
    "file-doc": ("File kind: word-processing document.", "Dateiart: Textdokument."),
    "file-slides": ("File kind: presentation.", "Dateiart: Präsentation."),
    "file-code": ("File kind: source code or script.", "Dateiart: Quelltext oder Skript."),
    "file-unknown": ("File kind not known: plain sheet.", "Dateiart unbekannt: leeres Blatt."),
    "cut": ("Cut the selection.", "Auswahl ausschneiden."),
    "paste": ("Paste from the clipboard.", "Aus der Zwischenablage einfügen."),
    "rename": ("Rename the selected item.", "Ausgewähltes Element umbenennen."),
    "share": ("Share the selected item with others.", "Ausgewähltes Element mit anderen teilen."),
    "trash": ("Move to the bin or open the bin.", "In den Papierkorb legen oder Papierkorb öffnen."),
    "sort": ("Change the sort order.", "Sortierung ändern."),
    "view-list": ("Show items as a list.", "Elemente als Liste zeigen."),
    "view-grid": ("Show items as a grid of big icons.", "Elemente als Raster großer Symbole zeigen."),
    "details": ("Show or hide the details panel.", "Detailleiste ein- oder ausblenden."),
    "back": ("Go back in the history.", "Im Verlauf zurückgehen."),
    "forward": ("Go forward in the history.", "Im Verlauf vorwärts gehen."),
    "up": ("Go to the parent folder.", "Zum übergeordneten Ordner gehen."),
    "reload": ("Reload the current view.", "Aktuelle Ansicht neu laden."),
    "home": ("Go to the home folder or start page.", "Zum Home-Ordner oder zur Startseite gehen."),
    "drive": ("A drive or storage place.", "Ein Laufwerk oder Speicherort."),
    "upload": ("Send a file to the server.", "Eine Datei zum Server senden."),
    "download": ("Fetch a file from the server.", "Eine Datei vom Server holen."),
    "filter": ("Narrow a list by a condition.", "Liste nach einer Bedingung einschränken."),
    "transfers": ("Show running uploads and downloads.", "Laufende Übertragungen anzeigen."),
    "info": ("Show information about the item.", "Informationen zum Element zeigen."),
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
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "sets/freesynergy-theme")
    glyphs = parse(glyph_rs.read_text())
    toml = []
    for name, doc, path in glyphs:
        std, ctx, kind = MAP[name]
        en, de = PURPOSE[name]
        for suffix in ("", "-symbolic"):
            f = out / "scalable" / ctx / f"{std}{suffix}.svg"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(SVG.format(d=path))
        toml.append(
            f'[[icon]]\nname = "{std}"\nfile = "scalable/{ctx}/{std}.svg"\ncontext = "{ctx}"\n'
            f'naming = "{kind}"\nsource_name = "{name}"\nmeaning = "{doc}"\n'
            f'purpose = "{en}"\npurpose_de = "{de}"\nused_in = ["fs-files"]\nsizes = ["scalable"]\n'
            f'variants = ["symbolic"]\nstatus = "draft-colour"\n'
        )
    header = (out / "icons.header.toml").read_text()
    (out / "icons.toml").write_text(header + "\n" + "\n".join(toml))
    print(f"{len(glyphs)} glyphs written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
