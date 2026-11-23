from quan_ly import Playlist, handle


def run(lines):
    p = Playlist()
    return p, [handle(p, line) for line in lines]


def check(p, codes):
    result, current = [], p.head
    while current is not None:
        result.append(current.value[:5])
        current = current.next
    assert result == codes and p.size == len(codes)
    if codes:
        assert p.tail.value[:5] == codes[-1] and p.tail.next is None
    else:
        assert p.head is None and p.tail is None


def test_them_dau_xem_dem():
    p, out = run(["XEM", "THEM ZM001 | Bình minh trên phố", "THEM ZM002 | Mưa đêm", "DAU ZM003 | Đường về nhà", "XEM", "DEM"])
    assert out == [
        "Danh sách phát đang trống.",
        "Đã thêm vào cuối: ZM001 - Bình minh trên phố",
        "Đã thêm vào cuối: ZM002 - Mưa đêm",
        "Đã thêm vào đầu: ZM003 - Đường về nhà",
        "1. ZM003 - Đường về nhà\n2. ZM001 - Bình minh trên phố\n3. ZM002 - Mưa đêm",
        "Danh sách phát có 3 bài.",
    ]
    check(p, ["ZM003", "ZM001", "ZM002"])


def test_tim_va_bo():
    p, out = run(["THEM ZM001 | Bình minh trên phố", "THEM ZM002 | Mưa đêm", "TIM ZM002", "TIM ZM009", "BO ZM001", "BO ZM001"])
    assert out[2:] == ["Bài ZM002 - Mưa đêm đang ở vị trí 2.", "Không tìm thấy bài ZM009.", "Đã bỏ: ZM001 - Bình minh trên phố", "Không tìm thấy bài ZM001."]
    check(p, ["ZM002"])


def test_bay_1_lenh_viet_thuong_thua_khoang_trang():
    p, out = run(["  them   zm002 |  Mưa đêm  ", " tim  zm002 ", "dem", " xem "])
    assert out == ["Đã thêm vào cuối: ZM002 - Mưa đêm", "Bài ZM002 - Mưa đêm đang ở vị trí 1.", "Danh sách phát có 1 bài.", "1. ZM002 - Mưa đêm"]


def test_bay_2_thieu_thong_tin():
    p, out = run(["THEM ZM004", "THEM ZM004 |   ", "DAU ZM004", "THEM", "THEM | Phố cũ", "BO", "TIM"])
    assert out == [
        "Thiếu tên bài. Cú pháp: THEM <mã bài> | <tên bài>",
        "Thiếu tên bài. Cú pháp: THEM <mã bài> | <tên bài>",
        "Thiếu tên bài. Cú pháp: DAU <mã bài> | <tên bài>",
        "Thiếu mã bài. Cú pháp: THEM <mã bài> | <tên bài>",
        "Thiếu mã bài. Cú pháp: THEM <mã bài> | <tên bài>",
        "Thiếu mã bài. Cú pháp: BO <mã bài>",
        "Thiếu mã bài. Cú pháp: TIM <mã bài>",
    ]
    check(p, [])


def test_bay_3_lenh_la_va_dong_trong():
    p, out = run(["PHAT ZM001", "xoa zm001", "", "    "])
    assert out == ["Lệnh không hợp lệ: PHAT", "Lệnh không hợp lệ: XOA", "Chưa nhập lệnh.", "Chưa nhập lệnh."]


def test_bay_4_ma_bai_sai_dinh_dang():
    p, out = run(["THEM M4 | Phố cũ", "THEM ZM0004 | Phố cũ", "THEM ZMABC | Phố cũ", "BO 12345", "TIM ZM1"])
    assert out == ["Mã bài không hợp lệ: M4", "Mã bài không hợp lệ: ZM0004", "Mã bài không hợp lệ: ZMABC", "Mã bài không hợp lệ: 12345", "Mã bài không hợp lệ: ZM1"]
    check(p, [])


def test_bay_5_trung_ma_va_bo_bai_cuoi_roi_them():
    p, out = run(["THEM ZM001 | Bình minh trên phố", "THEM ZM002 | Mưa đêm", "DAU zm002 | Mưa đêm", "BO ZM002", "THEM ZM003 | Đường về nhà", "XEM"])
    assert out[2] == "Bài ZM002 đã có trong danh sách phát."
    assert out[5] == "1. ZM001 - Bình minh trên phố\n2. ZM003 - Đường về nhà"
    check(p, ["ZM001", "ZM003"])


def test_bo_het_roi_them_lai():
    p, out = run(["THEM ZM001 | Bình minh trên phố", "BO ZM001", "XEM", "DAU ZM002 | Mưa đêm", "THEM ZM003 | Đường về nhà"])
    assert out[2] == "Danh sách phát đang trống."
    check(p, ["ZM002", "ZM003"])


def test_ten_bai_co_dau_gach_dung():
    p, out = run(["THEM ZM001 | Mưa | Nắng", "XEM"])
    assert out == ["Đã thêm vào cuối: ZM001 - Mưa | Nắng", "1. ZM001 - Mưa | Nắng"]
