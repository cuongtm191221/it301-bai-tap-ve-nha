from trinh_phat import Player


def make(codes):
    p = Player()
    for code in codes:
        p.add_last(code)
    return p


def test_tien_va_lui():
    p = make(["ZM001", "ZM002", "ZM003"])
    assert p.play_first() == "Đang phát: ZM001"
    assert p.next_song() == "Đang phát: ZM002"
    assert p.prev_song() == "Đang phát: ZM001"


def test_lui_khi_dang_o_bai_dau():
    p = make(["ZM001", "ZM002"])
    p.play_first()
    assert p.prev_song() == "Đã ở bài đầu, không thể lùi."
    assert p.current.value == "ZM001"


def test_tien_khi_dang_o_bai_cuoi():
    p = make(["ZM001", "ZM002"])
    p.play_first()
    p.next_song()
    assert p.next_song() == "Đã ở bài cuối, không thể chuyển tiếp."
    assert p.next_song() == "Đã ở bài cuối, không thể chuyển tiếp."
    assert p.current.value == "ZM002"


def test_chua_phat_bai_nao():
    p = make(["ZM001", "ZM002"])
    assert p.next_song() == "Chưa phát bài nào."
    assert p.prev_song() == "Chưa phát bài nào."


def test_danh_sach_trong():
    p = Player()
    assert p.play_first() == "Danh sách phát đang trống."
    assert p.current is None
