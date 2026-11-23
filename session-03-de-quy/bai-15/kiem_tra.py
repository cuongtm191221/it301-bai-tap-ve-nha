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


from chi_tieu_nhom import total_spending, count_transactions, deepest_level


def check_ai_total():
    assert total_spending([120000, [45000, 30000], 15000]) == 210000


def check_ai_count():
    assert count_transactions([120000, 45000, 15000]) == 3


def check_ai_depth():
    assert deepest_level([120000, [45000, [30000]]]) == 3


def check_ai_empty():
    assert total_spending([]) == 0


CHECKS = [
    ("tổng chi tiêu có nhóm con", check_ai_total),
    ("đếm giao dịch", check_ai_count),
    ("số cấp sâu nhất", check_ai_depth),
    ("tháng chưa có giao dịch", check_ai_empty),
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
