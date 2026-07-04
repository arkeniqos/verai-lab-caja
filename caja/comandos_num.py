"""Comandos numéricos del CLI: delegan en caja.stats (UW-01)."""

from caja import stats


def cmd_media(*args):
    """Convierte cada arg a float y delega el promedio en caja.stats.media."""
    valores = [float(a) for a in args]
    return stats.media(valores)


def cmd_mediana(*args):
    """Convierte cada arg a float y delega la mediana en caja.stats.mediana."""
    valores = [float(a) for a in args]
    return stats.mediana(valores)
