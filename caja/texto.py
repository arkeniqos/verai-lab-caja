"""Utilidades de texto de la caja (stdlib puro, sin efectos al importar)."""

from caja import stats


def slug(frase):
    """Convierte `frase` en un slug: minusculas, palabras unidas por '-',
    conservando solo caracteres alfanumericos dentro de cada palabra."""
    palabras = []
    for palabra in frase.split():
        limpia = "".join(c for c in palabra if c.isalnum()).lower()
        if limpia:
            palabras.append(limpia)
    return "-".join(palabras)


def contar_palabras(frase):
    """Cantidad de palabras en `frase` ('' -> 0)."""
    return len(frase.split())


def longitud_media(frase):
    """Promedio de las longitudes de palabra, via caja.stats.media."""
    return stats.media([len(palabra) for palabra in frase.split()])
