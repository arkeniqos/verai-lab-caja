"""Nucleo de despacho de caja.

REGISTRY mapea nombre de comando -> funcion. Cada UW registra sus comandos
SOLO dentro de su ZONA marcada. Las funciones _ancla_* son separadores
estables del seed: NO TOCAR (garantizan merges de 3 vias limpios).
"""

REGISTRY = {}


def despachar(nombre, *args, **kwargs):
    """Ejecuta el comando registrado bajo `nombre`."""
    if nombre not in REGISTRY:
        raise KeyError("comando desconocido: %s (proba 'ayuda')" % nombre)
    return REGISTRY[nombre](*args, **kwargs)


def ayuda():
    """Lista ordenada de comandos registrados."""
    return sorted(REGISTRY)


def _ancla_a():
    """Ancla estable del seed. NO TOCAR: separa la cabecera de la ZONA NUMEROS."""
    return "a"


# ==================================================================
# === ZONA NUMEROS (UW-02) =========================================
# UW-02 registra sus comandos SOLO entre esta linea y el marcador
# "fin ZONA NUMEROS". Ningun otro worker toca esta zona.
# Patron:
#   from caja import comandos_num
#   REGISTRY["media"] = comandos_num.cmd_media
from caja import comandos_num
REGISTRY["media"] = comandos_num.cmd_media
REGISTRY["mediana"] = comandos_num.cmd_mediana
# === fin ZONA NUMEROS =============================================
# ==================================================================


def _ancla_b():
    """Ancla estable del seed. NO TOCAR: separa ZONA NUMEROS de ZONA TEXTO."""
    return "b"


# ==================================================================
# === ZONA TEXTO (UW-03) ===========================================
# UW-03 registra sus comandos SOLO entre esta linea y el marcador
# "fin ZONA TEXTO". Ningun otro worker toca esta zona.
from caja import texto
REGISTRY["slug"] = texto.slug
REGISTRY["palabras"] = texto.contar_palabras
# === fin ZONA TEXTO ===============================================
# ==================================================================


def _ancla_c():
    """Ancla estable del seed. NO TOCAR: separa ZONA TEXTO de ZONA META."""
    return "c"


# ==================================================================
# === ZONA META (UW-06) ============================================
# UW-06 registra sus comandos SOLO entre esta linea y el marcador
# "fin ZONA META". Ningun otro worker toca esta zona.
# === fin ZONA META ================================================
# ==================================================================
