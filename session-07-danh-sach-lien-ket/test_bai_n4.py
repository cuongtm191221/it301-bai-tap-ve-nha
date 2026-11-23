from lien_ket import make_dlist
from bai_n4 import keep_latest


def test_vi_du_trong_de():
    d = make_dlist(["V1", "V2", "V3", "V4", "V5"])
    assert keep_latest(d, 3) == 2
    assert d.to_text() == "V3 -> V4 -> V5 -> None"
    assert d.to_text_backward() == "V5 -> V4 -> V3 -> None"


def test_k_lon_hon_so_phien_ban():
    d = make_dlist(["V1", "V2"])
    assert keep_latest(d, 5) == 0
    assert d.to_text() == "V1 -> V2 -> None"


def test_k_am_bao_loi():
    d = make_dlist(["V1"])
    try:
        keep_latest(d, -1)
        assert False, "k âm phải báo ValueError"
    except ValueError as e:
        assert "không được âm" in str(e)
