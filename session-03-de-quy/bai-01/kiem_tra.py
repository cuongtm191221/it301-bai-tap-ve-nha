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


from diem_thuong import streak_points, count_digits


def check_streak_base():
    assert streak_points(0) == 0, f"0 ngày ra {streak_points(0)}"
    assert streak_points(1) == 100, f"1 ngày ra {streak_points(1)}"


def check_streak():
    got = [streak_points(n) for n in (2, 3, 7, 30)]
    assert got == [300, 600, 2800, 46500], f"2, 3, 7, 30 ngày ra {got}"


def check_digits():
    got = [count_digits(n) for n in (7, 10, 45000, 1250000, 999999)]
    assert got == [1, 2, 5, 7, 6], f"số chữ số ra {got}"


def check_digits_small():
    got = [count_digits(n) for n in (1, 9)]
    assert got == [1, 1], f"số có một chữ số ra {got}"


CHECKS = [
    ("điểm thưởng 0 và 1 ngày (trường hợp cơ sở)", check_streak_base),
    ("điểm thưởng 2, 3, 7, 30 ngày", check_streak),
    ("số chữ số của số tiền", check_digits),
    ("số có một chữ số", check_digits_small),
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
