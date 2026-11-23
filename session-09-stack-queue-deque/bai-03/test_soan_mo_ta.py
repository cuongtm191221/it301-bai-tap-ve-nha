from soan_mo_ta import DescriptionEditor


def make(*parts):
    ed = DescriptionEditor()
    for p in parts:
        ed.write(p)
    return ed


def test_hoan_tac_va_lam_lai():
    ed = make("A", "B", "C")
    ed.undo()
    ed.undo()
    assert ed.text() == "A"
    ed.redo()
    assert ed.text() == "A B"


def test_lam_lai_xong_van_hoan_tac_duoc():
    ed = make("A", "B")
    ed.undo()
    ed.redo()
    ed.undo()
    assert ed.text() == "A"


def test_viet_moi_xoa_lam_lai():
    ed = make("A", "B")
    ed.undo()
    ed.write("X")
    ed.redo()
    assert ed.text() == "A X"


def test_khong_co_gi_de_lam():
    ed = make("A")
    for _ in range(3):
        ed.undo()
    assert ed.text() == ""
    for _ in range(3):
        ed.redo()
    assert ed.text() == "A"
