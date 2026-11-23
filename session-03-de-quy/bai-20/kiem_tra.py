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
import tra_gop
from tra_gop import count_plans_slow, count_plans, count_plans_limited, plan_report


def check_small():
    for amount in range(0, 16):
        assert count_plans(amount) == count_plans_slow(amount), f"lệch với bản cũ ở {amount} triệu"
    assert count_plans(-1) == 0


def check_large():
    box = run_limited(lambda: (count_plans(30), count_plans(3000)), 2, "khoản 30 và 3.000 triệu tính quá 2 giây")
    assert box[0][0] == 53798080
    assert len(str(box[0][1])) == 794, "khoản 3.000 triệu sai"


def check_limited():
    assert count_plans_limited(5, 3) == 8, count_plans_limited(5, 3)
    assert count_plans_limited(5, 5) == count_plans(5)
    assert count_plans_limited(10, 3) == 0 and count_plans_limited(0, 0) == 1
    box = run_limited(lambda: count_plans_limited(200, 120), 2, "khoản 200 triệu, tối đa 120 kỳ tính quá 2 giây")
    assert box[0] > 0


def check_report():
    lines = plan_report([1, 3, 5, 0, -2], 3)
    assert lines[0] == "Khoản 1 triệu: 1 cách trả, 1 cách trong tối đa 3 kỳ."
    assert lines[2] == "Khoản 5 triệu: 13 cách trả, 8 cách trong tối đa 3 kỳ.", lines[2]
    assert lines[3] == "Khoản 0 triệu: số tiền không hợp lệ." and lines[4] == "Khoản -2 triệu: số tiền không hợp lệ."
    assert plan_report([4], 0) == ["Khoản 4 triệu: số kỳ tối đa không hợp lệ."]


def check_slow_kept():
    src = inspect.getsource(count_plans)
    assert "count_plans_slow(" not in src, "count_plans không được gọi lại bản cũ"


CHECKS = [
    ("khớp bản cũ với khoản nhỏ", check_small),
    ("khoản 30 và 3.000 triệu", check_large),
    ("giới hạn số kỳ", check_limited),
    ("báo cáo", check_report),
    ("không gọi lại bản cũ", check_slow_kept),
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
