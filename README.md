# caja

Mini caja de herramientas CLI en Python puro (stdlib). Repo de juguete para la
calibración local del motor de orquestación de Verai (lote `calibracion-01`).

- Tests: `python -m pytest tests -q` (el motor exporta `PYTHONUTF8=1`).
- CLI: `python -m caja ayuda` — los comandos se registran en `caja/core.py` (REGISTRY).
- Los gates de cada UW viven SELLADOS en `tests/test_gates.py`.
