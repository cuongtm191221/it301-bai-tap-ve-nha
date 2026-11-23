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
from chi_tieu import total_amount, count_large

MONTH = [150000, 2500000, 49000, 1000000, 320000]


def check_total():
    assert total_amount(MONTH) == 4019000, f"5 giao dịch ra {total_amount(MONTH)}"
    assert total_amount([75000]) == 75000 and total_amount([75000, 25000]) == 100000


def check_total_empty():
    assert total_amount([]) == 0, "tháng chưa có giao dịch phải trả về 0"


def check_large():
    assert count_large(MONTH, 1000000) == 2, f"giao dịch từ 1.000.000đ ra {count_large(MONTH, 1000000)}"
    assert count_large([], 1000000) == 0


def check_unchanged_and_recursive():
    data = MONTH[:]
    total_amount(data)
    count_large(data, 1000000)
    assert data == MONTH, "không được sửa list giao dịch"
    for f in (total_amount, count_large):
        src = inspect.getsource(f)
        assert "for " not in src and "while " not in src and "sum(" not in src, f"{f.__name__} phải viết bằng đệ quy, không dùng vòng lặp hay sum()"


CHECKS = [
    ("tổng chi tiêu", check_total),
    ("tháng chưa có giao dịch", check_total_empty),
    ("đếm giao dịch từ ngưỡng trở lên", check_large),
    ("không sửa list, viết bằng đệ quy", check_unchanged_and_recursive),
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
