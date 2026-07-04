"""Utilidades de texto de la caja (stdlib puro).

`longitud_media` DELEGA el promedio en caja.stats.media (UW-01): prohibido
reimplementar el cálculo del promedio acá.
"""
from caja import stats


def slug(frase):
    """Slug URL-friendly: minúsculas, palabras unidas por '-', solo alfanuméricos.

    Espacios múltiples y bordes se normalizan; dentro de cada palabra se
    conservan únicamente los caracteres alfanuméricos.
    """
    palabras = []
    for palabra in frase.lower().split():
        limpia = "".join(c for c in palabra if c.isalnum())
        if limpia:
            palabras.append(limpia)
    return "-".join(palabras)


def contar_palabras(frase):
    """Cantidad de palabras separadas por espacios ('' -> 0)."""
    return len(frase.split())


def longitud_media(frase):
    """Promedio de las longitudes de palabra, vía caja.stats.media."""
    longitudes = [len(palabra) for palabra in frase.split()]
    return stats.media(longitudes)
