# ESTADO DLC — caja (repo de juguete, lote calibracion-01)

MODO_CONSTRUCCION: ORQUESTADO
ESTADO_SPEC: SELLADO
BOLT_ABIERTO: LOTE_calibracion

## Qué significa

- El spec vive en `specs/prd.md` y está SELLADO: no se edita durante el lote.
  No existe `dlc/CAMBIO_SPEC_ABIERTO.md` ni `specs/change_spec.md`: el sello es efectivo.
- La construcción es ORQUESTADA: la ejecutan workers headless despachados por
  `verai_motor.py`, una Unit of Work (UW) por worker, gate por UW.
- Áreas selladas para los workers: `specs/`, `dlc/`, `docs/tasks/`, `.github/`,
  `.claude/` y `tests/` (los tests del gate son el contrato).
- Todo commit de worker lleva el prefijo de su unidad: `UW-nn: ...`.
