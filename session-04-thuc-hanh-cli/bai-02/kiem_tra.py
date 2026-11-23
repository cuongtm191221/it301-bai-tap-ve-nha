"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Các mục đầu kiểm tra hàm nghiệp vụ; mục cuối chạy main.py, tự gõ lần lượt các phím trong KEYS
(cuối tệp) và kiểm tra các dòng thông báo bắt buộc xuất hiện đúng thứ tự. Không sửa tệp này.
"""
import os as _os
import subprocess as _sp
import sys as _sys
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
    return box[0]


def run_cli(seconds=10):
    """Chạy python main.py, tự gõ các phím trong KEYS (mỗi dòng một lần Enter); trả về toàn bộ chữ in ra."""
    keys = "\n".join(KEYS) + "\n"
    env = dict(_os.environ, PYTHONIOENCODING="utf-8")
    try:
        r = _sp.run([_sys.executable, "main.py"], input=keys, capture_output=True, text=True,
                    encoding="utf-8", timeout=seconds, env=env)
    except _sp.TimeoutExpired:
        raise AssertionError("main.py không dừng: kiểm tra chức năng Thoát và vòng lặp menu")
    if "NotImplementedError" in r.stderr:
        raise NotImplementedError
    assert "Traceback" not in r.stderr, "main.py dừng vì lỗi: " + r.stderr.strip().split("\n")[-1]
    return r.stdout


def appear_in_order(out, lines):
    """Mỗi dòng trong lines phải xuất hiện trong out, theo đúng thứ tự."""
    pos = 0
    for line in lines:
        k = out.find(line, pos)
        assert k >= 0, f'không thấy "{line}" (hoặc xuất hiện sai thứ tự)'
        pos = k + len(line)


import inspect
import tiet_kiem
from tiet_kiem import balance_after, months_to_reach, yearly_table


def recursive_only(func):
    body = inspect.getsource(func).split('"""', 2)[-1]
    assert func.__name__ + "(" in body, f"{func.__name__} phải gọi lại chính nó (đệ quy)"
    assert "for " not in body and "while " not in body, f"{func.__name__} không được dùng vòng lặp"


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_balance():
    assert balance_after(100000000, 650, 0) == 100000000, "0 tháng phải giữ nguyên tiền gửi"
    assert balance_after(100000000, 650, 1) == 100541666, f"1 tháng ra {balance_after(100000000, 650, 1)}"
    assert balance_after(100000000, 650, 12) == 106697178, f"12 tháng ra {balance_after(100000000, 650, 12)}"
    assert balance_after(5000000, 0, 24) == 5000000, "lãi 0% phải giữ nguyên"
    recursive_only(tiet_kiem.balance_after)


def check_months():
    assert months_to_reach(100000000, 650, 100000000) == 0, "đã đạt mục tiêu phải trả 0"
    assert months_to_reach(100000000, 650, 120000000) == 34, f"ra {months_to_reach(100000000, 650, 120000000)}"
    recursive_only(tiet_kiem.months_to_reach)


def check_never():
    raises("Số dư không tăng, không bao giờ đạt mục tiêu", lambda: months_to_reach(1000000, 0, 2000000))
    raises("Số dư không tăng, không bao giờ đạt mục tiêu", lambda: months_to_reach(100000, 1, 200000))


def check_too_long():
    got = run_limited(lambda: _catch(lambda: months_to_reach(1000000, 650, 10000000000)), 2, "quá 2 giây")
    assert got == "Cần hơn 600 tháng để đạt mục tiêu", f'cần hơn 600 tháng phải báo đúng lỗi (không được RecursionError), ra "{got}"'


def _catch(task):
    try:
        return task()
    except Exception as error:
        return str(error) if isinstance(error, ValueError) else type(error).__name__


def check_table():
    got = yearly_table(100000000, 650, 3)
    assert got == [106697178, 113842881, 121467143], f"bảng 3 năm ra {got}"
    assert yearly_table(100000000, 650, 0) == []
    assert len(yearly_table(1000000, 2000, 50)) == 50, "50 năm phải chạy được"
    recursive_only(tiet_kiem.yearly_table)


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Chưa nhập tiền gửi và lãi suất (chức năng 1).", "Đã lưu: gửi 100.000.000đ, lãi 6.50%/năm.",
        "Sau 12 tháng: 106.697.178đ", "Cần 34 tháng để đạt 120.000.000đ.", "Năm 3: 121.467.143đ",
        "Lỗi: Số tiền phải là số nguyên từ 1.000.000 đến 10.000.000.000", "Đã lưu: gửi 1.000.000đ, lãi 0.00%/năm.",
        "Lỗi: Số dư không tăng, không bao giờ đạt mục tiêu", "Lỗi: Số tháng phải là số nguyên từ 1 đến 600",
        "Lỗi: Lãi suất phải từ 0 đến 20 (%/năm), tối đa 2 chữ số thập phân",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Cảm ơn quý khách đã sử dụng dịch vụ Techcombank!",
    ])


CHECKS = [
    ("số dư sau n tháng (đệ quy)", check_balance),
    ("số tháng để đạt mục tiêu (đệ quy)", check_months),
    ("số dư không tăng thì dừng ngay, không đệ quy vô hạn", check_never),
    ("cần hơn 600 tháng: báo lỗi, không RecursionError", check_too_long),
    ("bảng số dư cuối mỗi năm (đệ quy)", check_table),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '2',
    '1',
    '100000000',
    '6,5',
    '2',
    '12',
    '3',
    '120000000',
    '4',
    '3',
    '3',
    '100000000000',
    '1',
    '1000000',
    '0',
    '3',
    '2000000',
    '2',
    '601',
    '1',
    '5000000',
    '25',
    'abc',
    '5',
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
