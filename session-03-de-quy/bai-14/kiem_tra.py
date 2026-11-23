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


import inspect, random
from ma_xac_thuc import otp_value_v1, otp_value_v2, otp_message

BOTH = [("otp_value_v1", otp_value_v1), ("otp_value_v2", otp_value_v2)]


def check_small():
    for name, f in BOTH:
        assert f(7, 3, 1000000) == 343, name
        assert f(2, 10, 1000) == 24, f"{name}(2, 10, 1000) ra {f(2, 10, 1000)}"


def check_edges():
    for name, f in BOTH:
        assert f(123457, 0, 999983) == 1, f"{name}: bộ đếm 0 phải ra 1"
        assert f(5, 4, 1) == 0 and f(5, 0, 1) == 0, f"{name}: mod 1 thì mọi giá trị là 0"
        assert f(1999998, 2, 999983) == (1999998 % 999983) ** 2 % 999983, f"{name}: seed lớn hơn mod"


def check_same_answer():
    rng = random.Random(11)
    for _ in range(200):
        seed, counter, mod = rng.randint(0, 10 ** 6), rng.randint(0, 300), rng.randint(1, 10 ** 6)
        assert otp_value_v1(seed, counter, mod) == otp_value_v2(seed, counter, mod), f"khác nhau với {seed}, {counter}, {mod}"


def check_message():
    assert otp_message(7, 3, 1000000) == "Mã xác thực lần 3: 000343"
    assert otp_message(123457, -1, 999983) == "Bộ đếm không hợp lệ."
    assert otp_message(123457, 5, 0) == "Cấu hình thiết bị không hợp lệ."


def check_large():
    box = run_limited(lambda: (otp_message(123457, 5000, 999983), otp_message(123457, 10 ** 9, 999983)), 2, "bộ đếm lớn tính quá 2 giây")
    expected = [f"Mã xác thực lần {c}: {pow(123457, c, 999983):06d}" for c in (5000, 10 ** 9)]
    assert list(box[0]) == expected, f"ra {box[0]}"


def check_no_builtin():
    for name, f in BOTH:
        src = inspect.getsource(f)
        assert "pow(" not in src and "**" not in src, f"{name} không dùng pow() hay **"


CHECKS = [
    ("ví dụ nhỏ trên cả hai giải pháp", check_small),
    ("bộ đếm 0, mod 1, seed lớn", check_edges),
    ("hai giải pháp cùng kết quả", check_same_answer),
    ("thông báo và dữ liệu sai", check_message),
    ("bộ đếm 5.000 và 1 tỷ trong 2 giây", check_large),
    ("không dùng pow() hay **", check_no_builtin),
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
