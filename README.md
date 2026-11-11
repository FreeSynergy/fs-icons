# FreeSynergy · Icons

**SVG icon sets for the FreeSynergy ecosystem**
by KalEl · Cyan + White

A curated collection of SVG icon sets, ready for use across all FreeSynergy programs.
Each set lives in its own directory. The `manifest.toml` describes available sets and their metadata.

## Structure

```
FreeSynergy.Icons/
  manifest.toml          # Registry of all available icon sets
  sync/                  # Rust binary: fs-icons-sync (pulls from upstream sources)
  gallery/               # Rust binary: icon browser and picker (coming soon)
  homarrlabs/            # Homarr Labs Dashboard Icons
    icon-name.svg
    icon-name-dark.svg
    ...
  (further sets in their own directories)
```

## Icon Sets

| ID | Name | Source | License |
|---|---|---|---|
| `homarrlabs` | Homarr Labs Dashboard Icons (optional; logos are trademarks of their owners, for identification only) | [homarr-labs/dashboard-icons](https://github.com/homarr-labs/dashboard-icons) | Apache-2.0 (`homarrlabs/LICENSE`, `homarrlabs/NOTICE`) |
| `we10x` | We10X icon theme (optional, own licence, not part of the default theme) | [yeyushengfan258/We10X-icon-theme](https://github.com/yeyushengfan258/We10X-icon-theme) | GPL-3.0 (`We10X/COPYING`, `We10X/NOTICE.md`) |
| `freesynergy` | FreeSynergy theme (new, in `sets/freesynergy/`) | drawn by the project | Apache-2.0 OR MIT |

## Updating an Icon Set

Build and run `fs-icons-sync` to pull the latest icons from upstream:

```bash
cargo run -p fs-icons-sync               # sync all sets
cargo run -p fs-icons-sync -- --set homarrlabs   # sync only homarrlabs
```

## Adding New Sets

1. Create a directory with the set ID as name (e.g., `simpleicons/`)
2. Add SVG files — use `name.svg` for light and `name-dark.svg` for dark variants
3. Add a `[[set]]` entry in `manifest.toml`
4. Add a sync script in `scripts/` if the set has an upstream source

## Gallery

The `gallery/` program lets you browse and select icons interactively.
It reads `manifest.toml` and can be embedded anywhere an icon picker is needed.

## License

See [LICENSE](LICENSE). Individual icon sets retain their original licenses; each set directory carries its licence text and origin notice. The root `LICENSE` covers only files that carry no other notice. See `docs/PLAN-revive.md`.
