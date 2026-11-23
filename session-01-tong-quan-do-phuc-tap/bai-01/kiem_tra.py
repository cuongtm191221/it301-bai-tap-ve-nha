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


from tra_cuu import find_order

TODAY = [
    {"code": "DH1001", "status": "Đang giao"},
    {"code": "DH1002", "status": "Đã giao"},
    {"code": "DH1003", "status": "Chờ lấy hàng"},
    {"code": "DH1004", "status": "Đang giao"},
]
WEEK = [
    {"code": "DH0901", "status": "Đã giao"},
    {"code": "DH0902", "status": "Đã hủy"},
    {"code": "DH0903", "status": "Đang giao"},
]


def check_first_and_middle():
    assert find_order(TODAY, "DH1001") == (0, 1), f"tìm đơn đầu ra {find_order(TODAY, 'DH1001')}"
    assert find_order(TODAY, "DH1002") == (1, 2), f"tìm đơn thứ hai ra {find_order(TODAY, 'DH1002')}"


def check_last():
    assert find_order(TODAY, "DH1004") == (3, 4), f"tìm đơn cuối ra {find_order(TODAY, 'DH1004')}"


def check_not_found():
    assert find_order(TODAY, "DH9999") == (None, 4), f"mã không có ra {find_order(TODAY, 'DH9999')}"
    assert find_order([], "DH1001") == (None, 0), f"danh sách rỗng ra {find_order([], 'DH1001')}"


def check_cancelled():
    box = run_limited(lambda: (find_order(WEEK, "DH0903"), find_order(WEEK, "DH0902")), 2, "hàm không dừng khi gặp đơn đã hủy")
    assert box[0][0] == (2, 3), f"tìm đơn đứng sau đơn đã hủy ra {box[0][0]}"
    assert box[0][1] == (None, 3), f"tìm đơn đã hủy ra {box[0][1]}"


def check_steps_worst_case():
    orders = [{"code": f"DH{i:04d}", "status": "Đang giao"} for i in range(1000)]
    assert find_order(orders, "DH0999") == (999, 1000), "đơn cuối trong 1.000 đơn phải xét 1.000 đơn"
    assert find_order(orders, "DH9999") == (None, 1000), "mã không có trong 1.000 đơn phải xét 1.000 đơn"


CHECKS = [
    ("tìm đơn đầu và đơn ở giữa", check_first_and_middle),
    ("tìm đơn đứng cuối danh sách", check_last),
    ("không tìm thấy và danh sách rỗng trả về None", check_not_found),
    ("bỏ qua đơn đã hủy và luôn dừng", check_cancelled),
    ("số đơn đã xét trong trường hợp xấu nhất", check_steps_worst_case),
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
