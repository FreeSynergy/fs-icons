# Programme icons (fs-store, fs-tasks, fs-people, fs-calendar, fs-files, fs-wiki, fs-maps)

Status: draft for review, not in the catalogue. Files: `FreeSynergy/apps/<id>.svg` (colour) and `FreeSynergy/apps/<id>-symbolic.svg`. Entries: `FreeSynergy/icons.toml`.

Family rules / Familienregeln: 128x128 viewBox, rounded tile (112 px, radius 28), one colour family per programme (light top-left to dark bottom-right), soft gloss on the upper half, a hard offset shadow below tile and glyph (light from top-left), white and tinted-white glyph with content, no filters, no text. Symbolic: 16x16 grid, `currentColor`, for bars and small sizes only. Licence for all 14 files: `MIT OR Apache-2.0` (`LICENSE-MIT`, `LICENSE-APACHE` in `FreeSynergy/`), own drawing, origin FreeSynergy project; nothing traced from another set.

Revision 2 / Überarbeitung 2: symbolic store is now a plain crate (lid, body, handle slot; no arrow); symbolic wiki carries the bookmark notch like the colour icon; symbolic files has a larger tab and a gap between tab part and front; calendar and tasks symbolics have larger cells/check strokes (min. 1.3 px on the 16 grid). Colour tasks and wiki glyphs enlarged (sheet 80x88 / page 80x90 in the 112 tile, about 55 to 60 % of the tile) so main glyph density matches calendar and maps; colours unchanged. Symbolic icons keep `currentColor`; previews substitute the theme foreground (light #2e3436, dark #eeeeec) at render time only.

## fs-store
- EN: Package store. Amber/gold tile; a white parcel box (lid, cream body, golden tape, handle slot) with an arrow dropping in. Use colour at 48 px and larger; `-symbolic` (plain crate, no arrow) for bars below 32 px.
- DE: Paketladen. Bernstein/Gold-Kachel; weiße Paketkiste (Deckel, cremefarbener Korpus, goldenes Band, Griffschlitz) mit einfallendem Pfeil. Farbe ab 48 px; `-symbolic` (schlichte Kiste, ohne Pfeil) für Leisten unter 32 px.

## fs-tasks
- EN: Tasks/board. Green tile; a white clipboard with dark clip and three rows: two done (green check), one open (ring). Colour from 48 px; symbolic clipboard with check below 32 px.
- DE: Aufgaben. Grüne Kachel; weißes Klemmbrett mit dunkler Klammer und drei Zeilen: zwei erledigt (grüner Haken), eine offen (Ring). Farbe ab 48 px; Symbolic (Klemmbrett mit Haken) unter 32 px.

## fs-people
- EN: People/contacts. Pink/magenta tile; a white person in front (head, shoulders, pink edge for separation), a pale pink second person behind. Colour from 48 px; symbolic two-person shape below 32 px.
- DE: Menschen/Kontakte. Pink/Magenta-Kachel; vorne eine weiße Person (Kopf, Schultern, rosa Rand zur Trennung), dahinter eine blassrosa zweite Person. Farbe ab 48 px; Symbolic (zwei Personen) unter 32 px.

## fs-calendar
- EN: Calendar. Red tile; a white page with dark-red header band, two binder rings, a grid of grey day cells and one red marked day. Colour from 48 px (cells blur at 32 px); symbolic calendar frame with dots below 32 px.
- DE: Kalender. Rote Kachel; weiße Seite mit dunkelrotem Kopfband, zwei Ringen, Raster grauer Tageszellen und einem roten markierten Tag. Farbe ab 48 px (Zellen verschwimmen bei 32 px); Symbolic (Rahmen mit Punkten) unter 32 px.

## fs-files
- EN: Files/folders. Blue tile; a dark-blue folder back with tab, two white sheets peeking out, a pale-blue front panel with a bright top edge. Colour from 48 px; symbolic two-part folder below 32 px.
- DE: Dateien/Ordner. Blaue Kachel; dunkelblaue Ordnerrückseite mit Reiter, zwei weiße Blätter ragen heraus, hellblaue Vorderseite mit heller Oberkante. Farbe ab 48 px; Symbolic (zweiteiliger Ordner) unter 32 px.

## fs-wiki
- EN: Notes/pages. Indigo tile; a white page with folded corner, indigo heading bar, three lavender text lines and a yellow bookmark ribbon. Colour from 48 px; symbolic page outline with bookmark and two lines below 32 px.
- DE: Notizen/Seiten. Indigo-Kachel; weiße Seite mit umgeknickter Ecke, indigofarbener Überschrift, drei lavendelfarbenen Textzeilen und gelbem Lesezeichen. Farbe ab 48 px; Symbolic (Seitenumriss mit Lesezeichen und zwei Zeilen) unter 32 px.

## fs-maps
- EN: Map/places. Cyan/teal tile; a folded three-panel map (pale cyan, white, light cyan) with a park, a water patch, a path, and a coral location pin with white centre. Colour from 48 px; symbolic pin below 32 px.
- DE: Karte/Orte. Cyan/Petrol-Kachel; gefaltete dreiteilige Karte (blasscyan, weiß, hellcyan) mit Park, Wasserfläche, Weg und korallenrotem Standortpin mit weißem Zentrum. Farbe ab 48 px; Symbolic (Pin) unter 32 px.
