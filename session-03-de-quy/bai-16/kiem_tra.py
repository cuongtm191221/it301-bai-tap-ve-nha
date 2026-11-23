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
from chon_qua import choose_count_v1, choose_count_v2, prize_message

BOTH = [("choose_count_v1", choose_count_v1), ("choose_count_v2", choose_count_v2)]


def check_small():
    for name, f in BOTH:
        assert f(5, 2) == 10 and f(6, 3) == 20, name
        assert f(10, 10) == 1 and f(7, 0) == 1, f"{name}: chọn hết hoặc không chọn ô nào là 1 cách"


def check_out_of_range():
    for name, f in BOTH:
        assert f(4, 6) == 0 and f(4, -1) == 0, f"{name}: k ngoài khoảng 0..n phải ra 0"


def check_same_answer():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(0, 16)
        k = rng.randint(-2, 18)
        assert choose_count_v1(n, k) == choose_count_v2(n, k), f"hai giải pháp khác nhau với n={n}, k={k}"


def check_message():
    assert prize_message(5, 2) == "Có 10 cách chọn 2 ô trong 5 ô."
    assert prize_message(4, 6) == "Không đủ ô: cần chọn 6 ô nhưng chỉ có 4 ô."
    assert prize_message(0, 1) == "Dữ liệu trò chơi không hợp lệ." and prize_message(5, 0) == "Dữ liệu trò chơi không hợp lệ."


def check_fast():
    box = run_limited(lambda: (prize_message(40, 20), prize_message(300, 150)), 2, "40 ô hoặc 300 ô tính quá 2 giây")
    assert box[0][0] == "Có 137846528820 cách chọn 20 ô trong 40 ô.", box[0][0]
    assert box[0][1].startswith("Có 9375970277") and box[0][1].endswith(" cách chọn 150 ô trong 300 ô."), box[0][1][:60]


def check_no_builtin():
    import chon_qua
    src = inspect.getsource(chon_qua)
    assert "comb(" not in src and "factorial" not in src and "import math" not in src, "không dùng math.comb hay math.factorial"


CHECKS = [
    ("ví dụ nhỏ trên cả hai giải pháp", check_small),
    ("k ngoài khoảng", check_out_of_range),
    ("hai giải pháp cùng kết quả", check_same_answer),
    ("thông báo và dữ liệu sai", check_message),
    ("40 ô và 300 ô trong 2 giây", check_fast),
    ("không dùng thư viện tính tổ hợp", check_no_builtin),
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
