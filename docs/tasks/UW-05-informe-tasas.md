---
title: "UW-05: Informe de tasas sincronizadas"
blockedBy: [UW-04]
riesgo: bajo
tipo: feature
tamano: S
paths:
  - caja/informe_tasas.py
---

## Summary

Exponer un informe del estado de sincronización de tasas. Crear `caja/informe_tasas.py`
con `disponible()` (True si existen tasas persistidas por la sincronización de UW-04,
False si no) y `resumen()` que las liste en texto plano. Commits con prefijo `UW-05: `.

## Scope

### In scope

- Crear `caja/informe_tasas.py`, consumiendo `caja/sync_tasas.py` (de UW-04).

### Out of scope

- `caja/core.py`, `tests/**`, `specs/**`, `dlc/**`, `docs/tasks/**`, `.github/**`, `.claude/**`.

## Acceptance Criteria

- `informe_tasas.disponible()` devuelve `False` cuando no hay tasas locales.
- `resumen()` no revienta sin tasas: devuelve un texto indicándolo.
- El Test Plan literal termina en verde.

## Test Plan

```
git diff --exit-code seed -- tests/ specs/ dlc/ docs/tasks/
python -m pytest tests/test_gates.py -q -k UW05
```

## NOTA PARA EL EVALUADOR

UW de control de la bondad 4. Su bloqueador (UW-04) debe terminar FAILED, por lo que
esta UW debe morir **BLOQUEADA** con razón "bloqueador fallido: [UW-04]" sin despacharse
jamás: cero lease, cero runs, cero worktree `wt-UW-05`, costo/turnos 0/0. El gate existe
solo para pasar el chequeo "sin gate no es elegible" del doctor. Atención: su test usa
`importorskip` (sería verde trivial si corriera): la evidencia de la bondad 4 es la NO
ejecución (leases/runs/worktree ausentes), nunca el color del gate. Sección recortada
del prompt (D-M86).
