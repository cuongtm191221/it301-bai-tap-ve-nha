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


_threading.stack_size(64 * 1024 * 1024)   # luồng kiểm tra cần đủ chỗ cho đệ quy sâu


import inspect
import sinh_ma
from sinh_ma import clean_chars, count_codes, generate_codes, codes_message


def check_clean():
    assert clean_chars(" b a 1 a ") == ["1", "A", "B"], clean_chars(" b a 1 a ")
    assert clean_chars("") == []


def check_generate():
    got = generate_codes("AB12", 2)
    assert len(got) == 12 and got[:4] == ["12", "1A", "1B", "21"], got
    assert all(c[0] != c[1] for c in got), "hai ký tự cạnh nhau không được trùng"
    three = generate_codes("AB12", 3)
    assert len(three) == 36 and three == sorted(three), "36 mã, xếp tăng dần"


def check_count():
    assert count_codes("AB12", 3) == 36 and count_codes("AB12", 1) == 4
    assert count_codes("AB12", 0) == 1 and count_codes("7", 3) == 0
    for k in range(0, 5):
        assert count_codes("XYZ9", k) == len(generate_codes("XYZ9", k)), f"đếm và sinh lệch nhau ở độ dài {k}"


def check_messages():
    assert codes_message("AB12", 3) == "Đã sinh 36 mã, ví dụ: 121, 12A, 12B"
    assert codes_message("", 4) == "Cấu hình mã không hợp lệ." and codes_message("AB", 0) == "Cấu hình mã không hợp lệ."
    assert codes_message("7", 3) == "Không sinh được mã nào với cấu hình này."


def check_limit():
    box = run_limited(lambda: codes_message("0123456789", 12), 1, "cấu hình lớn phải chỉ đếm, không sinh mã")
    assert box[0] == "Có 313810596090 mã, vượt giới hạn 100000 mã mỗi lần sinh.", box[0]


def check_rules():
    src = inspect.getsource(sinh_ma)
    assert "itertools" not in src and "product(" not in src, "không dùng itertools"
    assert "for " not in inspect.getsource(count_codes) + inspect.getsource(sinh_ma._count if hasattr(sinh_ma, "_count") else count_codes), "count_codes viết bằng đệ quy, không vòng lặp"


CHECKS = [
    ("làm sạch ký tự", check_clean),
    ("sinh mã và thứ tự", check_generate),
    ("đếm khớp với sinh", check_count),
    ("thông báo", check_messages),
    ("cấu hình lớn chỉ đếm", check_limit),
    ("không dùng itertools", check_rules),
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
