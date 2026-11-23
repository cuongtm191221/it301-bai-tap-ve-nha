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


def _recursive_only(*funcs, banned=()):
    for f in funcs:
        src = inspect.getsource(f)
        for word in ("for ", "while ") + tuple(banned):
            assert word not in src, f"{f.__name__} phải viết bằng đệ quy, không dùng {word.strip()}"

import inspect
from doc_so_tien import digits_value, parse_amount, total_amounts


def check_digits():
    assert digits_value("2024") == 2024 and digits_value("7") == 7 and digits_value("007") == 7
    assert digits_value("") is None and digits_value("12a3") is None and digits_value("-5") is None


def check_valid():
    assert parse_amount("50000") == 50000
    assert parse_amount("1.234.567đ") == 1234567
    assert parse_amount(" 20.000 đ ") == 20000
    assert parse_amount("0") == 0


def check_groups():
    for bad in ("1.23.456", ".500", "1.000.", "1234.567", "1..000"):
        assert parse_amount(bad) is None, f"{bad!r} phải là None, đang ra {parse_amount(bad)}"


def check_invalid():
    for bad in ("12a", "", "đ", "   ", "-5.000", "5,000"):
        assert parse_amount(bad) is None, f"{bad!r} phải là None, đang ra {parse_amount(bad)}"


def check_total():
    assert total_amounts(["120.000đ", "85.500", "abc", "1.000.000đ"]) == (1205500, 1)
    assert total_amounts([]) == (0, 0)


def check_style():
    _recursive_only(digits_value, total_amounts, banned=("int(", "isdigit", "sum("))


CHECKS = [
    ("digits_value", check_digits),
    ("số tiền hợp lệ", check_valid),
    ("nhóm chữ số sai", check_groups),
    ("ký tự lạ, chuỗi rỗng", check_invalid),
    ("tổng hóa đơn chia nhóm", check_total),
    ("đệ quy, không dùng int()", check_style),
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
