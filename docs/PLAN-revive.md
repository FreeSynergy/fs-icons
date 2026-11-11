# fs-icons: revive plan (2026-11-12)

Status: inventory done, skeleton in place (this branch `revive-icons`, based on origin/main `91a34d3`). Nothing pushed.

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
- Licence facts in `manifest.toml`/`README` are wrong or unbacked: homarrlabs "MIT" (upstream Apache-2.0), `freesynergy` "MIT" (no proof), We10X has no licence text.
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
scripts/import_glyphs.py  bridge: exports the 43 glyphs of fs-components-styles (glyph.rs) into sets/freesynergy
packaging/            example package manifest (section 4)
```
- `sets/freesynergy/`: 43 glyphs exported from `glyph.rs` at frontend-files `446d7ea`, names per Icon Naming Specification (`naming = spec`), widely used non-spec names marked `common` (`view-list-details`, `view-grid`, `application-pdf`, `application-octet-stream`), our own with prefix `freesynergy-` (mail, phone, person, check, rename, share, sort, details, upload, download, filter, transfers). Stroke 1.75, `currentColor`. These shapes change when the frontend agent rebases (stroke width, 3D nuance, standard names): re-run the importer, or after the hand-over edit the SVG files directly and drop the importer.
- Legacy directories stay where they are until decided (below). They are not gated and not in `sets/`.
- Each further set: own directory under `sets/`, own `icons.toml` with licence and origin, free licence only (list in `check_sets.py`), licence text shipped.

## 3. icons.toml (schema)
`[set]`: id, name, kind (`icon-theme`), version, license (SPDX), license_files, origin, grid, inherits.
`[[icon]]`: name, file, context, naming (`spec|common|own`), source_name, meaning (what it shows), purpose (what for), used_in (where reused), sizes (`scalable` or pixels).
`purpose` is still empty for all 43 (needs the designer or the frontend agent; the gate does not require it yet, see open points).
Generators to write next, in fs-documentation: a component page DE+EN per set (belongs to check-docs next to gen_component_indexes), reading only `icons.toml`.

## 4. Sets as packages (description only, no store code touched)
Kind `icon-theme` next to `program` in the catalogue (`fs-catalog/packages.toml`). Example: `packaging/freesynergy.package.toml`: id `icon-theme-freesynergy`, kind, version 0.0.N, licence, `[content]` set/index/catalogue/install dir (`icons/FreeSynergy` under the XDG data dir), `[source]` repo, tag, asset `icon-theme-<id>-{version}.tar.gz` of `sets/<id>/`. Installation = unpack into the icon directory; no code runs. Sources follow ADR 0068; a signed own source for designers comes later (same signature as other assets). Each set is its own package with its own licence, so the user chooses what to install.
Gap: `fs-release/.github/workflows/release.yml` builds binaries only (kinds cli/daemon/app); a data kind (tarball of `sets/<id>`, signed, draft release) does not exist. Needs a decision and a change in fs-release; not done here. `release.yml` is therefore NOT added to this repo yet.

## 5. Proposals (nothing removed; decisions by Strategy)
1. **We10X (GPL-3.0)**: own set, own licence, not part of the FreeSynergy theme package. Recommendation: own repo/package (`fs-icons-we10x`) or drop. Reasons: copyleft in a repo whose root says MIT; 57 MB, 10510 files; Windows look; no licence text here today. If kept, it needs `COPYING` and upstream notice first.
2. **homarrlabs**: keep as a separate set, licence corrected to Apache-2.0 (+ licence text and NOTICE of upstream), with a line that logos belong to their owners. Before it enters `sets/`: remove or fix the 65 flagged files (script, foreignObject, external fonts, oversize) and decide whether brand logos are acceptable in a store (recommended: yes as "app logos for identification", reviewed with the ADR 0068 source rules). 36 MB is large for a package; consider a download-on-demand source instead of the repo.
3. **`FreeSynergy/` (legacy 62)**: do not ship as "FreeSynergy". Proof of origin is missing; our own 43 glyphs replace it. Keep the old directory until every name used by a program exists in `sets/freesynergy`, then remove.
4. **cursor-sets/midnight**: origin unknown; cursors are not icon-theme material. Keep out of the package until the origin is proven; probably an own repo later.
5. **Rust `sync/`, `Cargo.toml`/`Cargo.lock`, `.clippy.toml`, `rustfmt.toml`, `deny.toml`, `Containerfile`, `package.toml`, `setup.sh`, `.githooks`, `CLAUDE.md`, `ci.yml`**: what `sync` does is pull upstream SVGs blindly (no licence, no safety check, overwrites). Not needed for our own set. For third-party sets the better replacement is a small reviewed import script per set that writes `icons.toml` with licence and origin, followed by `check_svg.py`. Suggest removing the whole Rust part once homarrlabs/We10X are decided. `package.toml` and `Containerfile` still name homarrlabs/we10x (and a wrong path `we10x/`), so they are stale already. Not removed here; waiting for approval.
6. `README.md`, `manifest.toml`: rewrite after decisions 1-5 (currently wrong licence facts). `LICENSE` at the root: FreeSynergy usage is Apache-2.0 OR MIT (LICENSE-APACHE, LICENSE-MIT) in the migrated repos; this repo still has a single MIT file. Not changed yet.

## 6. Open points
- Themes use colour from the app: `currentColor` is not resolved by most toolkits for theme icons. Options: fixed colour plus `-symbolic` variants (GTK convention), or only FreeSynergy frontends read the set. Needs a decision.
- Size variants: only `scalable` for now (24 grid, MinSize 16, MaxSize 512). Pixel-hinted 16/22 sizes later if wanted.
- Which standard names the frontend agent wants for `purpose`/`used_in`: fill from his rebase.
- Release pipeline for data packages (section 4).
- Docs generator in fs-documentation (section 3).
