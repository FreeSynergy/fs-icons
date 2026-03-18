# FreeSynergy · Icons

**SVG icon sets for the FreeSynergy ecosystem**
by KalEl · Cyan + White

A curated collection of SVG icon sets, ready for use across all FreeSynergy programs.
Each set lives in its own directory. The `manifest.toml` describes available sets and their metadata.

## Structure

```
FreeSynergy.Icons/
  manifest.toml          # Registry of all available icon sets
  sync/                  # Rust binary: fsn-icons-sync (pulls from upstream sources)
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
| `homarrlabs` | Homarr Labs Dashboard Icons | [homarr-labs/dashboard-icons](https://github.com/homarr-labs/dashboard-icons) | MIT |

## Updating an Icon Set

Build and run `fsn-icons-sync` to pull the latest icons from upstream:

```bash
cargo run -p fsn-icons-sync               # sync all sets
cargo run -p fsn-icons-sync -- --set homarrlabs   # sync only homarrlabs
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

See [LICENSE](LICENSE). Individual icon sets retain their original licenses as documented in `manifest.toml`.
