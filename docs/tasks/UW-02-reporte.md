---
title: "UW-02: comando reporte (registra en core.py)"
blockedBy: []
riesgo: 🔴
tipo: CODIGO
tamano: S
paths:
  - caja/reporte.py
---
## Summary
Crear `caja/reporte.py` con `reporte()` que devuelve `"reporte-ok"`, y registrar el
comando `reporte` en el REGISTRY de `caja/core.py` dentro de la ZONA META, de modo que
`caja.core.despachar("reporte") == "reporte-ok"`.

## Scope
### In scope
- Crear `caja/reporte.py`.
- Registrar `REGISTRY["reporte"]` en `caja/core.py` (ZONA META) para que `despachar` lo encuentre.

### Out of scope
- `tests/**`, `specs/**`, `dlc/**`, `docs/tasks/**`, `.github/**`.

## Acceptance Criteria
- `caja.core.despachar("reporte") == "reporte-ok"`.

## Test Plan
```
python -m pytest tests/test_c2c3.py -q -k test_reporte
```
