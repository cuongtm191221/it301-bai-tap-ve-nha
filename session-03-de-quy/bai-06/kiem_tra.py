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
from giao_dich_lon import largest


def check_sample():
    june = [150000, 2500000, 49000, 1000000, 320000]
    assert largest(june) == 2500000, f"ra {largest(june)}"
    assert largest([75000]) == 75000


def check_empty():
    assert largest([]) is None, "list rỗng phải trả về None"


def check_growing():
    data = [10000 * k for k in range(1, 31)]
    box = run_limited(lambda: largest(data), 1, "30 giao dịch tăng dần tính quá 1 giây")
    assert box[0] == 300000, f"ra {box[0]}"


def check_long():
    data = [5000000 - 1000 * k for k in range(500)]
    assert largest(data) == 5000000, f"500 giao dịch giảm dần ra {largest(data)}"


def check_unchanged():
    data = [3, 9, 1]
    largest(data)
    assert data == [3, 9, 1], "không được sửa list đầu vào"
    src = inspect.getsource(largest)
    assert "max(" not in src and "for " not in src and "while " not in src, "giữ cách viết đệ quy, không dùng max() hay vòng lặp"


CHECKS = [
    ("dữ liệu tháng 6", check_sample),
    ("tháng chưa có giao dịch", check_empty),
    ("30 giao dịch tăng dần trong 1 giây", check_growing),
    ("500 giao dịch giảm dần", check_long),
    ("không sửa list, giữ đệ quy", check_unchanged),
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
