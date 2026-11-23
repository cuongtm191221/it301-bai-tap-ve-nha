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


from chia_lo import split_batches, COMPLEXITY


def check_example():
    assert split_batches(10000, 500) == (5, 313), f"10.000 đơn ra {split_batches(10000, 500)}"


def check_integer():
    result = split_batches(1000000, 500)
    assert result == (11, 489), f"1.000.000 đơn ra {result}"
    assert isinstance(result[1], int), "số đơn của lô phải là số nguyên"


def check_exact_capacity():
    assert split_batches(1000, 500) == (1, 500), f"1.000 đơn, lô tối đa 500 ra {split_batches(1000, 500)}"
    assert split_batches(500, 500) == (0, 500), f"500 đơn, lô tối đa 500 ra {split_batches(500, 500)}"
    assert split_batches(300, 500) == (0, 300), f"300 đơn ra {split_batches(300, 500)}"


def check_no_order_lost():
    for n in (7, 999, 10001, 123457):
        splits, size = split_batches(n, 10)
        assert size * 2 ** splits >= n, f"{n} đơn: {2 ** splits} lô, mỗi lô {size} đơn thì không chứa đủ"


def check_bad_capacity():
    box = run_limited(lambda: (split_batches(100, 0), split_batches(100, -5)), 2, "hàm không dừng khi lô tối đa không dương")
    assert box[0] == (None, None), f"lô tối đa 0 và -5 ra {box[0]}"


def check_complexity():
    assert COMPLEXITY.replace(" ", "") == "O(logn)", f"Big-O ghi là {COMPLEXITY}"


CHECKS = [
    ("ví dụ 10.000 đơn", check_example),
    ("số đơn của lô là số nguyên", check_integer),
    ("đúng bằng lô tối đa thì không chia nữa", check_exact_capacity),
    ("không đơn nào bị mất", check_no_order_lost),
    ("lô tối đa không dương: trả về None và dừng", check_bad_capacity),
    ("Big-O ghi đúng", check_complexity),
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
