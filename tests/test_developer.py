from pydriller.domain.developer import Developer


def test_eq_dev():
    d1 = Developer("Davide", "s.d@gmail.com")
    d2 = Developer("Davide", "s.d@gmail.com")
    d3 = Developer("Davide", "s.d@gmail.eu")
    d4 = None

    assert d1 == d1
    assert d1 == d2
    assert d1 != d3
    assert d1 != d4
