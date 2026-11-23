from lien_ket import make_list
from bai_n2 import remove_all


def test_vi_du_trong_de():
    q = make_list(["HV1", "HV7", "HV2", "HV7"])
    assert remove_all(q, "HV7") == 2
    assert q.to_text() == "HV1 -> HV2 -> None"
    assert q.tail.value == "HV2"


def test_xoa_het():
    q = make_list(["HV7", "HV7"])
    assert remove_all(q, "HV7") == 2
    assert q.head is None
    assert q.tail is None


def test_khong_co_ma():
    q = make_list(["HV1"])
    assert remove_all(q, "HV9") == 0
    assert q.to_text() == "HV1 -> None"
