#!/usr/bin/env python3
"""scope_check — eje SCOPE determinista del mergeability scorecard de Verai (C2, D-M100).

Verifica `diff ⊆ paths:` sellados en la ficha UW. Es el único eje con dientes: corre
como paso requerido en dlc-guard (branch protection). Lee `paths:` SOLO de la rama BASE
(intocable), nunca de HEAD. stdlib puro (misma disciplina que verai_motor.py).

Semántica (D-M100):
  - PASA  (exit 0): todos los archivos del diff ⊆ ∪ globs(paths).
  - N/A   (exit 0): branch que no matchea uw-nn (modo mob u otro flujo) — no aplica.
  - FALLA (exit 1): hay archivos fuera de contrato; O la ficha uw-nn no trae `paths:`
    (fail-loud, no fail-open); O trae paths:["**"] sin `scope_waiver` humano.

Uso:
  scope_check.py --repo . --branch uw-02-x --base <sha> --head <sha>   # CI (dlc-guard)
  scope_check.py --repo . --uw UW-02 --files-from lista.txt            # medición / test
"""
import argparse
import os
import re
import subprocess
import sys

PASA, FALLA, NA = "PASA", "FALLA", "N/A"


# ── Matcher de globs (*, **, ?) sin dependencias ────────────────────────────────
def glob_a_regex(glob):
    """Traduce un glob estilo gitignore a regex. `**` cruza `/`; `*` no; `?` = 1 char."""
    i, out = 0, ["^"]
    while i < len(glob):
        c = glob[i]
        if c == "*":
            if glob[i + 1:i + 2] == "*":          # ** → cualquier cosa, incluido /
                out.append(".*")
                i += 2
                if glob[i:i + 1] == "/":          # **/  → absorbe el separador
                    i += 1
                continue
            out.append("[^/]*")                    # * → cualquier cosa menos /
        elif c == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(c))
        i += 1
    out.append("$")
    return "".join(out)


def matchea(archivo, patrones):
    a = archivo.replace("\\", "/").lstrip("./")
    return any(re.match(glob_a_regex(p.strip().replace("\\", "/").lstrip("./")), a) for p in patrones)


# ── Front matter: parseo de `paths:` (bloque o inline) y `scope_waiver` ──────────
def parsear_ficha(texto):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, re.S)
    fm = m.group(1) if m else texto
    lineas = fm.splitlines()
    paths, waiver = None, None
    i = 0
    while i < len(lineas):
        ln = lineas[i]
        mi = re.match(r"^paths:\s*(.*)$", ln)
        if mi:
            resto = mi.group(1).strip()
            if resto.startswith("["):              # inline: paths: [a, b]
                paths = [x.strip().strip("\"'") for x in resto.strip("[]").split(",") if x.strip()]
            else:                                   # bloque:  paths:\n  - a\n  - b
                paths = []
                j = i + 1
                while j < len(lineas) and re.match(r"^\s*-\s+\S", lineas[j]):
                    paths.append(re.sub(r"^\s*-\s+", "", lineas[j]).strip().strip("\"'"))
                    j += 1
                i = j - 1
        mw = re.match(r"^scope_waiver:\s*(.+)$", ln)
        if mw:
            waiver = mw.group(1).strip().strip("\"'")
        i += 1
    return paths, waiver


# ── Núcleo puro (testeable sin git) ─────────────────────────────────────────────
def evaluar(paths, waiver, diff_files):
    if paths is None:
        return FALLA, "ficha `uw-nn` SIN `paths:` sellado — fail-loud (D-M100). El router "\
                      "debe sellar `paths:` en la ficha base; si la UW toca todo a propósito, "\
                      "usá `paths: [\"**\"]` + `scope_waiver: <razón> — <quién>`."
    if [p.strip() for p in paths] == ["**"]:
        if not waiver:
            return FALLA, 'paths: ["**"] sin `scope_waiver` humano — un comodín de scope '\
                          'requiere aprobación humana explícita (D-M100).'
        return PASA, f'scope waiveado a propósito (`scope_waiver: {waiver}`) — {len(diff_files)} archivo(s), sin límite.'
    fuera = [f for f in diff_files if not matchea(f, paths)]
    if fuera:
        return FALLA, "fuera de contrato (∉ paths sellados): " + ", ".join(fuera) + \
                      "  · si es legítimo, el router extiende `paths:` en la ficha base"
    return PASA, f"{len(diff_files)} archivo(s) ⊆ paths sellados (no implica aislamiento intra-archivo)"


# ── Adaptadores git ──────────────────────────────────────────────────────────────
def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} → {r.returncode}: {r.stderr.strip()[:300]}")
    return r.stdout


def uw_de_branch(branch):
    m = re.match(r"^(uw-\d+)", branch, re.I)
    return m.group(1).upper() if m else None


def nombre_ficha(repo, uw, ref=None, tasks_dir="docs/tasks"):
    if ref:
        listado = git(repo, "ls-tree", "--name-only", "-r", ref, f"{tasks_dir}/").splitlines()
    else:
        listado = [f"{tasks_dir}/{f}" for f in os.listdir(os.path.join(repo, tasks_dir))]
    for p in listado:
        if re.match(rf"^{re.escape(uw)}[-.]", os.path.basename(p).upper()):
            return p
    return None


def leer_ficha(repo, uw, ref, tasks_dir):
    ficha = nombre_ficha(repo, uw, ref, tasks_dir)
    if not ficha:
        raise FileNotFoundError(f"no encuentro la ficha de {uw} en {tasks_dir} (ref={ref or 'working tree'})")
    if ref:
        return git(repo, "show", f"{ref}:{ficha}"), ficha
    return open(os.path.join(repo, ficha), encoding="utf-8").read(), ficha


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--tasks-dir", default="docs/tasks")
    ap.add_argument("--branch", help="rama del PR (deriva la UW); si no matchea uw-nn → N/A")
    ap.add_argument("--uw", help="UW explícita (para medición/test)")
    ap.add_argument("--base", help="SHA base (se lee `paths:` de acá — sellado)")
    ap.add_argument("--head", help="SHA head (se computa el diff base..head)")
    ap.add_argument("--files-from", help="archivo con la lista de archivos del diff (uno por línea) — modo test")
    args = ap.parse_args()
    repo = os.path.abspath(args.repo)

    uw = args.uw
    if not uw and args.branch:
        uw = uw_de_branch(args.branch)
        if not uw:
            print(f"scope: {NA} — branch '{args.branch}' no es uw-nn (modo mob u otro flujo)")
            return 0
    if not uw:
        print("scope: error — indicá --uw o --branch")
        return 2

    # `paths:` SIEMPRE de BASE (sellado); working tree solo en modo test sin --base
    ref = args.base
    texto, ficha = leer_ficha(repo, uw, ref, args.tasks_dir)
    paths, waiver = parsear_ficha(texto)

    if args.files_from:
        diff_files = [l.strip() for l in open(args.files_from, encoding="utf-8") if l.strip()]
    elif args.base and args.head:
        diff_files = [l for l in git(repo, "diff", "--name-only", args.base, args.head).splitlines() if l]
    else:
        print("scope: error — indicá --files-from, o --base y --head")
        return 2

    verdicto, detalle = evaluar(paths, waiver, diff_files)
    icono = {PASA: "✅", FALLA: "❌", NA: "➖"}[verdicto]
    print(f"scope [{uw}] ({ficha}): {icono} {verdicto} — {detalle}")
    return 0 if verdicto in (PASA, NA) else 1


if __name__ == "__main__":
    sys.exit(main())
