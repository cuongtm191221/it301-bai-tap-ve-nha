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
import xep_pallet
from xep_pallet import ways_naive, count_calls, ways_cached, ways_loop, ways, layouts, benchmark


def recursive_only(func):
    body = inspect.getsource(func).split('"""', 2)[-1]
    assert func.__name__ + "(" in body, f"{func.__name__} phải gọi lại chính nó (đệ quy)"
    assert "for " not in body and "while " not in body, f"{func.__name__} không được dùng vòng lặp"


def check_naive():
    assert [ways_naive(n) for n in range(1, 9)] == [1, 2, 3, 5, 8, 13, 21, 34], "ways_naive sai"
    recursive_only(xep_pallet.ways_naive)


def check_calls():
    assert [count_calls(n) for n in (1, 2, 3, 4, 10, 25)] == [1, 1, 3, 5, 109, 150049], f"số lời gọi ra {[count_calls(n) for n in (1, 2, 3, 4, 10, 25)]}"
    body = inspect.getsource(xep_pallet.count_calls).split('"""', 2)[-1]
    assert "ways_naive(" not in body, "count_calls phải tự tính bằng đệ quy, không chạy ways_naive"
    recursive_only(xep_pallet.count_calls)


def check_cached():
    src = inspect.getsource(xep_pallet.ways_cached)
    assert "lru_cache" in src, "ways_cached phải dùng functools.lru_cache"
    ways_cached.cache_clear()
    assert ways_cached(90) == 4660046610375530309, f"ways_cached(90) ra {ways_cached(90)}"
    assert run_limited(lambda: ways_cached(300) == ways_loop(300), 2, "lru_cache n = 300 quá 2 giây"), "ways_cached(300) khác ways_loop(300)"


def check_loop_and_choice():
    assert [ways_loop(n) for n in range(1, 9)] == [1, 2, 3, 5, 8, 13, 21, 34], "ways_loop sai"
    ways_cached.cache_clear()
    assert ways(400)[1] == "lru_cache" and ways(401)[1] == "vòng lặp", "chọn cách tính theo n sai"
    value, method = run_limited(lambda: ways(1000), 2, "n = 1000 quá 2 giây")
    assert method == "vòng lặp" and len(str(value)) == 209, "n = 1000 phải tính bằng vòng lặp, không RecursionError"


def check_layouts():
    assert layouts(1) == ["1"] and layouts(3) == ["1+1+1", "1+2", "2+1"], f"layouts(3) ra {layouts(3)}"
    assert len(layouts(8)) == 34 and len(set(layouts(8))) == 34, "layouts(8) phải có 34 cách khác nhau"


def check_benchmark():
    rows = run_limited(lambda: benchmark((10, 12)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [10, 12] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Dãy 10 m có 89 cách xếp (tính bằng lru_cache).", "Dãy 90 m có 4660046610375530309 cách xếp (tính bằng lru_cache).",
        "Dãy 1000 m có số có 209 chữ số cách xếp (tính bằng vòng lặp).", "Bản không nhớ gọi hàm 150049 lần với n = 25.",
        "5 cách: 1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 2+2", "Lỗi: Chiều dài phải là số nguyên từ 1 đến 8 mét",
        "Lỗi: Chiều dài phải là số nguyên từ 1 đến 30 mét", "Lỗi: Chiều dài phải là số nguyên từ 1 đến 1000 mét",
        "Lỗi: Chiều dài phải là số nguyên từ 1 đến 1000 mét", "n | không nhớ (ms) | lru_cache (ms)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã lưu phương án xếp kho. Tạm biệt!",
    ])


CHECKS = [
    ("số cách xếp, bản không nhớ (đệ quy)", check_naive),
    ("đếm số lời gọi (đệ quy)", check_calls),
    ("bản lru_cache", check_cached),
    ("bản vòng lặp và chọn cách tính theo n", check_loop_and_choice),
    ("liệt kê các cách xếp", check_layouts),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '10',
    '1',
    '90',
    '1',
    '1000',
    '2',
    '25',
    '3',
    '4',
    '3',
    '9',
    '2',
    '31',
    '1',
    '0',
    '1',
    'abc',
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
