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
import cong_thuc
from cong_thuc import Shop, eval_v1, eval_v2, set_formula, promo_prices, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def outcome(task):
    try:
        return ("ok", task())
    except ValueError as error:
        return ("lỗi", str(error))


CASES = [
    ("gia 90 * 100 /", 250000, 225000), ("gia 20000 -", 250000, 230000), ("gia", 7, 7), ("5 3 - 2 *", 0, 4),
    ("gia 3 + 2 * 1 - 4 /", 1000, 501), ("10 3 /", 0, 3), ("2 3 4 * +", 0, 14), ("gia 1000 - 50000 +", 120000, 169000),
]
ERRORS = [("gia +", "Biểu thức không hợp lệ"), ("1 2", "Biểu thức không hợp lệ"), ("+", "Biểu thức không hợp lệ"),
          ("", "Biểu thức không hợp lệ"), ("gia 10 % -", "Biểu thức không hợp lệ"), ("gia 0 /", "Không chia được cho 0"),
          ("1 0 / +", "Không chia được cho 0"), ("1 + 0 /", "Biểu thức không hợp lệ"), ("gia -5 +", "Biểu thức không hợp lệ")]


def check_v1():
    for text, price, want in CASES:
        assert eval_v1(text, price) == want, f"eval_v1({text!r}, {price}) ra {eval_v1(text, price)}, cần {want}"
    for text, message in ERRORS:
        raises(message, lambda: eval_v1(text, 100))


def check_v2():
    for text, price, want in CASES:
        assert eval_v2(text, price) == want, f"eval_v2({text!r}, {price}) ra {eval_v2(text, price)}, cần {want}"
    for text, message in ERRORS:
        raises(message, lambda: eval_v2(text, 100))


def check_same():
    rng = random.Random(8)
    pool = ["gia", "0", "1", "2", "7", "+", "-", "*", "/", "+", "*"]
    for _ in range(300):
        text = " ".join(rng.choice(pool) for _ in range(rng.randint(1, 9)))
        price = rng.randint(0, 50)
        a, b = outcome(lambda: eval_v1(text, price)), outcome(lambda: eval_v2(text, price))
        assert a == b, f"công thức {text!r}, gia = {price}: giải pháp 1 ra {a}, giải pháp 2 ra {b}"


def check_fast():
    formula = "gia" + " 1 +" * 100000
    got = run_limited(lambda: eval_v2(formula, 5), 1, "giải pháp 2 với công thức 200.001 phần quá 1 giây")
    assert got == 100005


def check_shop():
    shop = Shop()
    assert [p[3] for p in promo_prices(shop)] == [250000, 480000, 120000]
    assert set_formula(shop, "  gia   90 *  100 / ") == "gia 90 * 100 /" and [p[3] for p in promo_prices(shop)] == [225000, 432000, 108000]
    raises("Giá sau khuyến mãi của SP03 bị âm", lambda: set_formula(shop, "gia 200000 -"))
    raises("Biểu thức không hợp lệ", lambda: set_formula(shop, "gia 10 % -"))
    raises("Không chia được cho 0", lambda: set_formula(shop, "gia 0 /"))
    assert shop.formula == "gia 90 * 100 /", "công thức lỗi phải giữ công thức cũ"


def check_benchmark():
    rows = run_limited(lambda: benchmark((100, 200)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [100, 200] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Công thức: gia", "SP01 | Áo thun | 250.000đ -> 250.000đ", "Đã áp dụng: gia 90 * 100 /", "SP02 | Quần jean | 480.000đ -> 432.000đ",
        "Lỗi: Giá sau khuyến mãi của SP03 bị âm", "Lỗi: Biểu thức không hợp lệ", "Lỗi: Không chia được cho 0", "Kết quả: 501đ",
        "Lỗi: Biểu thức không hợp lệ", "Đã áp dụng: gia 1000 - 50000 +", "SP03 | Mũ lưỡi trai | 120.000đ -> 169.000đ",
        "Lựa chọn không hợp lệ.", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã lưu công thức. Tạm biệt!",
    ])


CHECKS = [
    ("giải pháp 1: kết quả và lỗi", check_v1),
    ("giải pháp 2: kết quả và lỗi", check_v2),
    ("hai giải pháp trên 300 công thức ngẫu nhiên", check_same),
    ("giải pháp 2 với công thức 200.001 phần", check_fast),
    ("đổi công thức, giá âm, giữ công thức cũ khi lỗi", check_shop),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    'gia   90 * 100 /',
    '1',
    '2',
    'gia 200000 -',
    '2',
    'gia 10 % -',
    '3',
    '1',
    'gia 0 /',
    '500',
    '3',
    '2',
    'gia 3 + 2 * 1 - 4 /',
    '1000',
    '3',
    '2',
    'gia +',
    '1000',
    '2',
    'gia 1000 - 50000 +',
    '1',
    '3',
    'x',
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
