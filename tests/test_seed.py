"""Smoke del seed: verde desde el commit inicial y a prueba de merges posteriores."""


def test_seed_nucleo_importa():
    from caja import core
    assert isinstance(core.ayuda(), list)


def test_seed_despacho_desconocido():
    import pytest
    from caja import core
    with pytest.raises(KeyError):
        core.despachar("comando-que-no-existe")


def test_seed_anclas_intactas():
    from caja import core
    assert (core._ancla_a(), core._ancla_b(), core._ancla_c()) == ("a", "b", "c")
