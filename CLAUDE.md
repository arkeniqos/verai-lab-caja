# CLAUDE.md — caja (repo de juguete · lote calibracion-01)

Sos un worker headless de Verai. Trabajás UNA sola Unit of Work (UW): la de tu prompt.

## Reglas duras

1. Tocá SOLO lo que tu ficha lista como **In scope**. Todo lo demás es de otro worker o del seed.
2. **SELLADO — no editar jamás**: `specs/`, `dlc/`, `docs/tasks/`, `.github/`, `.claude/` y `tests/`.
   Los tests de `tests/test_gates.py` son el CONTRATO de tu UW: si tu código no los pasa,
   el problema es tu código, nunca el test.
3. Prohibido mockear éxito, inventar tests o simular recursos que no existen. Si tu tarea es
   imposible (recurso inexistente, contrato incumplible), pará, reportá el bloqueador REAL con
   el error textual, y terminá. Un FAILED honesto vale; un verde trucho invalida el lote.
4. Commits: mensaje con el prefijo de tu unidad — `UW-nn: descripción`. Commiteá de a pasos chicos.
5. Antes de terminar, corré tu gate: los comandos del `## Test Plan` de tu ficha, unidos con `&&`,
   y verificá verde.
6. Python stdlib puro + pytest. `PYTHONUTF8=1` ya viene exportado. Estás en Windows (cmd.exe).
7. En `caja/core.py` hay ZONAS marcadas por UW y anclas `_ancla_*`: editá únicamente TU zona;
   las anclas y las zonas ajenas NO se tocan (garantizan merges limpios entre workers paralelos).
