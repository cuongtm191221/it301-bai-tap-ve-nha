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
import tach_tu_khoa
from tach_tu_khoa import make_keywords, count_slow, count_fast, best_split, add_keyword, benchmark

KW = make_keywords()


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_count():
    got = [count_fast(t, KW) for t in ("tainghebluetooth", "sacduphongkhongday", "loabluetooth", "maytinhbang", "tai")]
    assert got == [4, 6, 2, 0, 1], f"số cách tách ra {got}"


def check_random():
    rng = random.Random(10)
    words = ["a", "ab", "b", "ba", "aba", "bb"]
    for _ in range(100):
        text = "".join(rng.choice("ab") for _ in range(rng.randint(1, 14)))
        assert count_fast(text, words) == count_slow(text, words), f"khác bản cũ với {text}"
    kws = KW[:]
    count_fast("tainghebluetooth", kws)
    assert kws == KW, "count_fast làm đổi từ điển"


def check_rules():
    body = inspect.getsource(tach_tu_khoa.count_fast).split('"""', 2)[-1]
    assert "count_slow" not in body and "setrecursionlimit" not in body, "count_fast không được gọi bản cũ hay đổi giới hạn đệ quy"


def check_fast():
    text = "sacduphong" * 30
    got = run_limited(lambda: count_fast(text, KW), 1, "chuỗi 300 ký tự quá 1 giây")
    assert got == 3 ** 30, f"chuỗi 300 ký tự ra {got}"


def check_best():
    assert best_split("tainghebluetooth", KW) == ["tainghe", "bluetooth"]
    assert best_split("sacduphongkhongday", KW) == ["sacduphong", "khongday"]
    assert best_split("maytinhbang", KW) is None
    assert best_split("abab", ["ab", "a", "b", "ba", "aba", "bab"]) == ["a", "bab"], "cùng số từ phải lấy cách nhỏ nhất theo thứ tự chữ cái"
    text = "sacduphong" * 30
    got = run_limited(lambda: best_split(text, KW), 1, "gợi ý cho chuỗi 300 ký tự quá 1 giây")
    assert got == ["sacduphong"] * 30


def check_add():
    kws = make_keywords()
    assert add_keyword(kws, " Bang ") == "bang" and kws[-1] == "bang"
    raises("Từ khóa tai đã có", lambda: add_keyword(kws, "Tai"))
    for bad in ["x", "tai-nghe", "a" * 21, "điện", ""]:
        raises("Từ khóa phải gồm 2 đến 20 chữ cái a-z", lambda: add_keyword(kws, bad))
    assert len(kws) == 19


def check_benchmark():
    rows = run_limited(lambda: benchmark((2, 3)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [2, 3] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Có 4 cách tách. Gợi ý: tainghe bluetooth", "Có 6 cách tách. Gợi ý: sacduphong khongday",
        "Không tách được: có đoạn chưa có trong từ điển.", "Đã thêm bang. Từ điển có 19 từ.", "Có 2 cách tách. Gợi ý: maytinh bang",
        "Lỗi: Từ khóa tai đã có", "Lỗi: Từ khóa phải gồm 2 đến 20 chữ cái a-z", "Lỗi: Chuỗi chỉ được gồm chữ cái a-z không dấu",
        "bang, blue, bluetooth", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã lưu từ điển. Tạm biệt!",
    ])


CHECKS = [
    ("số cách tách trên dữ liệu mẫu", check_count),
    ("khớp bản cũ trên 100 chuỗi ngẫu nhiên", check_random),
    ("ràng buộc của count_fast", check_rules),
    ("chuỗi 300 ký tự trong 1 giây", check_fast),
    ("gợi ý cách tách ít từ nhất", check_best),
    ("thêm từ khóa và dữ liệu sai", check_add),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    'tai nghe Bluetooth',
    '1',
    'sacduphongkhongday',
    '1',
    'maytinhbang',
    '2',
    'bang',
    '1',
    'maytinhbang',
    '2',
    'Tai',
    '2',
    'x',
    '1',
    'tai-nghe',
    '3',
    '0',
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
