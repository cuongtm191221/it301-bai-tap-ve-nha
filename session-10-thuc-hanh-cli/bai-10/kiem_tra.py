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
import gia_cuoc
from gia_cuoc import peaks_slow, peaks_fast, make_counts, make_big_counts, record, parse_window, report, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_sample():
    counts = make_counts()
    got = peaks_fast(counts, 5)
    assert got == [40, 55, 120, 120, 120, 210, 210, 210, 210, 210, 180, 130, 130, 130, 130], f"k = 5 ra {got}"
    assert peaks_fast(counts, 1) == counts and peaks_fast(counts, 1440) == peaks_slow(counts, 1440)
    assert peaks_fast([], 3) == [] and counts == make_counts(), "không làm đổi counts"
    for bad in (0, 1441, -1, 2.5):
        raises("Số phút phải từ 1 đến 1440", lambda: peaks_fast(counts, bad))
    raises("Số phút phải từ 1 đến 1440", lambda: peaks_fast([], 0))


def check_same():
    rng = random.Random(10)
    for _ in range(300):
        counts = [rng.choice([0, 1, 5, 5, 9]) for _ in range(rng.randint(0, 20))]
        k = rng.randint(1, 8)
        assert peaks_fast(counts, k) == peaks_slow(counts, k), f"khác bản cũ với {counts}, k = {k}"


def check_rules():
    body = inspect.getsource(gia_cuoc.peaks_fast).split('"""', 2)[-1]
    for banned in ("peaks_slow", "max(", "sorted(", ":"):
        if banned == ":":
            assert "counts[" not in body or ":" not in body.split("counts[", 1)[1].split("]", 1)[0], "không cắt lát counts"
        else:
            assert banned not in body, f"peaks_fast không được dùng {banned}"
    counts = make_big_counts(200000)
    got = run_limited(lambda: peaks_fast(counts, 1000), 1, "200.000 phút, k = 1.000 quá 1 giây")
    assert len(got) == 200000 and got[-1] == 999 and got[0] == 0


def check_business():
    counts = make_counts()
    assert record(counts, " 250 ") == 16 and counts[-1] == 250
    for bad in ["-5", "10001", "1.5", "abc", ""]:
        raises("Số cuốc phải là số nguyên từ 0 đến 10000", lambda: record(counts, bad))
    assert parse_window(" 20 ") == 20
    for bad in ["0", "1441", "abc", "", "-3"]:
        raises("Số phút phải từ 1 đến 1440", lambda: parse_window(bad))
    rows = report(counts, 5)
    assert len(rows) == 10 and rows[0] == (7, 180, 210, 1.5) and rows[-1] == (16, 250, 250, 1.5) and rows[4] == (11, 130, 180, 1.2)
    assert report(counts, 1)[-2] == (15, 50, 50, 1.0) and report([90, 150], 3) == [(1, 90, 90, 1.0), (2, 150, 150, 1.2)]


def check_benchmark():
    rows = run_limited(lambda: benchmark((10, 20), n=500), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [10, 20] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Cửa sổ 5 phút", "Phút 6 | 210 cuốc | đỉnh 210 | x1.5", "Phút 11 | 130 cuốc | đỉnh 180 | x1.2", "Phút 15 | 50 cuốc | đỉnh 130 | x1.2",
        "Đã ghi phút 16.", "Lỗi: Số cuốc phải là số nguyên từ 0 đến 10000", "Đã đổi cửa sổ thành 1 phút.", "Phút 15 | 50 cuốc | đỉnh 50 | x1.0",
        "Phút 16 | 250 cuốc | đỉnh 250 | x1.5", "Lỗi: Số phút phải từ 1 đến 1440", "Lỗi: Số phút phải từ 1 đến 1440",
        "Đã đổi cửa sổ thành 20 phút.", "Phút 15 | 50 cuốc | đỉnh 210 | x1.5",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Be chúc bạn thượng lộ bình an!",
    ])


CHECKS = [
    ("peaks_fast trên dữ liệu mẫu, biên, lỗi, không đổi counts", check_sample),
    ("khớp bản cũ trên 300 bộ ngẫu nhiên", check_same),
    ("không dùng max, cắt lát, bản cũ; 200.000 phút trong 1 giây", check_rules),
    ("ghi số cuốc, đổi cửa sổ, báo cáo, dữ liệu sai", check_business),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    '250',
    '2',
    '-5',
    '3',
    '1',
    '1',
    '3',
    '0',
    '3',
    'abc',
    '3',
    '20',
    '1',
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
