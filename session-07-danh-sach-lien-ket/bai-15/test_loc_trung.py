"""Ba test mà trợ lý AI gửi kèm đoạn mã. Cả ba đều xanh với mã do AI viết."""
from loc_trung import Playlist, remove_duplicates


def make(codes):
    p = Playlist()
    for code in codes:
        p.add_last(code)
    return p


def test_khong_co_bai_trung():
    p = make(["ZM001", "ZM002", "ZM003"])
    assert remove_duplicates(p) == 0
    assert p.to_text() == "ZM001 -> ZM002 -> ZM003 -> None"


def test_mot_bai_trung_o_giua():
    p = make(["ZM001", "ZM002", "ZM001", "ZM003"])
    assert remove_duplicates(p) == 1
    assert p.to_text() == "ZM001 -> ZM002 -> ZM003 -> None"


def test_danh_sach_rong():
    p = Playlist()
    assert remove_duplicates(p) == 0
    assert p.to_text() == "None"
