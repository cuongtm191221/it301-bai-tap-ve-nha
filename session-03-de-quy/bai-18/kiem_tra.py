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


from ke_hoach import savings_schedule, months_needed, plan_message


def check_schedule():
    assert savings_schedule(0, 2000000, 500000, 100000) == [(1, 500000), (2, 1100000), (3, 1800000), (4, 2600000)]
    assert savings_schedule(6000000, 5000000, 800000, 0) == []


def check_months():
    assert months_needed(1000000, 5000000, 800000, 0) == 5
    assert months_needed(0, 10000000, 500000, 100000) == 11
    assert months_needed(5000000, 5000000, 1, 0) == 0


def check_non_positive():
    assert months_needed(0, 3000000, -200000, 100000) == 11, f"ra {months_needed(0, 3000000, -200000, 100000)}"
    assert months_needed(0, 5000000, 0, 0) is None


def check_limit():
    assert months_needed(0, 500000000, 100000, 0) is None, "5.000 tháng vượt giới hạn 600 tháng"
    assert months_needed(0, 60000000, 100000, 0) == 600, "đúng 600 tháng vẫn đạt"
    box = run_limited(lambda: months_needed(0, 10 ** 12, 1000, 0), 2, "dữ liệu cần rất nhiều tháng phải dừng ở 600 tháng")
    assert box[0] is None


def check_messages():
    assert plan_message(1000000, 5000000, 800000, 0) == "Cần 5 tháng, tháng cuối góp 800.000đ, số dư 5.000.000đ."
    assert plan_message(0, 10000000, 500000, 100000) == "Cần 11 tháng, tháng cuối góp 1.500.000đ, số dư 11.000.000đ."
    assert plan_message(6000000, 5000000, 800000, 0) == "Đã đủ mục tiêu."
    assert plan_message(0, 5000000, 0, 0) == "Không đạt mục tiêu trong 600 tháng, hãy tăng mức góp."
    assert plan_message(0, 0, 100000, 0) == "Dữ liệu không hợp lệ." and plan_message(-1, 100, 1, 0) == "Dữ liệu không hợp lệ."


CHECKS = [
    ("lịch góp từng tháng", check_schedule),
    ("số tháng cần góp", check_months),
    ("mức góp 0 hoặc âm", check_non_positive),
    ("giới hạn 600 tháng", check_limit),
    ("thông báo", check_messages),
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
