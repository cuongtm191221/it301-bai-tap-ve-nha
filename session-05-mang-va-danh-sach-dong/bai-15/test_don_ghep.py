from don_ghep import OrderArray


def test_ai_extend():
    a = OrderArray()
    a.extend(["GF01", "GF02"])
    assert a.items() == ["GF01", "GF02"]


def test_ai_index_of():
    a = OrderArray()
    a.extend(["GF01", "GF02"])
    assert a.index_of("GF02") == 1


def test_ai_remove_all():
    a = OrderArray()
    a.extend(["GF01", "GF02"])
    a.append("GF03")
    a.append("GF02")
    assert a.remove_all("GF02") == 2 and a.items() == ["GF01", "GF03"]
