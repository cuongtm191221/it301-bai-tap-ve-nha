from sap_xep import EditablePlaylist


def make():
    p = EditablePlaylist()
    p.add_song("ZM001", "Bình minh trên phố")
    p.add_song("ZM002", "Mưa đêm")
    p.add_song("ZM003", "Đường về nhà")
    return p


def codes(p):
    result, current = [], p.head
    while current is not None:
        result.append(current.value[:5])
        current = current.next
    assert len(result) == p.size
    if result:
        assert p.tail.value[:5] == result[-1] and p.tail.next is None
    else:
        assert p.tail is None
    return result


def test_them_va_hien_thi():
    p = EditablePlaylist()
    assert p.to_lines() == ["Danh sách phát đang trống."]
    assert p.add_song("  zm001 ", " Bình minh trên phố ") == "Đã thêm: ZM001 - Bình minh trên phố"
    assert p.add_song("ZM001", "Bình minh trên phố") == "Bài ZM001 đã có trong danh sách phát."
    assert p.add_song("ZM002", "Mưa đêm") == "Đã thêm: ZM002 - Mưa đêm"
    assert p.to_lines() == ["1. ZM001 - Bình minh trên phố", "2. ZM002 - Mưa đêm"]
    assert codes(p) == ["ZM001", "ZM002"]


def test_chen_vao_giua():
    p = make()
    assert p.insert_after(" zm001 ", " zm004", "Phố cũ ") == "Đã chèn: ZM004 - Phố cũ (sau ZM001)"
    assert codes(p) == ["ZM001", "ZM004", "ZM002", "ZM003"]


def test_bay_1_chen_bai_da_co():
    p = make()
    assert p.insert_after("ZM001", "zm003", "Đường về nhà") == "Bài ZM003 đã có trong danh sách phát."
    assert p.insert_after("ZM999", "ZM003", "Đường về nhà") == "Bài ZM003 đã có trong danh sách phát."
    assert codes(p) == ["ZM001", "ZM002", "ZM003"]


def test_bay_2_khong_co_bai_moc():
    p = make()
    assert p.insert_after("ZM999", "ZM004", "Phố cũ") == "Không tìm thấy bài ZM999 để chèn sau."
    assert codes(p) == ["ZM001", "ZM002", "ZM003"]
    empty = EditablePlaylist()
    assert empty.insert_after("ZM001", "ZM004", "Phố cũ") == "Không tìm thấy bài ZM001 để chèn sau."


def test_bay_3_chen_sau_bai_cuoi_roi_them():
    p = make()
    assert p.insert_after("ZM003", "ZM004", "Phố cũ") == "Đã chèn: ZM004 - Phố cũ (sau ZM003)"
    assert p.tail.value == "ZM004 - Phố cũ"
    p.add_song("ZM005", "Gió qua thềm")
    assert codes(p) == ["ZM001", "ZM002", "ZM003", "ZM004", "ZM005"]


def test_dua_bai_giua_len_dau():
    p = make()
    assert p.move_to_top("zm002") == "Đã đưa lên đầu: ZM002 - Mưa đêm"
    assert codes(p) == ["ZM002", "ZM001", "ZM003"]


def test_bay_4_dua_bai_cuoi_len_dau_roi_them():
    p = make()
    assert p.move_to_top("ZM003") == "Đã đưa lên đầu: ZM003 - Đường về nhà"
    assert p.tail.value == "ZM002 - Mưa đêm"
    p.add_song("ZM004", "Phố cũ")
    assert codes(p) == ["ZM003", "ZM001", "ZM002", "ZM004"]


def test_bay_5_bai_da_o_dau_khong_tim_thay_danh_sach_rong():
    p = make()
    assert p.move_to_top("ZM001") == "Bài ZM001 đã ở đầu danh sách phát."
    assert p.move_to_top("ZM999") == "Không tìm thấy bài ZM999 trong danh sách phát."
    assert codes(p) == ["ZM001", "ZM002", "ZM003"]
    empty = EditablePlaylist()
    assert empty.move_to_top("ZM001") == "Không tìm thấy bài ZM001 trong danh sách phát."
    one = EditablePlaylist()
    one.add_song("ZM001", "Bình minh trên phố")
    assert one.move_to_top("ZM001") == "Bài ZM001 đã ở đầu danh sách phát."
    assert codes(one) == ["ZM001"]
