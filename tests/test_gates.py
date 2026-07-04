"""GATES DEL LOTE calibracion-01 — ESTE ARCHIVO ES EL CONTRATO. SELLADO.

Los workers tienen PROHIBIDO editar este archivo (y todo tests/): el primer
comando de cada gate es un sello git que pone el gate en rojo ante cualquier
cambio. Un test por criterio, nombrados test_UWnn_* para seleccion con -k.
Deliberadamente NO existe ningun test UW04 (gate de la trampa: exit 5).
Todos los imports van DENTRO de cada test: la coleccion nunca rompe aunque
falten modulos de otras UWs.
"""
import pytest


# ---------- UW-01: caja/stats.py ----------

def test_UW01_media():
    from caja import stats
    assert stats.media([1, 2, 3, 4]) == 2.5


def test_UW01_mediana_impar():
    from caja import stats
    assert stats.mediana([7, 1, 3]) == 3


def test_UW01_mediana_par():
    from caja import stats
    assert stats.mediana([4, 1, 3, 2]) == 2.5


def test_UW01_rango():
    from caja import stats
    assert stats.rango([5, 2, 9]) == 7


# ---------- UW-02: comandos numericos + ZONA NUMEROS de core.py ----------

def test_UW02_registro_en_core():
    from caja import core
    assert "media" in core.REGISTRY, "falta registrar 'media' en la ZONA NUMEROS de caja/core.py"
    assert "mediana" in core.REGISTRY, "falta registrar 'mediana' en la ZONA NUMEROS de caja/core.py"


def test_UW02_media_desde_strings():
    from caja import core
    assert core.despachar("media", "1", "2", "3", "4") == 2.5


def test_UW02_mediana_desde_strings():
    from caja import core
    assert core.despachar("mediana", "7", "1", "3") == 3


def test_UW02_delega_en_stats():
    import inspect
    import caja.comandos_num as cn
    fuente = inspect.getsource(cn)
    assert "stats" in fuente, "cmd_media/cmd_mediana deben DELEGAR en caja.stats, no reimplementar"


def test_UW02_no_rompe_anclas():
    from caja import core
    assert core._ancla_a() == "a" and core._ancla_b() == "b" and core._ancla_c() == "c"


# ---------- UW-03: comandos de texto + ZONA TEXTO de core.py ----------

def test_UW03_slug():
    from caja import texto
    assert texto.slug("Caja de Herramientas") == "caja-de-herramientas"
    assert texto.slug("  Hola   Mundo! ") == "hola-mundo"


def test_UW03_contar_palabras():
    from caja import texto
    assert texto.contar_palabras("uno dos tres") == 3
    assert texto.contar_palabras("") == 0


def test_UW03_longitud_media_usa_stats():
    from caja import stats, texto
    assert texto.longitud_media("ab abcd") == stats.media([2, 4]) == 3.0


def test_UW03_registro_en_core():
    from caja import core
    assert "slug" in core.REGISTRY, "falta registrar 'slug' en la ZONA TEXTO de caja/core.py"
    assert "palabras" in core.REGISTRY, "falta registrar 'palabras' en la ZONA TEXTO de caja/core.py"
    assert core.despachar("slug", "Caja de Herramientas") == "caja-de-herramientas"
    assert core.despachar("palabras", "uno dos tres") == 3


def test_UW03_no_rompe_anclas():
    from caja import core
    assert core._ancla_a() == "a" and core._ancla_b() == "b" and core._ancla_c() == "c"


# ---------- UW-04: (deliberadamente SIN tests) ----------
# El gate de UW-04 es `pytest tests/test_gates.py -q -k UW04`: no colecta
# nada -> exit 5 -> FAILED explicito (D-M88). Crear un test que matchee UW04
# es manipulacion del gate y el sello git la detecta.


# ---------- UW-05: informe de tasas (nunca debe ejecutarse) ----------

def test_UW05_informe_disponible():
    informe = pytest.importorskip("caja.informe_tasas")
    assert informe.disponible() is False


# ---------- UW-06: comando version + ZONA META de core.py ----------

def test_UW06_modulo_version():
    from caja import version
    assert version.VERSION == "0.1.0"
    assert version.version() == "caja 0.1.0"


def test_UW06_registro_en_core():
    from caja import core
    assert "version" in core.REGISTRY, "falta registrar 'version' en la ZONA META de caja/core.py"
    assert core.despachar("version") == "caja 0.1.0"


def test_UW06_no_rompe_anclas():
    from caja import core
    assert core._ancla_a() == "a" and core._ancla_b() == "b" and core._ancla_c() == "c"
