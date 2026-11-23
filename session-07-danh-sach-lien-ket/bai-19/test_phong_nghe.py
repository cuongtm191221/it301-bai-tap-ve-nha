from phong_nghe import RoomQueue


def check(q, expected):
    result, current = [], q.head
    while current is not None:
        result.append(("*" if current.vip else "") + current.value[:5])
        current = current.next
    assert result == expected
    assert q.size == len(expected)
    if expected:
        assert q.tail.value[:5] == expected[-1].lstrip("*") and q.tail.next is None
    else:
        assert q.head is None and q.tail is None


def make():
    q = RoomQueue()
    q.add_request("ZM001", "Bình minh trên phố")
    q.add_request("ZM002", "Mưa đêm")
    q.add_request("ZM003", "Đường về nhà", vip=True)
    q.add_request("ZM004", "Phố cũ", vip=True)
    return q


def test_yeu_cau_thuong_xep_cuoi():
    q = RoomQueue()
    assert q.to_lines() == ["Hàng chờ của phòng đang trống."]
    assert q.add_request("ZM001", "Bình minh trên phố") == "Đã xếp hàng: ZM001 - Bình minh trên phố (vị trí 1)"
    assert q.add_request("  zm002 ", " Mưa đêm ") == "Đã xếp hàng: ZM002 - Mưa đêm (vị trí 2)"
    check(q, ["ZM001", "ZM002"])


def test_yeu_cau_vip_dung_truoc_yeu_cau_thuong_va_sau_vip_cu():
    q = RoomQueue()
    q.add_request("ZM001", "Bình minh trên phố")
    q.add_request("ZM002", "Mưa đêm")
    assert q.add_request("ZM003", "Đường về nhà", vip=True) == "Đã xếp ưu tiên: ZM003 - Đường về nhà (vị trí 1)"
    assert q.add_request("ZM004", "Phố cũ", vip=True) == "Đã xếp ưu tiên: ZM004 - Phố cũ (vị trí 2)"
    check(q, ["*ZM003", "*ZM004", "ZM001", "ZM002"])
    assert q.to_lines() == ["1. [VIP] ZM003 - Đường về nhà", "2. [VIP] ZM004 - Phố cũ", "3. ZM001 - Bình minh trên phố", "4. ZM002 - Mưa đêm"]


def test_bay_1_trung_ma_ke_ca_khac_loai_tai_khoan():
    q = make()
    assert q.add_request("zm001", "Bình minh trên phố", vip=True) == "Bài ZM001 đã có trong hàng chờ của phòng."
    assert q.add_request("ZM003", "Đường về nhà") == "Bài ZM003 đã có trong hàng chờ của phòng."
    check(q, ["*ZM003", "*ZM004", "ZM001", "ZM002"])


def test_bay_2_vip_khi_hang_cho_rong_hoac_toan_vip():
    q = RoomQueue()
    assert q.add_request("ZM001", "Bình minh trên phố", vip=True) == "Đã xếp ưu tiên: ZM001 - Bình minh trên phố (vị trí 1)"
    assert q.add_request("ZM002", "Mưa đêm", vip=True) == "Đã xếp ưu tiên: ZM002 - Mưa đêm (vị trí 2)"
    check(q, ["*ZM001", "*ZM002"])
    assert q.add_request("ZM003", "Đường về nhà") == "Đã xếp hàng: ZM003 - Đường về nhà (vị trí 3)"
    check(q, ["*ZM001", "*ZM002", "ZM003"])


def test_bay_3_huy_yeu_cau_vip_cuoi_roi_them_vip():
    q = make()
    assert q.cancel("zm004") == "Đã hủy yêu cầu: ZM004 - Phố cũ"
    assert q.add_request("ZM005", "Gió qua thềm", vip=True) == "Đã xếp ưu tiên: ZM005 - Gió qua thềm (vị trí 2)"
    check(q, ["*ZM003", "*ZM005", "ZM001", "ZM002"])
    q.cancel("ZM003")
    q.cancel("ZM005")
    assert q.add_request("ZM006", "Ngày nắng", vip=True) == "Đã xếp ưu tiên: ZM006 - Ngày nắng (vị trí 1)"
    check(q, ["*ZM006", "ZM001", "ZM002"])


def test_bay_4_phat_het_vip_roi_them_vip():
    q = make()
    assert q.play_next() == "Đang phát: ZM003 - Đường về nhà"
    assert q.play_next() == "Đang phát: ZM004 - Phố cũ"
    assert q.add_request("ZM005", "Gió qua thềm", vip=True) == "Đã xếp ưu tiên: ZM005 - Gió qua thềm (vị trí 1)"
    check(q, ["*ZM005", "ZM001", "ZM002"])


def test_bay_5_huy_bai_cuoi_roi_them_va_huy_bai_khong_co():
    q = make()
    assert q.cancel("ZM999") == "Không tìm thấy bài ZM999 trong hàng chờ của phòng."
    assert q.cancel("ZM002") == "Đã hủy yêu cầu: ZM002 - Mưa đêm"
    q.add_request("ZM005", "Gió qua thềm")
    check(q, ["*ZM003", "*ZM004", "ZM001", "ZM005"])
    assert RoomQueue().cancel("ZM001") == "Không tìm thấy bài ZM001 trong hàng chờ của phòng."


def test_phat_het_hang_cho_roi_dung_lai():
    q = make()
    for _ in range(4):
        q.play_next()
    assert q.play_next() == "Hàng chờ của phòng đang trống."
    check(q, [])
    assert q.add_request("ZM005", "Gió qua thềm", vip=True) == "Đã xếp ưu tiên: ZM005 - Gió qua thềm (vị trí 1)"
    q.add_request("ZM006", "Ngày nắng")
    check(q, ["*ZM005", "ZM006"])


def test_vip_cuoi_cung_la_tail_roi_them_thuong():
    q = RoomQueue()
    q.add_request("ZM001", "Bình minh trên phố", vip=True)
    q.add_request("ZM002", "Mưa đêm")
    q.cancel("ZM002")
    q.add_request("ZM003", "Đường về nhà", vip=True)
    q.add_request("ZM004", "Phố cũ")
    check(q, ["*ZM001", "*ZM003", "ZM004"])
