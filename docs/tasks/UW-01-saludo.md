---
title: "UW-01: comando saludo"
blockedBy: []
riesgo: ninguna
tipo: CODIGO
tamano: S
paths:
  - caja/saludo.py
---
## Summary
Crear `caja/saludo.py` con `saludo()` que devuelve `"hola"`.

## Scope
### In scope
- Crear `caja/saludo.py` con la función `saludo()`.
### Out of scope
- `caja/core.py`, `tests/**`, `specs/**`, `dlc/**`, `docs/tasks/**`, `.github/**`.

## Acceptance Criteria
- `caja.saludo.saludo() == "hola"`.

## Test Plan
```
python -m pytest tests/test_c2c3.py -q -k test_saludo
```
