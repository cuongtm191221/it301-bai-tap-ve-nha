from phat_ngay import Playlist, play_now


def make(codes):
    p = Playlist()
    for code in codes:
        p.add_last(code)
    return p


def test_chuyen_bai_o_giua_len_dau():
    p = make(["ZM001", "ZM002", "ZM003", "ZM004"])
    assert play_now(p, "ZM003") is True
    assert p.to_text() == "ZM003 -> ZM001 -> ZM002 -> ZM004 -> None"
    assert p.size == 4 and p.tail.value == "ZM004"


def test_chuyen_bai_cuoi_len_dau_roi_them_tiep():
    p = make(["ZM001", "ZM002", "ZM003"])
    assert play_now(p, "ZM003") is True
    assert p.tail.value == "ZM002" and p.size == 3
    p.add_last("ZM004")
    assert p.to_text() == "ZM003 -> ZM001 -> ZM002 -> ZM004 -> None"


def test_bai_da_o_dau():
    p = make(["ZM001", "ZM002"])
    assert play_now(p, "ZM001") is True
    assert p.to_text() == "ZM001 -> ZM002 -> None" and p.size == 2


def test_bai_khong_co():
    p = make(["ZM001", "ZM002"])
    assert play_now(p, "ZM999") is False
    assert p.to_text() == "ZM001 -> ZM002 -> None" and p.size == 2


def test_danh_sach_rong():
    p = Playlist()
    assert play_now(p, "ZM001") is False
    assert p.head is None and p.size == 0
