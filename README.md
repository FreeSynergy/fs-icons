# FreeSynergy · Icons

**SVG icon sets for the FreeSynergy ecosystem**
by KalEl · Cyan + White

A curated collection of SVG icon sets, ready for use across all FreeSynergy programs.
Each set lives in its own directory. The `manifest.toml` describes available sets and their metadata.

## Structure

```
sets/<id>/            icon-theme sets (freedesktop Icon Theme Specification); icons.toml is the data source
  freesynergy/        the FreeSynergy theme (drawn by the project)
FreeSynergy/          legacy logos of the owner (MIT OR Apache-2.0), not yet migrated
homarrlabs/           Homarr Labs Dashboard Icons (optional, Apache-2.0, trademark notice)
cursor-sets/          cursors (origin to be confirmed)
scripts/              gates.sh, check_svg.py, check_sets.py, gen_excluded.py, import_glyphs.py
manifest.toml         registry of the sets
docs/PLAN-revive.md   plan, inventory, decisions
```

## Icon Sets

| ID | Name | Source | License |
|---|---|---|---|
| `freesynergy-theme` | FreeSynergy theme (`sets/freesynergy/`) | drawn by the project | Apache-2.0 OR MIT |
| `freesynergy` | FreeSynergy logos (legacy, `FreeSynergy/`) | owner (KalEl) | MIT OR Apache-2.0 |
| `homarrlabs` | Homarr Labs Dashboard Icons (optional; logos are trademarks of their owners, for identification only) | [homarr-labs/dashboard-icons](https://github.com/homarr-labs/dashboard-icons) | Apache-2.0 (`homarrlabs/LICENSE`, `homarrlabs/NOTICE`) |

The We10X theme (GPL-3.0) was removed from this repository; it is no standard set. More free sets will be searched
for, or drawn by us (SVG, also with AI help).

## Checks

`scripts/gates.sh .` runs the script tests, `check_sets.py` (icons.toml against files, names, licences, index.theme)
and `check_svg.py` (no scripts, no external references, size limit) over `sets/`.

## Adding a Set

1. Create `sets/<id>/` with `icons.toml`, `index.theme`, `scalable/<context>/`, and the licence files of exactly this set.
2. Free licence only; write the origin into `[set]`.
3. Run `scripts/gates.sh .`.

## License

See [LICENSE](LICENSE). Individual icon sets retain their original licenses; each set directory carries its licence text and origin notice. The root `LICENSE` covers only files that carry no other notice. See `docs/PLAN-revive.md`.
