from lui_tien import ListeningSession


def make():
    s = ListeningSession()
    s.play("ZM001", "Bình minh trên phố")
    s.play("ZM002", "Mưa đêm")
    s.play("ZM003", "Đường về nhà")
    return s


def check(s, codes, current):
    forward, node = [], s.head
    while node is not None:
        forward.append(node)
        node = node.next
    backward, node = [], s.tail
    while node is not None:
        backward.append(node)
        node = node.prev
    assert [n.value[:5] for n in forward] == codes
    assert forward == backward[::-1]
    assert s.size == len(codes)
    assert (s.current.value[:5] if s.current is not None else None) == current
    if forward:
        assert s.head.prev is None and s.tail.next is None


def test_phat_lan_luot():
    s = ListeningSession()
    assert s.to_lines() == ["Chưa phát bài nào."]
    assert s.play("ZM001", "Bình minh trên phố") == "Đang phát: ZM001 - Bình minh trên phố"
    assert s.play("ZM002", "Mưa đêm") == "Đang phát: ZM002 - Mưa đêm"
    assert s.to_lines() == ["  ZM001 - Bình minh trên phố", "> ZM002 - Mưa đêm"]
    check(s, ["ZM001", "ZM002"], "ZM002")


def test_lui_va_tien():
    s = make()
    assert s.back() == "Lùi về: ZM002 - Mưa đêm"
    assert s.back() == "Lùi về: ZM001 - Bình minh trên phố"
    assert s.forward() == "Tiến tới: ZM002 - Mưa đêm"
    assert s.to_lines() == ["  ZM001 - Bình minh trên phố", "> ZM002 - Mưa đêm", "  ZM003 - Đường về nhà"]
    check(s, ["ZM001", "ZM002", "ZM003"], "ZM002")


def test_bay_1_chuan_hoa_du_lieu_nhap():
    s = ListeningSession()
    assert s.play("  zm002 ", " Mưa đêm ") == "Đang phát: ZM002 - Mưa đêm"


def test_bay_2_phat_bai_moi_sau_khi_lui():
    s = make()
    s.back()
    s.back()
    assert s.play("ZM004", "Phố cũ") == "Đang phát: ZM004 - Phố cũ (đã bỏ 2 bài phía sau)"
    check(s, ["ZM001", "ZM004"], "ZM004")
    assert s.forward() == "Không có bài nào phía sau để tiến tới."
    assert s.back() == "Lùi về: ZM001 - Bình minh trên phố"
    assert s.play("ZM005", "Gió qua thềm") == "Đang phát: ZM005 - Gió qua thềm (đã bỏ 1 bài phía sau)"
    check(s, ["ZM001", "ZM005"], "ZM005")


def test_bay_3_lui_o_bai_dau_tien_o_bai_cuoi():
    s = make()
    assert s.forward() == "Không có bài nào phía sau để tiến tới."
    s.back()
    s.back()
    assert s.back() == "Đây là bài đầu tiên của phiên nghe."
    assert s.back() == "Đây là bài đầu tiên của phiên nghe."
    check(s, ["ZM001", "ZM002", "ZM003"], "ZM001")


def test_bay_4_chua_phat_bai_nao():
    s = ListeningSession()
    assert s.back() == "Chưa phát bài nào."
    assert s.forward() == "Chưa phát bài nào."
    check(s, [], None)


def test_bay_5_phat_lai_dung_bai_dang_phat():
    s = make()
    assert s.play("zm003", "Đường về nhà") == "Bài ZM003 đang được phát."
    check(s, ["ZM001", "ZM002", "ZM003"], "ZM003")
    s.back()
    assert s.play("ZM002", "Mưa đêm") == "Bài ZM002 đang được phát."
    check(s, ["ZM001", "ZM002", "ZM003"], "ZM002")


def test_cung_mot_bai_duoc_phat_o_hai_thoi_diem():
    s = make()
    assert s.play("ZM001", "Bình minh trên phố") == "Đang phát: ZM001 - Bình minh trên phố"
    check(s, ["ZM001", "ZM002", "ZM003", "ZM001"], "ZM001")
    assert s.to_lines()[0].startswith("  ") and s.to_lines()[3].startswith("> ")
