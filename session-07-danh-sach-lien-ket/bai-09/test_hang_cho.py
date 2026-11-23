from hang_cho import PlayQueue


def make():
    q = PlayQueue()
    q.add_song("ZM001", "Bình minh trên phố")
    q.add_song("ZM002", "Mưa đêm")
    q.add_song("ZM003", "Đường về nhà")
    return q


def test_them_va_hien_thi():
    q = PlayQueue()
    assert q.to_lines() == ["Hàng chờ đang trống."]
    assert q.add_song("ZM001", "Bình minh trên phố") == "Đã thêm: ZM001 - Bình minh trên phố"
    assert q.add_song("ZM002", "Mưa đêm") == "Đã thêm: ZM002 - Mưa đêm"
    assert q.to_lines() == ["1. ZM001 - Bình minh trên phố", "2. ZM002 - Mưa đêm"]
    assert q.size == 2 and q.tail.value == "ZM002 - Mưa đêm"


def test_bay_1_chuan_hoa_du_lieu_nhap():
    q = PlayQueue()
    assert q.add_song("  zm002 ", " Mưa đêm ") == "Đã thêm: ZM002 - Mưa đêm"


def test_bay_2_trung_ma():
    q = make()
    assert q.add_song("zm001", "Bình minh trên phố") == "Bài ZM001 đã có trong hàng chờ."
    assert q.size == 3


def test_phat_theo_thu_tu_them():
    q = make()
    assert q.play_next() == "Đang phát: ZM001 - Bình minh trên phố"
    assert q.play_next() == "Đang phát: ZM002 - Mưa đêm"
    assert q.size == 1 and q.head is q.tail


def test_bay_3_phat_khi_hang_cho_rong():
    q = PlayQueue()
    assert q.play_next() == "Hàng chờ đang trống, không có bài để phát."
    q.add_song("ZM001", "Bình minh trên phố")
    q.play_next()
    assert q.head is None and q.tail is None and q.size == 0
    assert q.play_next() == "Hàng chờ đang trống, không có bài để phát."


def test_bay_4_bo_bai_khong_co():
    q = make()
    assert q.remove_song("ZM999") == "Không tìm thấy bài ZM999 trong hàng chờ."
    assert q.size == 3


def test_bay_5_bo_bai_cuoi_roi_them_tiep():
    q = make()
    assert q.remove_song("zm003") == "Đã bỏ: ZM003 - Đường về nhà"
    assert q.tail.value == "ZM002 - Mưa đêm" and q.size == 2
    q.add_song("ZM004", "Phố cũ")
    assert q.to_lines() == ["1. ZM001 - Bình minh trên phố", "2. ZM002 - Mưa đêm", "3. ZM004 - Phố cũ"]
