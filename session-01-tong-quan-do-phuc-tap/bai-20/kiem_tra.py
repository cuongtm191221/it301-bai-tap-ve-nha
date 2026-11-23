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


import copy
import random
from bao_cao_ngay import daily_report, daily_report_fast


def sample():
    return [
        {"code": "DH01", "buyer": "an", "amount": 300000},
        {"code": "DH02", "buyer": "binh", "amount": 1500000},
        {"code": "DH03", "buyer": "an", "amount": 200000},
        {"code": "DH04", "buyer": "chi", "amount": 250000},
        {"code": "DH05", "buyer": "binh", "amount": 100000},
        {"code": "DH06", "buyer": "dung", "amount": 1600000},
        {"code": "DH07", "buyer": "an", "amount": 150000},
    ]


def check_example():
    want = {"total": 4100000, "buyers": 4, "best_buyer": "binh", "big_orders": ["DH02", "DH06"], "largest": "DH06"}
    got = daily_report_fast(sample())
    assert got == want, f"ví dụ ra {got}"


def check_unchanged():
    orders = sample()
    daily_report_fast(orders)
    assert orders == sample(), "daily_report_fast không được sửa list orders"


def check_empty():
    want = {"total": 0, "buyers": 0, "best_buyer": None, "big_orders": [], "largest": None}
    assert daily_report_fast([]) == want, f"ngày chưa có đơn ra {daily_report_fast([])}"


def check_same_as_old():
    rng = random.Random(1)
    for _ in range(400):
        data = [{"code": f"DH{i}", "buyer": rng.choice("abcde"), "amount": rng.choice([100, 200, 300, 500, 1000])} for i in range(rng.randint(1, 15))]
        old = daily_report(copy.deepcopy(data))
        new = daily_report_fast(data)
        assert old == new, f"khác bản đang chạy với {data}: {new} so với {old}"


def check_speed():
    rng = random.Random(2)
    big = [{"code": f"DH{i}", "buyer": f"k{rng.randint(1, 50000)}", "amount": rng.randint(1, 2000) * 1000} for i in range(200000)]
    box = run_limited(lambda: daily_report_fast(big), 3, "200.000 đơn chạy quá 3 giây")


CHECKS = [
    ("ví dụ 7 đơn, khách bằng tiền nhau", check_example),
    ("không sửa list orders", check_unchanged),
    ("ngày chưa có đơn", check_empty),
    ("cùng kết quả với bản đang chạy", check_same_as_old),
    ("200.000 đơn trong 3 giây", check_speed),
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
