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


import inspect
from ma_gioi_thieu import valid_chars, count_digit_chars, is_valid_code


def check_chars():
    assert valid_chars("MOMO24") is True
    assert valid_chars("MOMO@24") is False, "MOMO@24 có ký tự @ phải là False"
    assert valid_chars("momo24") is False, "chữ thường không hợp lệ"
    assert valid_chars("") is True


def check_digits():
    assert count_digit_chars("MOMO100") == 3, f"MOMO100 ra {count_digit_chars('MOMO100')}, mong đợi 3"
    assert count_digit_chars("ABCDEF") == 0


def check_length():
    assert is_valid_code("AB1234") and is_valid_code("ABCDEFGH12"), "dài 6 và 10 ký tự phải hợp lệ"
    assert not is_valid_code("AB123") and not is_valid_code("ABCDEFGHI12"), "dài 5 và 11 ký tự không hợp lệ"


def check_rules():
    assert is_valid_code("MOMO2024") and is_valid_code("MOMO10")
    for bad in ("MOMO@24", "1MOMO23", "MOMOVN", "", "MOMO 24"):
        assert not is_valid_code(bad), f"{bad!r} phải không hợp lệ"


def check_recursive():
    for f in (valid_chars, count_digit_chars):
        src = inspect.getsource(f)
        assert "for " not in src and "while " not in src and "isdigit" not in src, f"{f.__name__} giữ cách viết đệ quy, không dùng vòng lặp hay isdigit()"


CHECKS = [
    ("valid_chars", check_chars),
    ("count_digit_chars có chữ số 0", check_digits),
    ("độ dài 6 đến 10", check_length),
    ("đủ các quy tắc", check_rules),
    ("giữ cách viết đệ quy", check_recursive),
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
