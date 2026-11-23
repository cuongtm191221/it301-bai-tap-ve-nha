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
import doi_tien
from doi_tien import count_ways_v1, count_ways_v2, fewest_notes, benchmark


def recursive_only(func):
    body = inspect.getsource(func).split('"""', 2)[-1]
    assert func.__name__ + "(" in body, f"{func.__name__} phải gọi lại chính nó (đệ quy)"
    assert "for " not in body and "while " not in body, f"{func.__name__} không được dùng vòng lặp"


def check_v1():
    got = [count_ways_v1(a) for a in (10000, 20000, 50000, 100000, 500000)]
    assert got == [1, 2, 4, 11, 451], f"giải pháp 1 ra {got}"
    recursive_only(doi_tien.count_ways_v1)


def check_v2():
    count_ways_v2.cache_clear() if hasattr(count_ways_v2, "cache_clear") else None
    got = [count_ways_v2(a) for a in (10000, 20000, 50000, 100000, 500000)]
    assert got == [1, 2, 4, 11, 451], f"giải pháp 2 ra {got}"


def check_same():
    rng = random.Random(4)
    for _ in range(30):
        a = rng.randint(1, 80) * 10000
        assert count_ways_v1(a) == count_ways_v2(a), f"hai giải pháp khác kết quả với {a}"


def check_v2_fast():
    if hasattr(count_ways_v2, "cache_clear"):
        count_ways_v2.cache_clear()
    got = run_limited(lambda: count_ways_v2(3000000), 1, "giải pháp 2 với 3.000.000đ quá 1 giây")
    assert got == 393119, f"3.000.000đ ra {got}"


def check_fewest():
    assert fewest_notes(1780000) == [(500000, 3), (200000, 1), (50000, 1), (20000, 1), (10000, 1)], f"1.780.000đ ra {fewest_notes(1780000)}"
    assert fewest_notes(10000) == [(10000, 1)] and fewest_notes(0) == []
    recursive_only(doi_tien.fewest_notes)


def check_benchmark():
    rows = run_limited(lambda: benchmark((100000, 200000)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [100000, 200000] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Chưa có lượt đổi nào.", "Đổi: 3 tờ 500.000đ, 1 tờ 200.000đ, 1 tờ 50.000đ, 1 tờ 20.000đ, 1 tờ 10.000đ",
        "Có 451 cách đổi 500.000đ.", "Có 393119 cách đổi 3.000.000đ.",
        "Lỗi: Số tiền phải là bội của 10.000đ, từ 10.000đ đến 3.000.000đ", "Lỗi: Số tiền phải là bội của 10.000đ, từ 10.000đ đến 3.000.000đ",
        "Lựa chọn không hợp lệ.", "Đã đổi: 1.780.000đ", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.",
        "Chúc mừng năm mới! Hẹn gặp lại.",
    ])


CHECKS = [
    ("số cách đổi, giải pháp 1 (đệ quy)", check_v1),
    ("số cách đổi, giải pháp 2", check_v2),
    ("hai giải pháp cùng kết quả trên 30 số tiền ngẫu nhiên", check_same),
    ("giải pháp 2 với 3.000.000đ trong 1 giây", check_v2_fast),
    ("phương án ít tờ nhất (đệ quy)", check_fewest),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '3',
    '1',
    '1780000',
    '2',
    '1',
    '500000',
    '2',
    '2',
    '3000000',
    '1',
    '15000',
    '1',
    '3500000',
    '2',
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
