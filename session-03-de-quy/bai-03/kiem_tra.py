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
from ma_may_man import reverse_code, is_symmetric


def check_reverse():
    got = [reverse_code(c) for c in ("MOMO24", "ABC", "X", "")]
    assert got == ["42OMOM", "CBA", "X", ""], f"đảo mã ra {got}"


def check_odd():
    got = [is_symmetric(c) for c in ("121", "12321", "A", "12345")]
    assert got == [True, True, True, False], f"mã độ dài lẻ ra {got}"


def check_even_and_empty():
    got = [is_symmetric(c) for c in ("7887", "MOMO", "", "11", "12")]
    assert got == [True, False, True, True, False], f"mã độ dài chẵn và mã rỗng ra {got}"


def check_recursive():
    for f in (reverse_code, is_symmetric):
        src = inspect.getsource(f)
        assert "for " not in src and "while " not in src and "[::-1]" not in src and "reversed" not in src, f"{f.__name__} phải viết bằng đệ quy"


CHECKS = [
    ("đảo mã", check_reverse),
    ("mã độ dài lẻ", check_odd),
    ("mã độ dài chẵn và mã rỗng", check_even_and_empty),
    ("viết bằng đệ quy", check_recursive),
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
