import pytest

from playlist import Playlist


def make(codes):
    p = Playlist()
    for code in codes:
        p.add_last(code)
    return p


def test_bo_bai_cuoi_roi_them_tiep():
    p = make(["ZM001", "ZM002", "ZM003"])
    assert p.remove("ZM003") is True
    assert p.tail.value == "ZM002" and p.size == 2
    p.add_last("ZM004")
    assert p.to_text() == "ZM001 -> ZM002 -> ZM004 -> None"


def test_bo_bai_dau():
    p = make(["ZM001", "ZM002", "ZM003"])
    assert p.remove("ZM001") is True
    assert p.to_text() == "ZM002 -> ZM003 -> None" and p.size == 2


def test_bo_bai_khong_co_va_danh_sach_rong():
    p = make(["ZM001", "ZM002"])
    assert p.remove("ZM999") is False
    assert p.size == 2
    assert Playlist().remove("ZM001") is False


def test_phat_het_danh_sach():
    p = make(["ZM001", "ZM002"])
    assert p.remove_first() == "ZM001"
    assert p.remove_first() == "ZM002"
    assert p.head is None and p.tail is None and p.size == 0


def test_phat_khi_danh_sach_trong():
    with pytest.raises(IndexError, match="danh sách phát đang trống"):
        Playlist().remove_first()
