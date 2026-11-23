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
from dinh_dang_tien import format_money, receipt_line


def check_basic():
    assert format_money(1234567) == "1.234.567", format_money(1234567)
    assert format_money(45000) == "45.000"
    assert format_money(1000) == "1.000"


def check_small():
    assert format_money(0) == "0" and format_money(950) == "950" and format_money(7) == "7"


def check_zero_groups():
    assert format_money(1005) == "1.005", f"1005 ra {format_money(1005)}"
    assert format_money(1000005) == "1.000.005", f"1000005 ra {format_money(1000005)}"
    assert format_money(2000000000) == "2.000.000.000"


def check_negative():
    assert format_money(-1500000) == "-1.500.000", format_money(-1500000)
    assert format_money(-999) == "-999"


def check_receipt():
    assert receipt_line("  Nguyễn   Văn An ", 1005000) == "Chuyển tiền cho Nguyễn Văn An: 1.005.000đ"
    assert receipt_line("   ", 20000) == "Chuyển tiền cho Không rõ người nhận: 20.000đ"


def check_style():
    _recursive_only(format_money, banned=(":,", "format(", "replace("))


CHECKS = [
    ("số có nhiều nhóm", check_basic),
    ("số dưới 1.000", check_small),
    ("nhóm có chữ số 0 ở đầu", check_zero_groups),
    ("số âm", check_negative),
    ("dòng biên lai", check_receipt),
    ("đệ quy, không dùng định dạng có sẵn", check_style),
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
