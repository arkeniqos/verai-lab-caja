#!/usr/bin/env bash
set -e
R="arkeniqos/verai-lab-caja"
cd /c/dev/verai-lab-caja
git checkout -q master && git pull -q origin master
git checkout -qb ci/sticky-comment
python - <<'EOF'
ANCLA = "claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}"
NUEVO = ANCLA + "\n          use_sticky_comment: true  # el veredicto DEBE ser visible en el PR"
for p in [r'.github/workflows/claude-review.yml', r'C:/Users/avich/OneDrive - GENUINE LAB/Documents/AUDIO/spec-dlc/plugins/verai/skills/dlc-orquesta-ops/assets/claude-review.yml']:
    s = open(p, encoding='utf-8').read()
    assert ANCLA in s and "use_sticky_comment" not in s, p
    open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(ANCLA, NUEVO))
print('ok sticky agregado')
EOF
git add .github && git -c user.email=lab@verai -c user.name=lab commit -qm "ci: use_sticky_comment true — veredicto del review visible en el PR"
git push -qu origin ci/sticky-comment
gh pr create --title "ci: veredicto del review visible (sticky comment)" --body "El run quedaba verde sin publicar el veredicto." --base master > /dev/null
git checkout -q master
N=$(gh pr list --state open --head ci/sticky-comment --json number --jq '.[0].number')
until [ "$(gh api repos/$R/commits/ci/sticky-comment/check-runs --jq '[.check_runs[] | select(.name=="dlc-guard" and .conclusion=="success")] | length')" -ge 1 ]; do sleep 6; done
gh pr merge $N -R "$R" --merge
cd /c/dev/verai-worktrees/_integracion
git pull -q origin lote/calibracion-03 && git fetch -q origin master
git merge -q origin/master -m "lote calibracion-03: trae sticky comment" && git push -q origin lote/calibracion-03
cd /c/dev/verai-worktrees/wt-UW-04
git commit -q --allow-empty -m "UW-04: retrigger review (sticky)" && git push -q origin uw-04-sync-tasas
SHA=$(git rev-parse HEAD)
echo "head nuevo: $SHA"
until [ "$(gh api repos/$R/commits/$SHA/check-runs --jq '[.check_runs[] | select(.status=="completed")] | length' 2>/dev/null)" -ge 2 ]; do sleep 15; done
gh api repos/$R/commits/$SHA/check-runs --jq '.check_runs[] | "\(.name): \(.conclusion)"'
echo "--- comentarios en PR 7: $(gh api repos/$R/issues/7/comments --jq 'length')"
gh api repos/$R/issues/7/comments --jq '.[-1].body[0:900]' 2>/dev/null
