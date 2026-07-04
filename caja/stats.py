"""Estadisticas basicas de la caja (stdlib puro, sin efectos al importar)."""


def media(valores):
    """Promedio aritmetico (float) de una lista de numeros."""
    return sum(valores) / len(valores)


def mediana(valores):
    """Mediana; con cantidad par, promedio de los dos centrales."""
    ordenados = sorted(valores)
    n = len(ordenados)
    medio = n // 2
    if n % 2 == 1:
        return ordenados[medio]
    return (ordenados[medio - 1] + ordenados[medio]) / 2


def rango(valores):
    """Diferencia entre el maximo y el minimo."""
    return max(valores) - min(valores)
