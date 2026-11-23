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


from li_xi import route_count


def check_small():
    got = [route_count(c) for c in (1, 2, 3, 4, 5)]
    assert got == [1, 2, 3, 5, 8], f"bản đồ 1..5 ô ra {got}, mong đợi [1, 2, 3, 5, 8]"


def check_zero():
    assert route_count(0) == 1, f"bản đồ 0 ô ra {route_count(0)}, mong đợi 1"


def check_negative():
    assert route_count(-3) == 0, f"số ô âm ra {route_count(-3)}, mong đợi 0"


def check_fast():
    box = run_limited(lambda: route_count(80), 2, "bản đồ 80 ô tính quá 2 giây")
    assert box[0] == 37889062373143906, f"bản đồ 80 ô ra {box[0]}"


CHECKS = [
    ("bản đồ 1 đến 5 ô", check_small),
    ("bản đồ 0 ô", check_zero),
    ("số ô âm", check_negative),
    ("bản đồ 80 ô trong 2 giây", check_fast),
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
