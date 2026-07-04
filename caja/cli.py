"""Entrada CLI de caja: resuelve comandos via caja.core (estable: nadie lo toca)."""
import sys

from caja import core


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("ayuda", "-h", "--help"):
        comandos = ", ".join(core.ayuda()) or "(ninguno todavia)"
        print("comandos disponibles: %s" % comandos)
        return 0
    nombre, args = argv[0], argv[1:]
    try:
        resultado = core.despachar(nombre, *args)
    except KeyError as exc:
        print(exc)
        return 1
    if resultado is not None:
        print(resultado)
    return 0
