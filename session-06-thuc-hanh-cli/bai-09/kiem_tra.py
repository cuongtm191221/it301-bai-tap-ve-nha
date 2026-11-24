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


import random
import inspect
import chia_chuyen
from chia_chuyen import make_orders, make_big_orders, batch_slow, batch_fast, add_order, benchmark

EXPECTED = [(["SD01", "SD03", "SD04", "SD06"], 1165000), (["SD07", "SD08"], 659000)]


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_sample():
    orders = make_orders()
    got = batch_fast(orders, 4)
    assert got == EXPECTED, f"4 đơn mỗi chuyến ra {got}"
    assert orders == make_orders(), "batch_fast làm đổi danh sách đơn"
    assert batch_fast(orders, 1) == batch_slow(orders, 1) and batch_fast(orders, 100) == batch_slow(orders, 100)


def check_same():
    rng = random.Random(9)
    for _ in range(200):
        orders = [("SD%02d" % k, rng.choice([0, 0, 1000, 25000, 99000])) for k in range(rng.randint(0, 25))]
        size = rng.randint(1, 6)
        assert batch_fast(orders, size) == batch_slow(orders, size), f"khác bản cũ với {orders}, {size} đơn mỗi chuyến"


def check_errors():
    for bad in (0, -2):
        raises("Số đơn mỗi chuyến phải là số nguyên dương", lambda: batch_fast(make_orders(), bad))
    raises("Số đơn mỗi chuyến phải là số nguyên dương", lambda: batch_fast([], 0))
    assert batch_fast([], 3) == [] and batch_fast([("SD1", 0)], 3) == []


def check_fast():
    body = inspect.getsource(chia_chuyen.batch_fast).split('"""', 2)[-1]
    assert "batch_slow" not in body, "batch_fast không được gọi batch_slow"
    orders = make_big_orders(200000)
    got = run_limited(lambda: batch_fast(orders, 50), 1, "batch_fast với 200.000 đơn quá 1 giây")
    assert len(got) == 3200 and got[0][0][0] == "SD000001" and len(got[-1][0]) == 50, f"200.000 đơn ra {len(got)} chuyến"


def check_add():
    orders = make_orders()
    assert add_order(orders, " sd09 ", " 150000 ") == "SD09" and orders[-1] == ("SD09", 150000)
    raises("Mã đơn đã tồn tại", lambda: add_order(orders, "SD09", "1"))
    for bad in ["XX1", "SD", "SDx1", ""]:
        raises("Mã đơn phải có dạng SD + số", lambda: add_order(orders, bad, "5"))
    for bad in ["-5", "1.5", "abc", ""]:
        raises("Giá trị đơn phải là số nguyên không âm", lambda: add_order(orders, "SD10", bad))
    assert len(orders) == 9
    assert add_order(orders, "SD10", "0") == "SD10"


def check_benchmark():
    rows = run_limited(lambda: benchmark((200, 400)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [200, 400] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "SD02 | 0đ | chưa thanh toán", "Chuyến 1: SD01, SD03, SD04, SD06 | 1.165.000đ", "Chuyến 2: SD07, SD08 | 659.000đ",
        "Tổng: 2 chuyến, 6 đơn.", "Đã thêm SD09 (150.000đ). Có 9 đơn.", "Lỗi: Mã đơn đã tồn tại",
        "Lỗi: Mã đơn phải có dạng SD + số", "Lỗi: Giá trị đơn phải là số nguyên không âm",
        "Lỗi: Số đơn mỗi chuyến phải là số nguyên dương", "Lỗi: Số đơn mỗi chuyến phải là số nguyên dương",
        "Chuyến 2: SD07, SD08, SD09 | 809.000đ", "Tổng: 2 chuyến, 7 đơn.", "n | bản cũ (ms) | bản mới (ms)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã chốt chuyến. Tạm biệt!",
    ])


CHECKS = [
    ("batch_fast trên dữ liệu mẫu, không đổi danh sách đơn", check_sample),
    ("khớp bản cũ trên 200 bộ ngẫu nhiên", check_same),
    ("lỗi số đơn mỗi chuyến, danh sách rỗng", check_errors),
    ("200.000 đơn trong 1 giây, không gọi bản cũ", check_fast),
    ("thêm đơn, dữ liệu sai", check_add),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '4',
    '2',
    'sd09',
    '150000',
    '2',
    'SD09',
    '1',
    '2',
    'XX1',
    '5',
    '2',
    'SD10',
    '-5',
    '3',
    '0',
    '3',
    'abc',
    '3',
    '4',
    '4',
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
