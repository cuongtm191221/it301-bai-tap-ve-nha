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


from doi_soat import same_orders_v1, same_orders_v2, reconcile_message

OURS = ["DH9001", "DH9002", "DH9003", "DH9004", "DH9005"]
CARRIER = ["DH9003", " dh9001", "DH9005", "DH9002", "DH9004 "]
BOTH = [("same_orders_v1", same_orders_v1), ("same_orders_v2", same_orders_v2)]


def check_match():
    for name, f in BOTH:
        assert f(OURS, CARRIER) is True, f"{name}: hai list khác thứ tự, khác cách viết vẫn phải khớp"


def check_count_times():
    for name, f in BOTH:
        assert f(["DH9001", "DH9001", "DH9002"], ["DH9001", "DH9002", "DH9002"]) is False, f"{name}: số lần xuất hiện khác nhau"
        assert f(["DH9001", "DH9001"], ["dh9001 ", "DH9001"]) is True, f"{name}: cùng số lần xuất hiện"


def check_mismatch():
    for name, f in BOTH:
        assert f(OURS, OURS[:4]) is False, f"{name}: khác số đơn"
        assert f(OURS, ["DH9003", "DH9001", "DH9005", "DH9002", "DH9006"]) is False, f"{name}: sai một mã"
        assert f([], []) is True, f"{name}: hai list rỗng"


def check_unchanged():
    for name, f in BOTH:
        a, b = OURS[:], CARRIER[:]
        f(a, b)
        assert a == OURS and b == CARRIER, f"{name} đã sửa list đầu vào"


def check_same_answer():
    import random
    rng = random.Random(5)
    for _ in range(300):
        a = [f"DH{rng.randint(1, 6)}" for _ in range(rng.randint(0, 8))]
        b = a[:]
        rng.shuffle(b)
        if rng.random() < 0.5 and b:
            b[rng.randrange(len(b))] = f"DH{rng.randint(1, 6)}"
        assert same_orders_v1(a, b) == same_orders_v2(a, b), f"hai giải pháp khác nhau với {a} và {b}"


def check_message():
    assert reconcile_message(OURS, CARRIER) == "Khớp 5 đơn."
    assert reconcile_message(OURS, CARRIER[:4]) == "Lệch: số đơn khác nhau (5 và 4)."
    assert reconcile_message(OURS, ["DH9003", "DH9001", "DH9005", "DH9002", "DH9006"]) == "Lệch: có mã đơn không khớp."
    assert reconcile_message([], []) == "Chưa có đơn để đối soát."


def check_message_fast():
    a = [f"DH{i:06d}" for i in range(50000)]
    b = a[::-1]
    box = run_limited(lambda: reconcile_message(a, b), 3, "reconcile_message chạy 50.000 đơn mỗi bên quá 3 giây")
    assert box[0] == "Khớp 50000 đơn."


CHECKS = [
    ("khác thứ tự, khác cách viết vẫn khớp", check_match),
    ("đếm đúng số lần xuất hiện của mỗi mã", check_count_times),
    ("khác số đơn, sai một mã, hai list rỗng", check_mismatch),
    ("không sửa hai list đầu vào", check_unchanged),
    ("hai giải pháp cho cùng kết quả", check_same_answer),
    ("thông báo đối soát", check_message),
    ("thông báo cho 50.000 đơn mỗi bên trong 3 giây", check_message_fast),
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
