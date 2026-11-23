from lien_ket import make_list
from bai_n1 import insert_after


def test_chen_o_giua():
    p = make_list(["KH1", "KH2", "KH3"])
    assert insert_after(p, "KH2", "KH9") is True
    assert p.to_text() == "KH1 -> KH2 -> KH9 -> KH3 -> None"


def test_chen_sau_node_cuoi_doi_tail():
    p = make_list(["KH1", "KH2", "KH3"])
    insert_after(p, "KH3", "KH8")
    assert p.tail.value == "KH8"


def test_khong_co_target():
    p = make_list(["KH1"])
    assert insert_after(p, "KH5", "KH9") is False
    assert p.to_text() == "KH1 -> None"


def test_danh_sach_rong():
    p = make_list([])
    assert insert_after(p, "KH1", "KH9") is False
