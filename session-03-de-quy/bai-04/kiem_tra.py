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


from tiet_kiem import months_to_goal


def check_example():
    assert months_to_goal(1000000, 5000000, 800000) == 5, f"ví dụ ra {months_to_goal(1000000, 5000000, 800000)}"


def check_reached():
    assert months_to_goal(5000000, 5000000, 800000) == 0 and months_to_goal(6000000, 5000000, 800000) == 0, "đã đủ hoặc vượt mục tiêu phải là 0 tháng"


def check_overshoot():
    assert months_to_goal(0, 1000000, 300000) == 4, "góp vượt mục tiêu ở tháng cuối vẫn phải dừng"


def check_never():
    box = run_limited(lambda: (months_to_goal(1000000, 5000000, 0), months_to_goal(1000000, 5000000, -50000)), 2, "hàm không dừng khi góp 0đ")
    assert box[0] == (None, None), f"góp 0đ và góp âm ra {box[0]}"


def check_long():
    assert months_to_goal(0, 100000000, 50000) == 2000, "2.000 tháng phải tính được, không báo RecursionError"
    assert months_to_goal(0, 10000000, 1000) == 10000


CHECKS = [
    ("ví dụ 5 tháng", check_example),
    ("đã đủ hoặc vượt mục tiêu", check_reached),
    ("góp vượt mục tiêu ở tháng cuối", check_overshoot),
    ("góp 0đ hoặc âm: None và dừng", check_never),
    ("mục tiêu cần hàng nghìn tháng", check_long),
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
