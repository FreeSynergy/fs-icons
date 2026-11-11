# CLAUDE.md – fs-icons

## What is this?

FreeSynergy Icons: SVG icon sets (data, no program). `sets/freesynergy/` is the FreeSynergy icon theme
(freedesktop Icon Theme Specification); `FreeSynergy/` holds the owner's legacy logos; `homarrlabs/` is an optional
third-party set (Apache-2.0, trademark notice). Plan and decisions: `docs/PLAN-revive.md`.

## Rules

- Language in files: **English**. Language in chat: **German**.
- One data source per set: `sets/<id>/icons.toml`. Docs are generated from it.
- Free licences only; every set carries its own licence text and origin.
- Third-party files are never edited; unsafe ones are excluded and listed (`EXCLUDED.md`).
- No CHANGELOG.md. After every feature: commit directly.

## Quality gate (before every commit)

```
scripts/gates.sh .
```
