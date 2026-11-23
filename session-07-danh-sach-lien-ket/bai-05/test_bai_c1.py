from lien_ket import make_list
from bai_c1 import total_minutes


def test_vi_du_trong_de():
    path = make_list([45, 30, 60])
    assert total_minutes(path) == (135, 3)


def test_danh_sach_rong():
    assert total_minutes(make_list([])) == (0, 0)


def test_khong_doi_danh_sach():
    path = make_list([45, 30, 60])
    total_minutes(path)
    assert path.to_text() == "45 -> 30 -> 60 -> None"
