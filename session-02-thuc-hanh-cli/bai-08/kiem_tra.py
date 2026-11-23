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
from voucher import make_vouchers, make_big_vouchers, issue, total_value, find_duplicates_v1, find_duplicates_v2, benchmark

EXPECTED = [("LZ3M9P0B", 2), ("LZ8K2Q1A", 3)]


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_issue():
    vs = make_vouchers()
    assert total_value(vs) == 300 and total_value([]) == 0, "tổng giá trị sai"
    assert issue(vs, " lz1x5w6d ", "10") == ["LZ1X5W6D", 10] and len(vs) == 8, "phát mã trùng vẫn phải được"
    for bad in ["LZ12", "AB12CD34", "LZ1X5W6D9", "LZ1X-W6D", ""]:
        raises("Mã voucher phải có 8 ký tự chữ hoặc số, bắt đầu bằng LZ", lambda: issue(vs, bad, "10"))
    for bad in ["30", "0", "-10", "50.0", "x"]:
        raises("Giá trị phải là 10, 20, 50 hoặc 100 (nghìn đồng)", lambda: issue(vs, "LZ9A9A9A", bad))
    assert len(vs) == 8, "dữ liệu sai không được phát"


def check_v1():
    vs = make_vouchers()
    assert find_duplicates_v1(vs) == EXPECTED, f"giải pháp 1 ra {find_duplicates_v1(vs)}"
    assert vs == make_vouchers(), "giải pháp 1 làm đổi lô"


def check_v2():
    vs = make_vouchers()
    assert find_duplicates_v2(vs) == EXPECTED, f"giải pháp 2 ra {find_duplicates_v2(vs)}"
    assert vs == make_vouchers(), "giải pháp 2 làm đổi lô"


def check_edges():
    for f in (find_duplicates_v1, find_duplicates_v2):
        assert f([]) == [] and f([["LZ000001", 10]]) == [], f"{f.__name__}: lô rỗng, một voucher"
        assert f([["LZ000001", 10]] * 4) == [("LZ000001", 4)], f"{f.__name__}: một mã phát 4 lần"


def check_same_random():
    rng = random.Random(8)
    for _ in range(200):
        vs = [[f"LZ{rng.randint(0, 15):06d}", 10] for _ in range(rng.randint(0, 30))]
        assert find_duplicates_v1(vs) == find_duplicates_v2(vs), f"hai giải pháp khác kết quả với {vs}"


def check_v2_fast():
    vs = make_big_vouchers(200000)
    got = run_limited(lambda: find_duplicates_v2(vs), 2, "giải pháp 2 với 200.000 voucher quá 2 giây")
    assert len(got) == 2000 and all(c == 2 for _, c in got), f"200.000 voucher ra {len(got)} mã trùng"


def check_benchmark():
    rows = run_limited(lambda: benchmark((200, 400)), 10, "đo hiệu năng quá 10 giây")
    assert [r[0] for r in rows] == [200, 400] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Mã trùng: LZ3M9P0B (2 lần), LZ8K2Q1A (3 lần)", "7. LZ8K2Q1A | 50k", "Tổng: 7 voucher, giá trị 300k",
        "Đã phát LZ1X5W6D trị giá 10k. Lô có 8 voucher.", "Mã trùng: LZ1X5W6D (2 lần), LZ3M9P0B (2 lần), LZ8K2Q1A (3 lần)",
        "Lỗi: Mã voucher phải có 8 ký tự chữ hoặc số, bắt đầu bằng LZ", "Lỗi: Giá trị phải là 10, 20, 50 hoặc 100 (nghìn đồng)",
        "LZ1X5W6D | 10k", "LZ8K2Q1A | 50k", "Lỗi: Số voucher phải là số nguyên dương", "Lựa chọn không hợp lệ.",
        "n | giải pháp 1 (ms) | giải pháp 2 (ms)", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã khóa lô voucher. Tạm biệt!",
    ])


CHECKS = [
    ("phát voucher, tổng giá trị, dữ liệu sai", check_issue),
    ("giải pháp 1 trên dữ liệu mẫu", check_v1),
    ("giải pháp 2 trên dữ liệu mẫu", check_v2),
    ("lô rỗng, một voucher, một mã phát nhiều lần", check_edges),
    ("hai giải pháp cùng kết quả trên 200 lô ngẫu nhiên", check_same_random),
    ("giải pháp 2 với 200.000 voucher", check_v2_fast),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '3',
    '1',
    '1',
    '1',
    '2',
    'lz1x5w6d',
    '10',
    '3',
    '2',
    '2',
    'LZ12',
    '50',
    '2',
    'LZ9A9A9A',
    '30',
    '1',
    '2',
    '2',
    '1',
    '2',
    'x',
    '3',
    '3',
    '4',
    'abc',
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
