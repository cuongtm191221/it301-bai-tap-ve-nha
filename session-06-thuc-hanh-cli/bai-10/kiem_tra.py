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
import chot_ca
from chot_ca import make_catalog, make_sales, make_big_catalog, make_big_sales, close_slow, close_fast, add_sale, benchmark

EXPECTED = ([47, 0, 0, 0, 8], [3, 4, 5])


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_sample():
    catalog, sales = make_catalog(), make_sales()
    got = close_fast(catalog, sales)
    assert tuple(got) == EXPECTED, f"dữ liệu mẫu ra {got}"
    assert catalog == make_catalog() and sales == make_sales(), "close_fast làm đổi dữ liệu vào"


def check_same():
    rng = random.Random(10)
    for _ in range(200):
        codes = rng.sample(range(0, 30), rng.randint(0, 8))
        catalog = [(c, "H", rng.randint(0, 6)) for c in codes]
        sales = [(rng.randint(0, 30), rng.randint(1, 4)) for _ in range(rng.randint(0, 15))]
        assert tuple(close_fast(catalog, sales)) == tuple(close_slow(catalog, sales)), f"khác bản cũ với {catalog}, {sales}"


def check_edges():
    assert tuple(close_fast([], [(5, 1)])) == ([], [1])
    assert tuple(close_fast([(0, "A", 3), (9999, "B", 2)], [])) == ([3, 2], [])
    assert tuple(close_fast([(0, "A", 3), (9999, "B", 2)], [(9999, 2), (0, 3), (0, 1)])) == ([0, 0], [3]), "mã biên 0000, 9999; bán đúng bằng tồn"


def check_fast():
    body = inspect.getsource(chot_ca.close_fast).split('"""', 2)[-1]
    assert "close_slow" not in body, "close_fast không được gọi close_slow"
    assert "dict(" not in body and "set(" not in body and "{" not in body, "close_fast không được dùng dict, set"
    catalog, sales = make_big_catalog(10000), make_big_sales(200000)
    stocks, rejected = run_limited(lambda: close_fast(catalog, sales), 1, "10.000 mặt hàng, 200.000 giao dịch quá 1 giây")
    assert len(stocks) == 10000 and len(rejected) == 44000 and sum(stocks) == 88000, f"ra {len(rejected)} từ chối, tổng tồn {sum(stocks)}"


def check_add():
    sales = make_sales()
    assert add_sale(sales, " 4500 ", " 3 ") == (4500, 3) and sales[-1] == (4500, 3)
    assert add_sale(sales, "0007", "1") == (7, 1)
    for bad in ["45", "12345", "45a0", ""]:
        raises("Mã hàng phải gồm 4 chữ số", lambda: add_sale(sales, bad, "1"))
    for bad in ["0", "-2", "1.5", "abc", ""]:
        raises("Số lượng phải là số nguyên dương", lambda: add_sale(sales, "1001", bad))
    assert len(sales) == 9


def check_benchmark():
    rows = run_limited(lambda: benchmark((100, 200)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [100, 200] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "3010 | Gạo ST25 5kg | tồn 5", "1001 | Mì Hảo Hảo | còn 47", "4500 | Dầu ăn Neptune 1L | còn 8",
        "Giao dịch bị từ chối: 3, 4, 5", "Đã ghi giao dịch 8: 4500 x 3.", "Lỗi: Mã hàng phải gồm 4 chữ số",
        "Lỗi: Số lượng phải là số nguyên dương", "Lỗi: Số lượng phải là số nguyên dương", "4500 | Dầu ăn Neptune 1L | còn 5",
        "Giao dịch bị từ chối: 3, 4, 5", "n | bản cũ (ms) | bản mới (ms)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã chốt sổ. Tạm biệt!",
    ])


CHECKS = [
    ("close_fast trên dữ liệu mẫu, không đổi dữ liệu vào", check_sample),
    ("khớp bản cũ trên 200 bộ ngẫu nhiên", check_same),
    ("danh mục rỗng, không giao dịch, mã biên, bán đúng bằng tồn", check_edges),
    ("10.000 mặt hàng, 200.000 giao dịch trong 1 giây; không gọi bản cũ, không dict, set", check_fast),
    ("ghi giao dịch, dữ liệu sai", check_add),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '2',
    '4500',
    '3',
    '2',
    '45',
    '1',
    '2',
    '1001',
    '0',
    '2',
    '1001',
    'abc',
    '3',
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
