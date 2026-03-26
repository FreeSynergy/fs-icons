# CLAUDE.md – fs-icons

## What is this?

FreeSynergy Icons — curated SVG icon sets for the FreeSynergy desktop.
Contains icon directories (homarrlabs, we10x) and a `sync` binary that
pulls the latest SVGs from upstream sources without requiring system git.

## Rules

- Language in files: **English** (comments, code, variable names)
- Language in chat: **German**
- OOP everywhere: traits over match blocks, types carry their own behavior
- No CHANGELOG.md
- After every feature: commit directly

## Quality Gates (before every commit)

```
cargo clippy --all-targets -- -D warnings
cargo fmt --check
cargo test
```

Every lib.rs / main.rs must have:
```rust
#![deny(clippy::all, clippy::pedantic, warnings)]
```

## Architecture

- `sync/` — workspace member binary `fs-icons-sync`
  - `clone_shallow` — depth=1 gix clone, no system git required
  - `sync_homarrlabs` — copies SVGs from `dashboard-icons/svg/`
  - `sync_we10x` — recursively copies SVGs from `We10X-icon-theme/src/`
- `homarrlabs/` — app/service icons (dashboard-icons upstream)
- `we10x/` — system icons (We10X-icon-theme upstream)

## Dependencies

- `gix =0.80` (blocking HTTP transport, worktree mutation)
- `clap =4` (derive feature)
- `tempfile` (temporary clone directories)
