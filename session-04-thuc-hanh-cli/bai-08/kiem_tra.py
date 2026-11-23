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
from combo import make_menu, make_big_prices, count_combos_v1, count_combos_v2, best_combo, benchmark

PRICES = [m[2] for m in make_menu()]


def names(combo):
    return [m[0] for m in combo]


def check_v1():
    got = [count_combos_v1(PRICES, b) for b in (4000, 5000, 20000, 100000, 300000)]
    assert got == [0, 1, 4, 56, 127], f"giải pháp 1 ra {got}"
    assert count_combos_v1([], 100000) == 0


def check_v2():
    got = [count_combos_v2(PRICES, b) for b in (4000, 5000, 20000, 100000, 300000)]
    assert got == [0, 1, 4, 56, 127], f"giải pháp 2 ra {got}"
    prices = PRICES[:]
    count_combos_v1(prices, 100000); count_combos_v2(prices, 100000)
    assert prices == PRICES, "đếm combo làm đổi list giá"


def check_same():
    rng = random.Random(8)
    for _ in range(100):
        prices = [rng.randint(1, 9) * 1000 for _ in range(rng.randint(0, 10))]
        b = rng.randint(0, 30) * 1000
        assert count_combos_v1(prices, b) == count_combos_v2(prices, b), f"hai giải pháp khác kết quả với {prices}, {b}"


def check_v2_fast():
    prices = make_big_prices(40)
    got = run_limited(lambda: count_combos_v2(prices, 200000), 1, "giải pháp 2 với 40 món, 200.000đ quá 1 giây")
    assert got == 314597, f"40 món, 200.000đ ra {got}"


def check_best():
    menu = make_menu()
    assert names(best_combo(menu, 100000)) == ["CT01", "CT05", "CT07"], f"ngân sách 100.000đ ra {names(best_combo(menu, 100000))}"
    assert names(best_combo(menu, 300000)) == [m[0] for m in menu], "ngân sách đủ mua cả thực đơn"
    assert menu == make_menu(), "best_combo làm đổi thực đơn"
    assert best_combo(menu, 4000) == [] and names(best_combo(menu, 5000)) == ["CT04"], "ngân sách nhỏ sai"
    tie = [["A", "a", 10000], ["B", "b", 4000], ["C", "c", 6000], ["D", "d", 10000]]
    assert names(best_combo(tie, 10000)) == ["A"], f"nhiều combo cùng tổng phải chọn ít món, món đứng trước; ra {names(best_combo(tie, 10000))}"


def check_benchmark():
    rows = run_limited(lambda: benchmark((8, 10)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [8, 10] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "CT07 | Sườn thêm | 30.000đ", "Combo 100.000đ (3 món): Cơm tấm sườn, Chả trứng thêm, Sườn thêm", "Có 56 combo trong 100.000đ.", "Có 56 combo trong 100.000đ.",
        "Combo 5.000đ (1 món): Trà đá", "Lỗi: Ngân sách phải là số nguyên từ 10.000 đến 2.000.000", "Lựa chọn không hợp lệ.",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Chúc ngon miệng!",
    ])


CHECKS = [
    ("đếm combo, giải pháp 1", check_v1),
    ("đếm combo, giải pháp 2", check_v2),
    ("hai giải pháp cùng kết quả trên 100 thực đơn ngẫu nhiên", check_same),
    ("giải pháp 2 với 40 món trong 1 giây", check_v2_fast),
    ("combo sát ngân sách nhất", check_best),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    '100000',
    '3',
    '1',
    '100000',
    '3',
    '2',
    '100000',
    '2',
    '10000',
    '2',
    '5000',
    '3',
    '3',
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
