from lich_su import RecentHistory


def make(limit=4):
    h = RecentHistory(limit)
    h.record("ZM001", "Bình minh trên phố")
    h.record("ZM002", "Mưa đêm")
    h.record("ZM003", "Đường về nhà")
    return h


def check_links(h):
    # Đi xuôi theo next và đi ngược theo prev phải ra cùng các node
    forward, current = [], h.head
    while current is not None:
        forward.append(current)
        current = current.next
    backward, current = [], h.tail
    while current is not None:
        backward.append(current)
        current = current.prev
    assert forward == backward[::-1]
    assert len(forward) == h.size
    if forward:
        assert h.head.prev is None and h.tail.next is None


def test_ghi_va_hien_thi():
    h = RecentHistory()
    assert h.to_lines() == ["Chưa có lịch sử nghe."]
    assert h.to_lines_oldest_first() == ["Chưa có lịch sử nghe."]
    assert h.record("ZM001", "Bình minh trên phố") == "Đã ghi: ZM001 - Bình minh trên phố"
    assert h.record("ZM002", "Mưa đêm") == "Đã ghi: ZM002 - Mưa đêm"
    assert h.to_lines() == ["1. ZM002 - Mưa đêm", "2. ZM001 - Bình minh trên phố"]
    assert h.to_lines_oldest_first() == ["1. ZM001 - Bình minh trên phố", "2. ZM002 - Mưa đêm"]
    check_links(h)


def test_bay_1_chuan_hoa_du_lieu_nhap():
    h = RecentHistory()
    assert h.record("  zm002 ", " Mưa đêm ") == "Đã ghi: ZM002 - Mưa đêm"


def test_bay_2_nghe_lai_bai_cu():
    h = make()
    assert h.record("zm001", "Bình minh trên phố") == "Đã đưa lên đầu: ZM001 - Bình minh trên phố"
    assert h.size == 3
    assert h.to_lines() == ["1. ZM001 - Bình minh trên phố", "2. ZM003 - Đường về nhà", "3. ZM002 - Mưa đêm"]
    assert h.tail.value == "ZM002 - Mưa đêm"
    check_links(h)


def test_bay_2_nghe_lai_bai_o_giua():
    h = make()
    assert h.record("ZM002", "Mưa đêm") == "Đã đưa lên đầu: ZM002 - Mưa đêm"
    assert h.to_lines_oldest_first() == ["1. ZM001 - Bình minh trên phố", "2. ZM003 - Đường về nhà", "3. ZM002 - Mưa đêm"]
    check_links(h)


def test_bay_3_nghe_lai_bai_dang_o_dau():
    h = make()
    assert h.record("ZM003", "Đường về nhà") == "Bài ZM003 đang ở đầu lịch sử."
    assert h.size == 3
    check_links(h)


def test_bay_4_vuot_gioi_han():
    h = make(limit=3)
    assert h.record("ZM004", "Phố cũ") == "Đã ghi: ZM004 - Phố cũ (bỏ bài cũ nhất: ZM001 - Bình minh trên phố)"
    assert h.size == 3
    assert h.to_lines() == ["1. ZM004 - Phố cũ", "2. ZM003 - Đường về nhà", "3. ZM002 - Mưa đêm"]
    assert h.tail.value == "ZM002 - Mưa đêm"
    check_links(h)


def test_xoa_bai_giua_va_khong_tim_thay():
    h = make()
    assert h.remove_song("ZM999") == "Không tìm thấy bài ZM999 trong lịch sử."
    assert h.remove_song(" zm002 ") == "Đã xóa khỏi lịch sử: ZM002 - Mưa đêm"
    assert h.to_lines() == ["1. ZM003 - Đường về nhà", "2. ZM001 - Bình minh trên phố"]
    check_links(h)


def test_bay_5_xoa_bai_dau_bai_cuoi_va_bai_duy_nhat():
    h = make()
    assert h.remove_song("ZM003") == "Đã xóa khỏi lịch sử: ZM003 - Đường về nhà"
    assert h.head.value == "ZM002 - Mưa đêm"
    check_links(h)
    assert h.remove_song("ZM001") == "Đã xóa khỏi lịch sử: ZM001 - Bình minh trên phố"
    assert h.head is h.tail
    check_links(h)
    h.remove_song("ZM002")
    assert h.head is None and h.tail is None and h.size == 0
    assert h.record("ZM004", "Phố cũ") == "Đã ghi: ZM004 - Phố cũ"
    check_links(h)
