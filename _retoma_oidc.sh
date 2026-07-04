#!/usr/bin/env bash
set -e
R="arkeniqos/verai-lab-caja"
JQ_GUARD='[.check_runs[] | select(.name=="dlc-guard" and .conclusion=="success")] | length'
JQ_DONE='[.check_runs[] | select(.status=="completed")] | length'
JQ_ALL='.check_runs[] | "\(.name): \(.conclusion)"'
until [ "$(gh api repos/$R/commits/ci/oidc-permission/check-runs --jq "$JQ_GUARD")" -ge 1 ]; do sleep 6; done
gh pr merge 12 -R "$R" --merge
cd /c/dev/verai-worktrees/_integracion
git pull -q origin lote/calibracion-03 && git fetch -q origin master
git merge -q origin/master -m "lote calibracion-03: trae fix OIDC" && git push -q origin lote/calibracion-03
cd /c/dev/verai-worktrees/wt-UW-04
git commit -q --allow-empty -m "UW-04: retrigger review (OIDC)" && git push -q origin uw-04-sync-tasas
SHA=$(git rev-parse HEAD)
echo "head nuevo: $SHA"
until [ "$(gh api repos/$R/commits/$SHA/check-runs --jq "$JQ_DONE" 2>/dev/null)" -ge 2 ]; do sleep 10; done
gh api repos/$R/commits/$SHA/check-runs --jq "$JQ_ALL"
