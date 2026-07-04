---
title: "UW-02: Comandos numéricos (ZONA NUMEROS de core.py)"
blockedBy: [UW-01]
riesgo: bajo
tipo: feature
tamano: S
paths:
  - caja/comandos_num.py
  - caja/core.py
---

## Summary

Exponer las estadísticas de `caja.stats` (construidas por UW-01) como comandos del CLI.
Crear `caja/comandos_num.py` y registrar los comandos `media` y `mediana` en el REGISTRY,
editando `caja/core.py` EXCLUSIVAMENTE dentro de la ZONA NUMEROS marcada para esta UW.
Commits con prefijo `UW-02: `.

## Scope

### In scope

- Crear `caja/comandos_num.py` con:
  - `cmd_media(*args)`: convierte cada arg string a float y DELEGA en `caja.stats.media`.
  - `cmd_mediana(*args)`: ídem con `caja.stats.mediana`.
  - Prohibido reimplementar los cálculos: se importan de `caja.stats`.
- Editar `caja/core.py` SOLO entre las líneas `=== ZONA NUMEROS (UW-02)` y
  `=== fin ZONA NUMEROS`, registrando `REGISTRY["media"]` y `REGISTRY["mediana"]`.

### Out of scope

- Cualquier otra línea de `caja/core.py`: anclas `_ancla_*`, ZONA TEXTO, ZONA META,
  funciones del seed. Otro worker está editando ESTE MISMO archivo en paralelo:
  salirte de tu zona rompe el merge.
- `caja/stats.py` (es de UW-01), `tests/**`, `specs/**`, `dlc/**`, `docs/tasks/**`,
  `.github/**`, `.claude/**`.

## Acceptance Criteria

- `caja.core.despachar("media", "1", "2", "3", "4") == 2.5`
- `caja.core.despachar("mediana", "7", "1", "3") == 3`
- `caja/comandos_num.py` importa y usa `caja.stats` (el gate lo verifica por fuente).
- Las anclas `_ancla_a/_ancla_b/_ancla_c` siguen intactas.
- El Test Plan literal termina en verde.

## Test Plan

```
git diff --exit-code seed -- tests/ specs/ dlc/ docs/tasks/
python -m pytest tests/test_gates.py -q -k UW02
```
