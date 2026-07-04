#!/usr/bin/env bash
set -e
R="arkeniqos/verai-lab-caja"
until [ "$(gh api repos/$R/commits/ci/review-turns/check-runs --jq '[.check_runs[] | select(.name=="dlc-guard" and .conclusion=="success")] | length')" -ge 1 ]; do sleep 6; done
gh pr merge 13 -R "$R" --merge
cd /c/dev/verai-worktrees/_integracion
git pull -q origin lote/calibracion-03 && git fetch -q origin master
git merge -q origin/master -m "lote calibracion-03: trae review a 30 turnos" && git push -q origin lote/calibracion-03
cd /c/dev/verai-worktrees/wt-UW-04
git commit -q --allow-empty -m "UW-04: retrigger review (30 turnos)" && git push -q origin uw-04-sync-tasas
SHA=$(git rev-parse HEAD)
echo "head nuevo: $SHA"
until [ "$(gh api repos/$R/commits/$SHA/check-runs --jq '[.check_runs[] | select(.status=="completed")] | length' 2>/dev/null)" -ge 2 ]; do sleep 15; done
gh api repos/$R/commits/$SHA/check-runs --jq '.check_runs[] | "\(.name): \(.conclusion)"'
echo "--- último comentario del PR 7 ---"
gh pr view 7 -R "$R" --json comments --jq '.comments[-1].body[0:800]'
