from playlist import Playlist


def make(codes):
    p = Playlist()
    for code in codes:
        p.add_last(code)
    return p


def test_count():
    assert make(["ZM001", "ZM002", "ZM003", "ZM004"]).count() == 4
    assert make(["ZM001"]).count() == 1


def test_count_danh_sach_rong():
    assert Playlist().count() == 0


def test_find_co_va_khong_co():
    p = make(["ZM001", "ZM002", "ZM003", "ZM004"])
    assert p.find("ZM001") == 0
    assert p.find("ZM003") == 2
    assert p.find("ZM999") is None


def test_find_khong_lam_mat_danh_sach():
    p = make(["ZM001", "ZM002", "ZM003", "ZM004"])
    head = p.head
    p.find("ZM003")
    p.find("ZM999")
    assert p.head is head
    assert p.to_text() == "ZM001 -> ZM002 -> ZM003 -> ZM004 -> None"
