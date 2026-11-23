from xem_san_pham import ProductBrowser


def make(*pages):
    b = ProductBrowser("Home")
    for p in pages:
        b.visit(p)
    return b


def test_quay_lai_tien_toi():
    b = make("A", "B", "C")
    assert b.back() == "B" and b.back() == "A"
    assert b.forward() == "B" and b.forward() == "C"


def test_tien_toi_roi_quay_lai():
    b = make("A", "B")
    b.back()
    b.forward()
    assert b.back() == "A" and b.back() == "Home"


def test_mo_trang_moi_xoa_tien_toi():
    b = make("A", "B")
    b.back()
    b.visit("X")
    assert b.forward() == "X"
    assert b.back() == "A"


def test_het_trang():
    b = make("A")
    assert b.back() == "Home" and b.back() == "Home"
    assert b.forward() == "A" and b.forward() == "A"
