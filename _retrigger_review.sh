#!/usr/bin/env bash
set -e
R="arkeniqos/verai-lab-caja"
cd /c/dev/verai-worktrees/wt-UW-04
git commit -q --allow-empty -m "UW-04: retrigger review (App instalada)" && git push -q origin uw-04-sync-tasas
SHA=$(git rev-parse HEAD)
echo "head nuevo: $SHA"
until [ "$(gh api repos/$R/commits/$SHA/check-runs --jq '[.check_runs[] | select(.status=="completed")] | length' 2>/dev/null)" -ge 2 ]; do sleep 10; done
gh api repos/$R/commits/$SHA/check-runs --jq '.check_runs[] | "\(.name): \(.conclusion)"'
echo "--- último comentario del PR 7 ---"
gh pr view 7 -R "$R" --json comments --jq '.comments[-1].body[0:600]'
