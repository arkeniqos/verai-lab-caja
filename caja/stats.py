"""Estadísticas básicas de la caja (stdlib puro, sin dependencias)."""


def media(valores):
    """Promedio aritmético (float) de una lista de números."""
    return sum(valores) / len(valores)


def mediana(valores):
    """Mediana; con cantidad par de elementos, promedio de los dos centrales."""
    ordenados = sorted(valores)
    n = len(ordenados)
    medio = n // 2
    if n % 2 == 1:
        return ordenados[medio]
    return (ordenados[medio - 1] + ordenados[medio]) / 2


def rango(valores):
    """Diferencia entre el máximo y el mínimo."""
    return max(valores) - min(valores)
