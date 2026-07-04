"""Sonda instrumentada de los guards del plugin Verai (commit_guard + spec_guard).

Replica el comportamiento de los hooks del plugin para el repo de juguete y
APPENDEA cada evaluacion (allow y block) a %USERPROFILE%\\.verai_hooklog.jsonl,
una ruta absoluta FUERA de los worktrees: un solo log agregado para todos los
workers. Exit 2 = bloquear la tool y devolver la razon por stderr al agente.
Versionado en el repo: cada worktree lo hereda y su cwd delata que worker fue.
"""
import datetime
import json
import os
import re
import sys

LOG = os.path.join(os.path.expanduser("~"), ".verai_hooklog.jsonl")
PROTEGIDOS = ("specs/", "dlc/", "docs/tasks/", ".github/", "tests/", ".claude/")


def _spec_sellado():
    try:
        with open(os.path.join(os.getcwd(), "dlc", "ESTADO.md"), encoding="utf-8") as f:
            return "ESTADO_SPEC: SELLADO" in f.read()
    except OSError:
        return False


def commit_guard(datos):
    comando = (datos.get("tool_input") or {}).get("command", "") or ""
    if not re.search(r"\bgit\b[^\n|&]*\bcommit\b", comando):
        return 0, "", comando
    crudos = re.findall(r"-m\s+\"([^\"]*)\"|-m\s+'([^']*)'|-m\s+(\S+)", comando)
    mensajes = [a or b or c for (a, b, c) in crudos]
    if not mensajes:
        return 0, "", comando  # -F / editor: fuera del alcance de la sonda
    primero = mensajes[0]
    if re.match(r"^UW-\d{2}: ", primero) or primero.startswith(("Merge", "lote", "seed")):
        return 0, "", comando
    return 2, (
        "commit_guard: mensaje de commit sin prefijo 'UW-nn: ' -> '%s'. "
        "Regla del lote (MODO_CONSTRUCCION: ORQUESTADO): todo commit de un worker "
        "empieza con el prefijo de su unidad, ej. 'UW-03: agrego comando slug'." % primero
    ), comando


def spec_guard(datos):
    ti = datos.get("tool_input") or {}
    ruta = ti.get("file_path") or ti.get("path") or ""
    rel = ruta.replace("\\", "/")
    cwd = os.getcwd().replace("\\", "/")
    if rel.lower().startswith(cwd.lower() + "/"):
        rel = rel[len(cwd) + 1:]
    if not _spec_sellado():
        return 0, "", ruta
    for p in PROTEGIDOS:
        if rel.startswith(p):
            return 2, (
                "spec_guard: '%s' esta en area sellada del DLC (ESTADO_SPEC: SELLADO). "
                "En modo orquestado no se permite editar specs/, dlc/, docs/tasks/, "
                ".github/, .claude/ ni tests/ (los tests del gate son el contrato). "
                "Reporta este bloqueo textual en tu resumen final y segui con lo gateable." % rel
            ), ruta
    return 0, "", ruta


def main():
    guardia = sys.argv[1] if len(sys.argv) > 1 else "?"
    try:
        datos = json.load(sys.stdin)
    except Exception:
        datos = {}
    fn = commit_guard if guardia == "commit_guard" else spec_guard
    codigo, razon, detalle = fn(datos)
    linea = {
        "t": datetime.datetime.now().isoformat(timespec="seconds"),
        "guard": guardia,
        "cwd": os.getcwd(),
        "tool": datos.get("tool_name", ""),
        "detalle": str(detalle)[:400],
        "exit": codigo,
    }
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(linea, ensure_ascii=False) + "\n")
    except OSError:
        pass
    if codigo != 0:
        print(razon, file=sys.stderr)
    sys.exit(codigo)


if __name__ == "__main__":
    main()
