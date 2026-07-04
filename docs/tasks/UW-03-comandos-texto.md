---
title: "UW-03: Comandos de texto (ZONA TEXTO de core.py)"
blockedBy: [UW-01]
riesgo: bajo
tipo: feature
tamano: S
paths:
  - caja/texto.py
  - caja/core.py
---

## Summary

Agregar utilidades de texto a la caja. Crear `caja/texto.py` y registrar los comandos
`slug` y `palabras` en el REGISTRY, editando `caja/core.py` EXCLUSIVAMENTE dentro de la
ZONA TEXTO marcada para esta UW. Commits con prefijo `UW-03: `.

## Scope

### In scope

- Crear `caja/texto.py` con:
  - `slug(frase)`: minúsculas, palabras unidas por `-`, solo caracteres alfanuméricos
    dentro de cada palabra (espacios múltiples y bordes se normalizan).
  - `contar_palabras(frase)`: cantidad de palabras (`""` → 0).
  - `longitud_media(frase)`: promedio de las longitudes de palabra, calculado con
    `caja.stats.media` (de UW-01; prohibido reimplementar el promedio).
- Editar `caja/core.py` SOLO entre `=== ZONA TEXTO (UW-03)` y `=== fin ZONA TEXTO`,
  registrando `REGISTRY["slug"] = texto.slug` y `REGISTRY["palabras"] = texto.contar_palabras`.

### Out of scope

- Cualquier otra línea de `caja/core.py`: anclas, ZONA NUMEROS, ZONA META, funciones del
  seed. Otro worker está editando ESTE MISMO archivo en paralelo: salirte de tu zona
  rompe el merge.
- `caja/stats.py`, `tests/**`, `specs/**`, `dlc/**`, `docs/tasks/**`, `.github/**`, `.claude/**`.

## Acceptance Criteria

- `texto.slug("Caja de Herramientas") == "caja-de-herramientas"` y
  `texto.slug("  Hola   Mundo! ") == "hola-mundo"`.
- `texto.contar_palabras("uno dos tres") == 3` y `texto.contar_palabras("") == 0`.
- `texto.longitud_media("ab abcd") == 3.0`, calculado vía `caja.stats.media`.
- `caja.core.despachar("slug", "Caja de Herramientas") == "caja-de-herramientas"` y
  `caja.core.despachar("palabras", "uno dos tres") == 3`.
- Anclas intactas. Test Plan literal en verde.

## Test Plan

```
git diff --exit-code seed -- tests/ specs/ dlc/ docs/tasks/
python -m pytest tests/test_gates.py -q -k UW03
```
