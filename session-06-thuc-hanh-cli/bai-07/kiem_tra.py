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
import lac_xu
from lac_xu import make_turns, make_big_turns, add_turn, unique_v1, unique_v2, count_turns, benchmark

EXPECTED = [100245, 532001, 777777, 3, 888120]


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_v1():
    turns = make_turns()
    assert unique_v1(turns) == EXPECTED and turns == make_turns(), f"giải pháp 1 ra {unique_v1(turns)}"


def check_v2():
    turns = make_turns()
    assert unique_v2(turns) == EXPECTED and turns == make_turns(), f"giải pháp 2 ra {unique_v2(turns)}"
    assert unique_v2([0, 999999, 0]) == [0, 999999], "mã nhỏ nhất và lớn nhất"
    for f in (lac_xu.unique_v1, lac_xu.unique_v2):
        body = inspect.getsource(f).split('"""', 2)[-1]
        assert "set(" not in body and "dict(" not in body and "{" not in body, f"{f.__name__} không được dùng dict, set"


def check_same():
    rng = random.Random(7)
    for _ in range(200):
        turns = [rng.randint(0, 20) for _ in range(rng.randint(0, 40))]
        assert unique_v1(turns) == unique_v2(turns), f"hai giải pháp khác kết quả với {turns}"
    assert unique_v1([]) == unique_v2([]) == []


def check_fast():
    turns = make_big_turns(300000)
    got = run_limited(lambda: unique_v2(turns), 1, "giải pháp 2 với 300.000 lượt quá 1 giây")
    assert len(got) == 150001, f"300.000 lượt ra {len(got)} người chơi"


def check_add_count():
    turns = make_turns()
    assert add_turn(turns, " 000999 ") == 999 and turns[-1] == 999
    for bad in ["1000000", "12a", "-5", ""]:
        raises("Mã người dùng phải là số từ 0 đến 999999", lambda: add_turn(turns, bad))
    assert count_turns(turns, 100245) == 3 and count_turns(turns, 5) == 0


def check_benchmark():
    rows = run_limited(lambda: benchmark((200, 400)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [200, 400] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "5 người chơi: 100245, 532001, 777777, 000003, 888120", "5 người chơi: 100245, 532001, 777777, 000003, 888120",
        "Đã ghi lượt của 000999. Tổng 9 lượt.", "Lỗi: Mã người dùng phải là số từ 0 đến 999999",
        "Lỗi: Mã người dùng phải là số từ 0 đến 999999", "100245 đã lắc 3 lượt.", "Lỗi: Mã người dùng phải là số từ 0 đến 999999",
        "Lựa chọn không hợp lệ.", "n | giải pháp 1 (ms) | giải pháp 2 (ms)", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.",
        "Đã khóa minigame. Tạm biệt!",
    ])


CHECKS = [
    ("giải pháp 1 trên dữ liệu mẫu", check_v1),
    ("giải pháp 2 trên dữ liệu mẫu, không dict, set", check_v2),
    ("hai giải pháp cùng kết quả trên 200 bộ ngẫu nhiên", check_same),
    ("giải pháp 2 với 300.000 lượt", check_fast),
    ("ghi lượt, đếm lượt, dữ liệu sai", check_add_count),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '2',
    '1',
    '2',
    '2',
    '1',
    '000999',
    '1',
    '1000000',
    '1',
    '12a',
    '3',
    '100245',
    '3',
    'x',
    '2',
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
