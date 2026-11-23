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
from tim_giao_dich import find_transaction, count_matches, search_message

CODES = ["MM2401", " mm2402", "MM2403 ", "MM2402", "MM2405"]


def check_find():
    assert find_transaction(CODES, "MM2403") == 2
    assert find_transaction(CODES, "mm2405 ") == 4, "phải chuẩn hóa cả mã cần tìm"
    assert find_transaction(CODES, "MM2402") == 1, "mã trùng: trả về vị trí đầu tiên"
    assert find_transaction(CODES, "MM9999") == -1
    assert find_transaction([], "MM2401") == -1


def check_count():
    assert count_matches(CODES, "MM2402") == 2
    assert count_matches(CODES, "MM9999") == 0
    assert count_matches([], "MM2401") == 0


def check_messages():
    assert search_message(CODES, "mm2405 ") == "Tìm thấy MM2405 ở dòng 5."
    assert search_message(CODES, "MM2402") == "Tìm thấy MM2402 ở dòng 2 (mã xuất hiện 2 lần, cần kiểm tra trùng)."
    assert search_message(CODES, "MM9999") == "Không tìm thấy giao dịch MM9999."
    assert search_message(CODES, "  ") == "Mã giao dịch trống, vui lòng nhập lại."


def check_long():
    codes = [f"MM{k:05d}" for k in range(600)]
    assert find_transaction(codes, "MM00599") == 599
    assert count_matches(codes, "MM00300") == 1


def check_style():
    _recursive_only(find_transaction, count_matches, banned=("[1:]", ".index(", ".count(", " in codes"))
    data = list(CODES)
    search_message(data, "MM2402")
    assert data == CODES, "không được sửa list đầu vào"


CHECKS = [
    ("find_transaction", check_find),
    ("count_matches", check_count),
    ("thông báo cho tổng đài", check_messages),
    ("600 giao dịch", check_long),
    ("đệ quy theo vị trí, không cắt list", check_style),
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
