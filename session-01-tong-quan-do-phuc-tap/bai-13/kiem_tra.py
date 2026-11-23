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


from van_don import has_duplicate_v1, has_duplicate_v2, print_check_message

BOTH = [("has_duplicate_v1", has_duplicate_v1), ("has_duplicate_v2", has_duplicate_v2)]


def check_no_duplicate():
    for name, f in BOTH:
        assert f(["SPX0001", "SPX0002", "SPX0003", "SPX0004", "SPX0005"]) is False, name


def check_normalize():
    for name, f in BOTH:
        assert f(["SPX0001", " spx0002", "SPX0003", "SPX0002 "]) is True, f"{name}: mã viết thường hoặc thừa khoảng trắng vẫn là trùng"


def check_ends():
    for name, f in BOTH:
        assert f(["SPX0009", "SPX0001", "SPX0002", "SPX0009"]) is True, f"{name}: mã trùng ở hai đầu"
        assert f(["SPX0001", "SPX0002", "SPX0003", "SPX0003"]) is True, f"{name}: mã trùng ở hai vị trí cuối"


def check_small_and_unchanged():
    for name, f in BOTH:
        assert f([]) is False and f(["SPX0001"]) is False, f"{name}: lô rỗng hoặc 1 vận đơn"
        data = ["SPX0003", " spx0001", "SPX0002"]
        f(data)
        assert data == ["SPX0003", " spx0001", "SPX0002"], f"{name} đã sửa list đầu vào"


def check_same_answer():
    import random
    rng = random.Random(7)
    for _ in range(300):
        data = [f"SPX{rng.randint(1, 40):04d}" for _ in range(rng.randint(0, 12))]
        assert has_duplicate_v1(data) == has_duplicate_v2(data), f"hai giải pháp cho kết quả khác nhau với {data}"


def check_message():
    assert print_check_message(["SPX0001", "SPX0002", "SPX0003", "SPX0004", "SPX0005"]) == "Không có mã trùng, in 5 vận đơn."
    assert print_check_message(["SPX0001", " spx0002", "SPX0003", "SPX0002 "]) == "Phát hiện mã vận đơn trùng, dừng in."
    assert print_check_message([]) == "Chưa có vận đơn để in."


def check_message_fast():
    big = [f"SPX{i:06d}" for i in range(100000)]
    box = run_limited(lambda: print_check_message(big), 3, "print_check_message chạy lô 100.000 vận đơn quá 3 giây")
    assert box[0] == "Không có mã trùng, in 100000 vận đơn."


CHECKS = [
    ("lô không có mã trùng", check_no_duplicate),
    ("chuẩn hóa mã trước khi so", check_normalize),
    ("mã trùng ở hai đầu và ở cuối", check_ends),
    ("lô rỗng, 1 vận đơn, không sửa list đầu vào", check_small_and_unchanged),
    ("hai giải pháp cho cùng kết quả", check_same_answer),
    ("thông báo trước khi in", check_message),
    ("thông báo cho lô 100.000 vận đơn trong 3 giây", check_message_fast),
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
