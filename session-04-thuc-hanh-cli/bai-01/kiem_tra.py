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
import tich_diem
from tich_diem import make_bills, total_points, count_big, largest, add_bill


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


def check_points():
    assert total_points(make_bills()) == 51, f"điểm mẫu ra {total_points(make_bills())}"
    assert total_points([]) == 0 and total_points([9999]) == 0 and total_points([10000]) == 1, "rỗng, dưới 10.000, đúng 10.000"
    recursive_only(tich_diem.total_points)


def check_count():
    bills = make_bills()
    assert [count_big(bills, t) for t in (60000, 65000, 300000)] == [3, 3, 0], "đếm hóa đơn lớn sai (bằng ngưỡng là tính)"
    assert count_big([], 1) == 0
    recursive_only(tich_diem.count_big)


def check_largest():
    assert largest(make_bills()) == 210000 and largest([]) is None and largest([7000]) == 7000, "hóa đơn lớn nhất sai"
    assert largest([5, 9, 9, 1]) == 9
    recursive_only(tich_diem.largest)
    assert "max(" not in inspect.getsource(tich_diem.largest).split(chr(34) * 3, 2)[-1], "largest không được dùng max()"


def check_not_changed():
    bills = make_bills()
    total_points(bills); count_big(bills, 1); largest(bills)
    assert bills == make_bills(), "các hàm tính toán làm đổi lịch sử"


def check_add():
    bills = make_bills()
    assert add_bill(bills, " 95000 ") == 95000 and bills[-1] == 95000, "thêm hóa đơn sai"
    for bad in ["500", "5000001", "12.5", "-1000", "abc", ""]:
        raises("Số tiền phải là số nguyên từ 1.000 đến 5.000.000", lambda: add_bill(bills, bad))
    assert len(bills) == 7


def check_long():
    bills = [10000] * 500
    got = run_limited(lambda: (total_points(bills), count_big(bills, 10000), largest(bills)), 2, "500 hóa đơn quá 2 giây")
    assert got == (500, 500, 10000), f"500 hóa đơn ra {got}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "6. 65.000đ", "Điểm: 51 - Hạng: Bạc", "Đã thêm hóa đơn 95.000đ. Điểm mới: 60.", "Có 4 hóa đơn từ 60.000đ trở lên.",
        "Hóa đơn lớn nhất: 210.000đ", "Lỗi: Số tiền phải là số nguyên từ 1.000 đến 5.000.000",
        "Lỗi: Số tiền phải là số nguyên từ 1.000 đến 5.000.000", "Lỗi: Ngưỡng phải là số nguyên dương", "7. 95.000đ",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Cảm ơn quý khách. Hẹn gặp lại!",
    ])


CHECKS = [
    ("tổng điểm (đệ quy)", check_points),
    ("đếm hóa đơn lớn (đệ quy)", check_count),
    ("hóa đơn lớn nhất (đệ quy)", check_largest),
    ("không làm đổi lịch sử", check_not_changed),
    ("thêm hóa đơn và dữ liệu sai", check_add),
    ("lịch sử 500 hóa đơn", check_long),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    '95000',
    '3',
    '60000',
    '4',
    '2',
    '500',
    '2',
    '12.5',
    '3',
    'abc',
    '1',
    'x',
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
