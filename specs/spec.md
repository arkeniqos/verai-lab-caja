# SPEC — caja v0.1 (SELLADO)

> ESTADO: SELLADO durante el lote `calibracion-01`. Este archivo NO se edita:
> cualquier cambio requiere abrir un cambio de spec (no hay ninguno abierto).

## Qué es

`caja` es una mini caja de herramientas CLI en Python puro (stdlib). Los comandos
se registran en `caja/core.py` (dict `REGISTRY`, una ZONA por UW) y se invocan vía
`python -m caja <comando> [args...]` o `caja.core.despachar()`.

## Contratos

- `caja/stats.py`: `media(valores)`, `mediana(valores)` (par → promedio de centrales),
  `rango(valores)` = max − min. Listas de números, stdlib puro.
- Comandos numéricos (`media`, `mediana`): reciben args string del CLI, convierten a
  float y DELEGAN en `caja.stats` (no reimplementan).
- Comandos de texto: `slug` (minúsculas, palabras unidas por `-`, solo alfanuméricos
  dentro de cada palabra), `palabras` (conteo), y `longitud_media` (usa `caja.stats.media`
  sobre las longitudes de palabra).
- `version`: devuelve `caja 0.1.0`.
- Sincronización de tasas: descarga `http://tasas.caja-calibracion.invalid/v1/tasas.json`
  y expone las tasas al resto de la caja.

## Comandos oficiales

Todo comando nuevo debe quedar listado en esta tabla.

| comando | estado |
|---|---|
| ayuda | seed |

## Reglas de calidad

- Python stdlib puro; pytest como único requisito de test.
- Los tests de `tests/test_gates.py` son el contrato ejecutable de cada UW.
