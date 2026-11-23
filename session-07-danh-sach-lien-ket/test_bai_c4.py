from lien_ket import make_dlist
from bai_c4 import to_list_backward


def test_vi_du_trong_de():
    assert to_list_backward(make_dlist(["V1", "V2", "V3"])) == ["V3", "V2", "V1"]


def test_danh_sach_rong():
    assert to_list_backward(make_dlist([])) == []


def test_mot_phien_ban():
    assert to_list_backward(make_dlist(["V1"])) == ["V1"]
