"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
import threading as _threading


def run_limited(task, seconds, message):
    """Chạy task tối đa seconds giây; quá giờ thì mục kiểm tra CHƯA ĐẠT với lời nhắn message."""
    box, errors = [], []

    def target():
        try:
            box.append(task())
        except BaseException as error:
            errors.append(error)

    worker = _threading.Thread(target=target, daemon=True)
    worker.start()
    worker.join(seconds)
    if errors:
        raise errors[0]
    assert box, message
    return box


from cskh import find_order, count_status, orders_of, duplicate_codes, handle

ORDERS = [
    {"code": "DH1001", "buyer": "an.nguyen", "status": "Đang giao"},
    {"code": "DH1002", "buyer": "binh.tran", "status": "Đã giao"},
    {"code": "DH1003", "buyer": "an.nguyen", "status": "Chờ lấy hàng"},
    {"code": "DH1004", "buyer": "chi.le", "status": "Đang giao"},
    {"code": "DH1002", "buyer": "binh.tran", "status": "Đã giao"},
    {"code": "DH1005", "buyer": "an.nguyen", "status": "Đã hủy"},
]


def check_functions():
    assert find_order(ORDERS, "DH1004") == (4, 4) and find_order(ORDERS, "DH9999") == (None, 6)
    assert count_status(ORDERS, "đang GIAO") == 2
    assert orders_of(ORDERS, "an.nguyen") == ["DH1001", "DH1003", "DH1005"]
    assert duplicate_codes(ORDERS) == ["DH1002"] and duplicate_codes([]) == []


def check_commands():
    assert handle(ORDERS, "TIM dh1004") == "Đơn DH1004: Đang giao (vị trí 4, đã xét 4 đơn)."
    assert handle(ORDERS, "TIM DH9999") == "Không tìm thấy DH9999 (đã xét 6 đơn)."
    assert handle(ORDERS, "  dem   đang giao ") == 'Có 2 đơn "đang giao".'
    assert handle(ORDERS, "KHACH An.Nguyen") == "Khách an.nguyen có 3 đơn: DH1001, DH1003, DH1005."
    assert handle(ORDERS, "TRUNG") == "Có 1 mã đơn trùng: DH1002."


def check_errors():
    assert handle(ORDERS, "TIM") == "Thiếu thông tin. Cú pháp: TIM <mã đơn>"
    assert handle(ORDERS, "dem") == "Thiếu thông tin. Cú pháp: DEM <trạng thái>"
    assert handle(ORDERS, "KHACH") == "Thiếu thông tin. Cú pháp: KHACH <mã khách>"
    assert handle(ORDERS, "XOA DH1001") == "Lệnh không hợp lệ: XOA"
    assert handle(ORDERS, "   ") == "Chưa nhập lệnh."


def check_empty_results():
    assert handle(ORDERS, "KHACH dung.pham") == "Khách dung.pham chưa có đơn."
    assert handle(ORDERS[:4], "TRUNG") == "Không có mã đơn trùng."
    assert handle([], "TIM DH1") == "Không tìm thấy DH1 (đã xét 0 đơn)."


def check_many_duplicates_and_speed():
    big = [{"code": f"DH{i % 150000:06d}", "buyer": "k", "status": "Đã giao"} for i in range(200000)]
    box = run_limited(lambda: duplicate_codes(big), 3, "TRUNG với 200.000 đơn chạy quá 3 giây")
    assert len(box[0]) == 50000 and box[0][0] == "DH000000", "200.000 đơn phải có 50.000 mã trùng, mỗi mã một lần"
    assert duplicate_codes([{"code": c} for c in ("DH3", "DH1", "DH3", "DH3")]) == ["DH3"], "mã xuất hiện 3 lần chỉ ghi một lần"


CHECKS = [
    ("bốn hàm tra cứu", check_functions),
    ("các lệnh TIM, DEM, KHACH, TRUNG", check_commands),
    ("thiếu thông tin, lệnh lạ, dòng trống", check_errors),
    ("không có kết quả", check_empty_results),
    ("mã xuất hiện nhiều lần; TRUNG với 200.000 đơn trong 3 giây", check_many_duplicates_and_speed),
]


if __name__ == "__main__":
    passed = 0
    for name, check in CHECKS:
        try:
            check()
            print("ĐẠT      |", name)
            passed += 1
        except NotImplementedError:
            print("CHƯA LÀM |", name)
        except AssertionError as error:
            print("CHƯA ĐẠT |", name, "-", error)
        except Exception as error:
            print("LỖI      |", name, "-", type(error).__name__, error)
    print(f"Kết quả: {passed}/{len(CHECKS)} mục đạt")
