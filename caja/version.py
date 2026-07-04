"""Versión de la caja (stdlib puro).

`VERSION` es la versión semántica del paquete; `version()` la formatea como
etiqueta legible para el comando `version` del REGISTRY.
"""

VERSION = "0.1.0"


def version():
    """Etiqueta legible de versión: 'caja <VERSION>'."""
    return "caja %s" % VERSION
