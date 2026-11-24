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
from gia_co_phieu import make_prices, make_big_prices, add_price, recent_average, best_trade, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def brute(prices):
    best = None
    for s in range(len(prices)):
        for b in range(s):
            p = prices[s] - prices[b]
            if p > 0 and (best is None or p > best[2]):
                best = (b + 1, s + 1, p)
    return best


def check_sample():
    assert best_trade(make_prices()) == (4, 10, 8100), f"giá mẫu ra {best_trade(make_prices())}"
    assert best_trade([]) is None and best_trade([5000]) is None and best_trade([9000, 8000, 7000]) is None, "không có lãi phải trả None"


def check_ties():
    assert best_trade([5000, 3000, 3000, 6000, 6000]) == (2, 4, 3000), "cùng lãi: bán sớm nhất, mua sớm nhất"
    rng = random.Random(6)
    for _ in range(300):
        prices = [rng.randint(1, 6) * 1000 for _ in range(rng.randint(0, 12))]
        assert best_trade(prices) == brute(prices), f"sai với {prices}"


def check_fast():
    prices = make_big_prices(500000)
    got = run_limited(lambda: best_trade(prices), 1, "500.000 phiên quá 1 giây: phải một lượt duyệt")
    assert got is not None and got[0] < got[1] and got[2] == prices[got[1] - 1] - prices[got[0] - 1]


def check_recent():
    prices = make_prices()
    assert recent_average(prices, 3) == ([102800, 101900, 103500], 102733), f"3 phiên gần nhất ra {recent_average(prices, 3)}"
    assert recent_average(prices, 20)[0] == prices and recent_average([], 3) == ([], None)
    assert prices == make_prices()


def check_add():
    prices = make_prices()
    assert add_price(prices, " 101000 ") == 11 and prices[-1] == 101000
    for bad in ["500", "10000001", "1.5", "abc", "", "-5000"]:
        raises("Giá phải là số nguyên từ 1.000 đến 10.000.000", lambda: add_price(prices, bad))
    assert len(prices) == 11


def check_benchmark():
    rows = run_limited(lambda: benchmark((1000, 2000), number=1), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [1000, 2000] and all(len(r) == 3 and r[1] > 0 for r in rows), f"benchmark ra {rows}"
    assert rows[1][2] > rows[0][2] > 1000 * 8, "byte phải là sys.getsizeof của list giá"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "102.800đ, 101.900đ, 103.500đ", "Trung bình 3 phiên: 102.733đ", "Mua phiên 4, bán phiên 10: lãi 8.100đ mỗi cổ phiếu.",
        "Đã thêm phiên 11.", "Lỗi: Giá phải là số nguyên từ 1.000 đến 10.000.000", "Lỗi: Giá phải là số nguyên từ 1.000 đến 10.000.000",
        "Lỗi: Số phiên phải là số nguyên dương", "Trung bình 11 phiên: 99.790đ",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Lưu ý: số liệu chỉ để học, không phải khuyến nghị đầu tư. Tạm biệt!",
    ])


CHECKS = [
    ("mua bán tốt nhất trên giá mẫu, không có lãi", check_sample),
    ("cùng lãi và 300 dãy giá ngẫu nhiên", check_ties),
    ("500.000 phiên trong 1 giây", check_fast),
    ("k phiên gần nhất và trung bình", check_recent),
    ("thêm giá và dữ liệu sai", check_add),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '2',
    '3',
    '3',
    '1',
    '101000',
    '1',
    '500',
    '1',
    'abc',
    '2',
    '0',
    '2',
    '20',
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
