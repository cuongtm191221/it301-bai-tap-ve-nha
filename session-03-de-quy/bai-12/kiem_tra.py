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
from nen_trang_thai import compress, longest_fail_streak, summary


def check_compress():
    assert compress(["OK", "OK", "FAIL", "OK"]) == [("OK", 2), ("FAIL", 1), ("OK", 1)]
    assert compress(["PENDING"]) == [("PENDING", 1)]
    assert compress([]) == []


def check_clean():
    assert compress(["ok ", " OK", "Ok"]) == [("OK", 3)], f"ra {compress(['ok ', ' OK', 'Ok'])}"


def check_not_merge_far():
    assert compress(["OK", "FAIL", "OK"]) == [("OK", 1), ("FAIL", 1), ("OK", 1)], "chỉ gộp các trạng thái liên tiếp"


def check_streak():
    assert longest_fail_streak(["FAIL", "OK", "FAIL", "FAIL"]) == 2
    assert longest_fail_streak(["OK", "OK"]) == 0 and longest_fail_streak([]) == 0
    assert longest_fail_streak(["fail", "FAIL ", "OK"]) == 2


def check_summary():
    assert summary(["OK", "FAIL", "fail", "FAIL ", "OK"]) == "OK x1, FAIL x3, OK x1 | Cảnh báo: 3 lần thất bại liên tiếp"
    assert summary(["OK", "OK", "FAIL", "OK"]) == "OK x2, FAIL x1, OK x1"
    assert summary([]) == "Chưa có giao dịch"


def check_long():
    data = ["OK"] * 300 + ["FAIL"] * 4 + ["OK"] * 200
    assert compress(data) == [("OK", 300), ("FAIL", 4), ("OK", 200)]
    _recursive_only(compress)
    original = ["OK", "ok"]
    compress(original)
    assert original == ["OK", "ok"], "không được sửa list đầu vào"


CHECKS = [
    ("nén trạng thái", check_compress),
    ("chuẩn hóa chữ hoa, khoảng trắng", check_clean),
    ("chỉ gộp trạng thái liên tiếp", check_not_merge_far),
    ("chuỗi FAIL dài nhất", check_streak),
    ("dòng tóm tắt và cảnh báo", check_summary),
    ("500 trạng thái, đệ quy, không sửa list", check_long),
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
