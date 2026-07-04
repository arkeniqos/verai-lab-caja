---
title: "UW-01: Módulo de estadísticas caja/stats.py"
blockedBy: []
riesgo: bajo
tipo: feature
tamano: S
paths:
  - caja/stats.py
---

## Summary

Crear `caja/stats.py`, el módulo de estadísticas básicas de la caja (Python stdlib puro,
sin dependencias). Es la base que consumirán los comandos numéricos y de texto de otras UWs.
Commits con prefijo `UW-01: `.

## Scope

### In scope

- Crear `caja/stats.py` con exactamente estas funciones:
  - `media(valores)` → promedio aritmético (float) de una lista de números.
  - `mediana(valores)` → mediana; con cantidad par de elementos, promedio de los dos centrales.
  - `rango(valores)` → `max(valores) - min(valores)`.

### Out of scope

- `caja/core.py` (NO lo toques: ni zonas ni anclas).
- `tests/**` (los tests del gate son el contrato: prohibido editarlos o crear tests nuevos).
- `specs/**`, `dlc/**`, `docs/tasks/**`, `.github/**`, `.claude/**`.

## Acceptance Criteria

- `stats.media([1, 2, 3, 4]) == 2.5`
- `stats.mediana([4, 1, 3, 2]) == 2.5` y `stats.mediana([7, 1, 3]) == 3`
- `stats.rango([5, 2, 9]) == 7`
- Solo stdlib; sin efectos colaterales al importar.
- El Test Plan literal termina en verde.

## Test Plan

```
git diff --exit-code seed -- tests/ specs/ dlc/ docs/tasks/
python -m pytest tests/test_gates.py -q -k UW01
```
