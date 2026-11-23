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


import random
from the_qua import clean_values, count_pay_ways_v1, count_pay_ways_v2, pay_ways_message

BOTH = [("count_pay_ways_v1", count_pay_ways_v1), ("count_pay_ways_v2", count_pay_ways_v2)]


def check_clean():
    assert clean_values([50, 20, 10, 20]) == [10, 20, 50]
    assert clean_values([0, -10, 30, 20]) == [20, 30]
    assert clean_values([]) == []


def check_small():
    for name, f in BOTH:
        assert f(100, [10, 20, 50]) == 10, f"{name}(100, [10, 20, 50]) ra {f(100, [10, 20, 50])}"
        assert f(35, [10, 20]) == 0, name
        assert f(0, [10, 20]) == 1, f"{name}: số tiền 0 có đúng 1 cách (không dùng thẻ nào)"


def check_dirty_values():
    for name, f in BOTH:
        assert f(100, [50, 20, 10, 20]) == 10, f"{name}: mệnh giá lặp lại chỉ tính một lần"
        assert f(60, [0, -10, 20, 30]) == 2, f"{name}: bỏ mệnh giá 0 và âm"


def check_same_answer():
    rng = random.Random(3)
    for _ in range(150):
        values = [rng.choice([5, 10, 20, 30, 50]) for _ in range(rng.randint(0, 4))]
        amount = rng.randint(0, 120)
        assert count_pay_ways_v1(amount, values) == count_pay_ways_v2(amount, values), f"hai giải pháp khác nhau với {amount}, {values}"


def check_message():
    assert pay_ways_message(100, [10, 20, 50]) == "Có 10 cách ghép 100 nghìn đồng từ các thẻ 10, 20, 50."
    assert pay_ways_message(35, [10, 20]) == "Không ghép được 35 nghìn đồng từ các thẻ hiện có."
    assert pay_ways_message(0, [10]) == "Số tiền không hợp lệ." and pay_ways_message(-20, [10]) == "Số tiền không hợp lệ."


def check_fast():
    box = run_limited(lambda: pay_ways_message(1000, [1, 2, 5, 10, 20, 50]), 2, "số tiền 1.000 nghìn đồng tính quá 2 giây")
    assert box[0] == "Có 103119386 cách ghép 1000 nghìn đồng từ các thẻ 1, 2, 5, 10, 20, 50.", box[0]


CHECKS = [
    ("làm sạch mệnh giá", check_clean),
    ("ví dụ nhỏ trên cả hai giải pháp", check_small),
    ("mệnh giá lặp, mệnh giá 0 và âm", check_dirty_values),
    ("hai giải pháp cùng kết quả", check_same_answer),
    ("thông báo", check_message),
    ("1.000 nghìn đồng trong 2 giây", check_fast),
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
