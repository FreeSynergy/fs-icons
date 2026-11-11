# fs-icons: revive plan (2026-11-12)

Status: inventory done, skeleton in place, Strategy decisions of 2026-11-12 applied (this branch `revive-icons`, based on origin/main `91a34d3`). Nothing pushed, nothing deleted.

## 1. Inventory (origin/main 91a34d3, 93 MB without .git)

| Path | What | SVG files | Size | Licence evidence |
|---|---|---|---|---|
| `FreeSynergy/` | old "brand/UI" set, 62 icons, 24 grid, stroke `currentColor`, plus `languages/` (de, en) | 62 | 248 KB | only `manifest.toml` says MIT. No file, no author, no source. The style looks like a common stroke set; provenance unproven (rule: nothing copied). |
| `homarrlabs/` | app and service logos, many `-dark`/`-light` pairs | 2757 | 36 MB | Repo `LICENSE` is FreeSynergy's own MIT and covers no set. Upstream `homarr-labs/dashboard-icons` `LICENSE` (read 2026-11-12) is **Apache-2.0**, not MIT as README/manifest say. Apache-2.0 needs the licence text shipped and a notice. Many files are third-party brand logos: the repo licence cannot grant trademark or logo rights (not verified per file). |
| `We10X/` | freedesktop theme (actions, apps, categories, devices, emblems, emotes, mimes, places, preferences, status, animations) | 10510 | 57 MB | Upstream `yeyushengfan258/We10X-icon-theme` has `COPYING` = **GPL-3.0** (read 2026-11-12). No licence file and no notice in this repo. Imitates a Windows 10 look (design/trademark risk, unchecked). |
| `cursor-sets/midnight/` | 31 cursors as SVG | 31 | 128 KB | none; origin unknown. |
| `assets/icon.svg` | repo icon | 1 | 4 KB | none |
| `sync/`, `Cargo.*`, `Containerfile`, `.githooks`, `setup.sh`, `package.toml`, `deny.toml`, `.clippy.toml`, `rustfmt.toml`, `CLAUDE.md`, `.github/workflows/ci.yml` | old-era tooling | | | |

Findings:
- Licence facts in `manifest.toml`/`README` were wrong or unbacked: homarrlabs "MIT" (upstream Apache-2.0), We10X without licence text. Corrected now (section 5, done items); the old `freesynergy` "MIT" stays as it is until the owner confirms (user question to Strategy).
- SVG safety scan (new `scripts/check_svg.py`, 64 KB limit): 13267 files, 150 problems in 141 files. homarrlabs: 65 files (3 `<script>`: carousell, falcon-player and one more; 8 `<foreignObject>`; 31 `<style>` with external font URLs, e.g. archivebox; 4 not XML; embedded `data:img/png` hrefs; oversize). We10X: 76 files (mostly oversize, 1 external). `FreeSynergy/`, `cursor-sets/`, `assets/`: clean. Full list: `python3 -I scripts/check_svg.py homarrlabs We10X`.
- `sync/` (Rust, `fs-icons-sync`, 218 lines, gix shallow clone): pulls homarrlabs `svg/` and We10X `src/` from upstream into the tree. It copies whatever upstream has, without licence or safety checks, and overwrites our fixes. `Cargo.lock` is 80 KB of gix dependencies.

## 2. Structure (skeleton done)

```
sets/<id>/            one directory per set; the set is the unit of licence, origin, package
  icons.toml          THE data source of the set ([set] meta + [[icon]] entries)
  index.theme         freedesktop Icon Theme Specification (Inherits=hicolor)
  scalable/<context>/<name>.svg    contexts: actions, status, places, mimetypes, devices ...
  LICENSE-*           the licence(s) of exactly this set
scripts/check_svg.py  SVG safety (no script, no on* attributes, no external href/url(), no foreignObject, size limit, no ENTITY)
scripts/check_sets.py icons.toml vs files vs index.theme vs licence (free list); own names only with prefix freesynergy-
scripts/gates.sh      the one measure (tests + check_sets + check_svg on sets/); .github/workflows/check.yml runs the same
scripts/gen_excluded.py  writes EXCLUDED.md of a third-party set (flagged files, reason; files stay untouched)
scripts/import_glyphs.py  bridge: exports the 43 glyphs of fs-components-styles (glyph.rs) into sets/freesynergy
packaging/            example package manifest (section 4)
```
- `sets/freesynergy/`: 43 glyphs exported from `glyph.rs` at frontend-files `446d7ea`, names per Icon Naming Specification (`naming = spec`), widely used names that the Icon Naming Specification does NOT list marked `common` (checked against the spec text on 2026-11-12: `mark-location`, `view-list-details`, `view-grid`, `application-pdf`, `application-octet-stream` are not in it; `user-trash`, `drive-harddisk` are), our own with prefix `freesynergy-` (mail, phone, person, check, rename, share, sort, details, upload, download, filter, transfers). Each icon exists twice: `name.svg` (coloured variant, currently the same line drawing, `draft-colour`) and `name-symbolic.svg` (single colour, `currentColor`), see section 7. Stroke 1.75. These shapes change when the frontend agent rebases (stroke width, 3D nuance, standard names): re-run the importer, or after the hand-over edit the SVG files directly and drop the importer.
- Legacy directories stay where they are until decided (below). They are not gated and not in `sets/`.
- Each further set: own directory under `sets/`, own `icons.toml` with licence and origin, free licence only (list in `check_sets.py`), licence text shipped.

## 3. icons.toml (schema)
`[set]`: id, name, kind (`icon-theme`), version, license (SPDX), license_files, origin, grid, inherits.
`[[icon]]`: name, file, context, naming (`spec|common|own`), source_name, meaning (what it shows), purpose (what for), used_in (where reused), sizes (`scalable` or pixels).
`purpose` (EN) and `purpose_de` (DE) are filled for all 43 (short, from name and use; the frontend agent corrects where the real use differs) and are required by `check_sets.py`. `variants = ["symbolic"]` says that `<name>-symbolic.svg` exists next to the file (single colour, `currentColor`); `status = "draft-colour"` says that the coloured file is still the line drawing and waits for the coloured version (light 3D nuance) of the frontend agent.
Generators to write next, in fs-documentation: a component page DE+EN per set (belongs to check-docs next to gen_component_indexes), reading only `icons.toml`.

## 4. Sets as packages (description only, no store code touched)
Kind `icon-theme` next to `program` in the catalogue (`fs-catalog/packages.toml`). Example: `packaging/freesynergy.package.toml`: id `icon-theme-freesynergy`, kind, version 0.0.N, licence, `[content]` set/index/catalogue/install dir (`icons/FreeSynergy` under the XDG data dir), `[source]` repo, tag, asset `icon-theme-<id>-{version}.tar.gz` of `sets/<id>/`. Installation = unpack into the icon directory; no code runs. Sources follow ADR 0068; a signed own source for designers comes later (same signature as other assets). Each set is its own package with its own licence, so the user chooses what to install.
Gap: `fs-release/.github/workflows/release.yml` builds binaries only (kinds cli/daemon/app); a data kind (tarball of `sets/<id>`, signed, draft release) does not exist. Needs a decision and a change in fs-release; not done here. `release.yml` is therefore NOT added to this repo yet.

## 5. Decisions and status

Done (2026-11-12, local):
- **We10X (GPL-3.0)**: `We10X/COPYING` (full text from upstream commit `0f52ff2d...`) and `We10X/NOTICE.md` (author, upstream URL, source of the text, version/commit situation, changes: none known) added; `manifest.toml` and `README.md` corrected (GPL-3.0, `default = false`). Files untouched.
- **homarrlabs (Apache-2.0)**: `homarrlabs/LICENSE` (upstream text, commit `d767d732...`) and `homarrlabs/NOTICE` (copyright, upstream, trademark notice EN+DE: "Logos are trademarks of their owners, for identification only") added; manifest/README corrected to Apache-2.0, `default = false`. Optional, separate set, never in the default. Flagged files are NOT cleaned (that would alter third-party logos): they are excluded from the package and listed with reason in `homarrlabs/EXCLUDED.md` (65 files; scripts, foreignObject, external fonts/references, not XML, oversize; generated by `scripts/gen_excluded.py`, which can be re-run). The same list exists for `We10X/EXCLUDED.md` (76 files, mostly oversize) so a later package has it ready. Trademark and use rights of the logos themselves are not cleared by the licence: check the owners' brand rules before any store listing; recommendation: only as an optional separate set with licence and trademark notice, never as default.
- Old `FreeSynergy/` (62, "by KalEl · Cyan + White", probably the owner's icons): unchanged. Origin and licence: **user is asked via Strategy**. Planned fate: it falls away once `sets/freesynergy` covers all names the programs use AND the origin cannot be proven. Nothing deleted.

Pending, needs a Yes from the owner (deleting) or other work:
- **We10X leaves fs-icons**: becomes its own optional set package with its own licence (mirror per ADR 0068), never default. Removing it from this repo is a deletion; waits for the owner's Yes.
- **Rust `sync/`, `Cargo.*`, `.clippy.toml`, `rustfmt.toml`, `deny.toml`, `Containerfile`, `package.toml`, `setup.sh`, `.githooks`, `CLAUDE.md`, `ci.yml`**: proposal unchanged, not removed. `sync` pulls upstream SVGs blindly (no licence, no safety check, overwrites our fixes) and is not needed for our own set; for third-party sets use a small reviewed import script per set that writes `icons.toml` with licence and origin, then `check_svg.py`. `package.toml` and `Containerfile` are stale (they name homarrlabs/we10x and the wrong path `we10x/`). Note `ci.yml` still runs cargo and a grep-based SVG check on the whole tree.
- **cursor-sets/midnight**: origin unknown; not icon-theme material; keep out of packages until proven.
- **Release action for icon packages**: in fs-release after the current milestone (noted). Decision template in section 6.
- `README.md`/`manifest.toml` are corrected for the licence facts only; full rewrite after the layout is final. Root `LICENSE` is still the single MIT file (migrated repos use LICENSE-APACHE and LICENSE-MIT).

### Update 2026-11-12 (owner's Yes via Strategy)
- **Removed (git rm, local, branch revive-icons):** `We10X/` (GPL-3.0, no standard set any more), `sync/` (replaced by gates and `check_sets.py`), `Cargo.toml`, `Cargo.lock`, and the Rust-only files `.clippy.toml`, `rustfmt.toml`, `deny.toml`, `.githooks/`, `setup.sh` (they only served the Rust code). `ci.yml` lost its cargo, deny and audit jobs (the SVG scan job stays). `package.toml`, `Containerfile`, `manifest.toml`, `README.md`, `CLAUDE.md` were cleaned of We10X and sync. Nothing else was deleted.
- We10X stays in git history (commit before this one). If a user wants it later it becomes its own optional package with its own licence (mirror per ADR 0068), never default.
- **Later:** look for more free sets (checked licence, separate set each) or draw our own (SVG, also with AI help; each with `icons.toml`, licence and origin).
- **Old `FreeSynergy/` (62):** belongs to the owner: origin "Owner (KalEl), logos", licence `MIT OR Apache-2.0` (repo convention), entered in `manifest.toml`, `README.md` and `FreeSynergy/icons.toml`, licence files copied. The text above that says "origin unproven / falls away" is superseded: it stays until the programs use the new theme names, then it is decided again.

## 6. Decision template: release action for icon packages (signed tarball per set)

Today: `fs-release/.github/workflows/release.yml` builds binaries (kinds cli, daemon, app) into deb/rpm/AppImage/zip/msi and so on, signs and attests, and creates a draft release. A data package (no binary) has no kind.

| Option | What | For | Against |
|---|---|---|---|
| A. New kind `data` (or `icon-theme`) in `release.yml` | job packs `sets/<id>/` into `<name>-<version>.tar.gz`, signs it with the same GPG key, attests, draft release; input `set` | one pipeline, same signing and draft rules as every program; catalogue generator (`gen_catalog.py`) already reads release assets | change in the central fs-release (all programs use it): needs tests there; the milestone in progress comes first |
| B. Small own workflow in fs-icons that calls only the signing and draft building blocks of fs-release (`actions/*`) | per-repo `release.yml` for tarballs | no change to the big pipeline; quick | duplicates the "one measure" idea; two places to keep in line |
| C. No release, catalogue points at a git tag archive | tag only | nothing to build | unsigned archive; breaks the rule that every file is verified against the project key |

Recommendation: A, after the fs-release milestone; B only if the first icon package is needed earlier. C rejected (signature). Open for the owner: the kind name (`icon-theme` as in the catalogue, or `data`); per-set tag (`icon-theme-freesynergy-v0.0.N`) versus one repo tag with several assets.

## 7. Decision (Strategy, 2026-11-12): colours, symbolic variants

Decision: both, by freedesktop convention. The normal name is the coloured icon (light 3D nuance); next to it a `-symbolic` variant, single colour with `currentColor`, for bars and menus. Our renderer resolves `currentColor` from the theme; other toolkits take the coloured variants (or their own recolouring of the symbolic ones). In `icons.toml`: `variants = ["symbolic"]` (file `<name>-symbolic.svg` next to `<name>.svg`) and `status`.

What the sources say (read 2026-11-12):
- freedesktop Icon Theme Specification (http://specifications.freedesktop.org/icon-theme/latest/): the words "symbolic" and "recolor" do not appear; it defines lookup and `Inherits`, not recolouring. A missing icon is searched in inherited themes; dashes in names are not a fallback rule in the spec itself. So `-symbolic` is a convention on top, not part of the spec.
- freedesktop Icon Naming Specification (http://specifications.freedesktop.org/icon-naming/latest/): no `-symbolic` suffix; the word appears only in `emblem-symbolic-link`. The names we use are standard except those marked `common` (not in the spec: see section 2). Own names are allowed; we prefix them `freesynergy-`.
- GTK 4: `GtkIconPaintable` implements `GtkSymbolicPaintable` (https://docs.gtk.org/gtk4/class.IconPaintable.html, https://docs.gtk.org/gtk4/iface.SymbolicPaintable.html): symbolic paintables get "at least 5 colors ... every time": foreground, error, warning, success and (GTK 4.22) accent; `snapshot_symbolic` draws with them. So GTK recolours symbolic icons by itself; the docs do not say how a `-symbolic` name is recognised (known convention: file name ends in `-symbolic`; not verified in these docs). `is_symbolic()` is deprecated since 4.20.
- Qt: `QIcon::setIsMask` marks an icon as a mask that "can potentially be modified based on where it's displayed" (https://doc.qt.io/qt-6/qicon.html); `QIcon::fromTheme` follows the freedesktop lookup. The pages read do not describe `-symbolic` handling in Qt.
- KDE: the page read (https://develop.kde.org/docs/features/additional-features/icons/) says Plasma follows the freedesktop specification, falls back to more generic names (`document-open-recent` to `document-open`), and names Cuttlefish for inspecting colour schemes; it does not explain recolouring. Breeze monochrome icons are recoloured with a colour-scheme style sheet inside the SVG (known from the Breeze icon sources; NOT verified in this session: check before relying on it).
- GNOME HIG, app icons (https://developer.gnome.org/hig/guidelines/app-icons.html): "Each app should have an additional symbolic version of its app icon" for small sizes and special contexts.

Consequences and trade-offs:
- `currentColor` in a plain SVG theme file is resolved by browsers/our renderer, not by every toolkit: some load such files with black. That is why the coloured variants stay and are the fallback.
- Recolouring of `-symbolic` by GTK is documented (colour list above); Qt/KDE behaviour is unconfirmed here, so test with real toolkits before promising it.
- Cost: every icon twice (86 files for 43 icons); the coloured variant is a draft until the frontend agent delivers the 3D nuance (`status = "draft-colour"`). The single-colour variant is what exists today.
- `check_sets.py` requires the variant file to exist when `variants` lists it, and lists variant files as part of the icon.

## 8. Open points
- Pixel-hinted sizes (16/22) later, if wanted; for now only `scalable` (24 grid, MinSize 16, MaxSize 512).
- Docs generator in fs-documentation reading only `icons.toml` (DE+EN component pages; belongs to check-docs next to gen_component_indexes).
- Qt/KDE recolouring of `-symbolic`: test with real toolkits.
- Owner confirmation of the origin of the old `FreeSynergy/` set (asked via Strategy).
