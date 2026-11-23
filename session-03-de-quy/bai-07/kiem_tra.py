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


from tiet_kiem_online import balance_after, history


def check_one_year():
    assert balance_after(10000000, 6, 1) == 10600000


def check_compound():
    got = balance_after(10000000, 6, 3)
    assert got == 11910160, f"3 năm ra {got}, mong đợi 11910160 (lãi tính trên số dư đầu năm)"


def check_zero_years():
    assert balance_after(10000000, 6, 0) == 10000000, "0 năm phải trả về số tiền gửi"


def check_history():
    got = history(10000000, 6, 3)
    assert got == [10000000, 10600000, 11236000, 11910160], f"lịch sử ra {got}"
    assert history(5000000, 5, 0) == [5000000]


def check_rounding():
    assert balance_after(999, 7, 2) == 1142, f"999đ, lãi 7%, 2 năm ra {balance_after(999, 7, 2)}, mong đợi 1142 (làm tròn xuống từng năm)"


CHECKS = [
    ("1 năm", check_one_year),
    ("3 năm lãi kép", check_compound),
    ("0 năm", check_zero_years),
    ("lịch sử số dư", check_history),
    ("làm tròn xuống từng năm", check_rounding),
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
