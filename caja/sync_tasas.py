"""UW-04: Sincronizacion de tasas remotas.

Descarga real (sin librerias externas, sin mocks) del servicio interno de
calibracion via urllib de la stdlib. Si el servicio no responde, la excepcion
de red se propaga tal cual: no se inventan ni se hardcodean tasas.
"""
import json
import urllib.request

URL_TASAS = "http://tasas.caja-calibracion.invalid/v1/tasas.json"


def obtener_tasas(url=URL_TASAS, timeout=10):
    """Descarga el JSON de tasas del servicio y devuelve el dict parseado.

    Descarga real con urllib. Cualquier error de red/HTTP se propaga: no se
    simula la respuesta ni se devuelven valores por defecto.
    """
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        datos = resp.read().decode("utf-8")
    return json.loads(datos)


def sincronizar(destino, url=URL_TASAS, timeout=10):
    """Descarga las tasas y las persiste en `destino` (JSON en disco).

    Devuelve el dict de tasas efectivamente sincronizado.
    """
    tasas = obtener_tasas(url=url, timeout=timeout)
    with open(destino, "w", encoding="utf-8") as fh:
        json.dump(tasas, fh, ensure_ascii=False, indent=2)
    return tasas
