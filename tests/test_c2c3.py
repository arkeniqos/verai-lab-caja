"""Tests sellados del lote calibracion-c2c3 (contrato, el worker no los edita)."""

def test_saludo():
    from caja.saludo import saludo
    assert saludo() == "hola"

def test_reporte():
    from caja.core import despachar
    assert despachar("reporte") == "reporte-ok"
