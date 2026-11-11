#!/usr/bin/env bash
# The one measure for this data repo; .github/workflows/check.yml runs exactly the same.
#   scripts/gates.sh <repo root>
# 1. unit tests of the scripts  2. icons.toml / index.theme / licences consistent  3. every SVG in sets/ safe.
# Legacy directories (homarrlabs, We10X, FreeSynergy, cursor-sets) are NOT gated yet: see docs/PLAN-revive.md.
set -euo pipefail
root="$(cd "$1" && pwd)"
cd "$root"
python3 -I -m unittest discover -s tests
python3 -I scripts/check_sets.py "$root"
python3 -I scripts/check_svg.py sets
echo "gates ok: $root at $(git rev-parse --short HEAD 2>/dev/null || echo untracked)"
