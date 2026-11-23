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
import chuoi_ngay
from chuoi_ngay import make_days, make_big_days, report_slow, report_fast, add_day, benchmark, slow_fails


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_sample():
    assert report_fast(make_days()) == (4, 4, 19), f"báo cáo mẫu ra {report_fast(make_days())}"
    assert report_fast([]) == (0, 0, 0) and report_fast([5]) == (1, 1, 1)


def check_cap():
    days = list(range(100, 110))
    assert report_fast(days) == report_slow(days) == (10, 10, 1 + 2 + 3 + 4 + 5 + 6 + 7 + 7 + 7 + 7), "điểm tối đa 7 mỗi ngày"


def check_random():
    rng = random.Random(9)
    for _ in range(200):
        days, d = [], 0
        for _ in range(rng.randint(0, 60)):
            d += rng.choice([1, 1, 1, 2, 5])
            days.append(d)
        assert report_fast(days) == report_slow(days), f"khác bản cũ với {days}"


def check_rules():
    body = inspect.getsource(chuoi_ngay.report_fast).split('"""', 2)[-1]
    for banned in ("report_slow", "_streak_end", "setrecursionlimit"):
        assert banned not in body, f"report_fast không được dùng {banned}"
    days = make_days()
    report_fast(days)
    assert days == make_days(), "report_fast làm đổi lịch sử"


def check_long():
    days = make_big_days(100000)
    got = run_limited(lambda: report_fast(days), 1, "100.000 ngày quá 1 giây")
    assert got[0] == 9 and got[2] > 0, f"100.000 ngày ra {got}"
    assert slow_fails(3000) is True, "bản cũ với 3.000 ngày phải gặp RecursionError"


def check_add():
    days = make_days()
    add_day(days, " 2026-11-14 ")
    assert report_fast(days)[1] == 5
    raises("Ngày mua phải sau ngày mua gần nhất (2026-11-14)", lambda: add_day(days, "2026-11-14"))
    for bad in ["14/11/2026", "2026-13-01", "2026-11-31", ""]:
        raises("Ngày phải có dạng YYYY-MM-DD", lambda: add_day(days, bad))
    assert len(days) == 10


def check_benchmark():
    rows = run_limited(lambda: benchmark((50, 100), number=1), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [50, 100] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Chuỗi dài nhất: 4 ngày | Chuỗi hiện tại: 4 ngày | Điểm thưởng: 19", "2026-11-13, 2026-11-12, 2026-11-11",
        "Đã ghi 2026-11-14. Chuỗi hiện tại: 5 ngày.", "Lỗi: Ngày mua phải sau ngày mua gần nhất (2026-11-14)",
        "Lỗi: Ngày phải có dạng YYYY-MM-DD", "Đã ghi 2026-11-20. Chuỗi hiện tại: 1 ngày.",
        "Chuỗi dài nhất: 5 ngày | Chuỗi hiện tại: 1 ngày | Điểm thưởng: 25", "Lỗi: Số ngày phải là số nguyên dương",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Cảm ơn quý khách. Hẹn gặp lại!",
    ])


CHECKS = [
    ("báo cáo mẫu, lịch sử rỗng, một ngày", check_sample),
    ("điểm tối đa 7 mỗi ngày", check_cap),
    ("khớp bản cũ trên 200 lịch sử ngẫu nhiên", check_random),
    ("ràng buộc của report_fast", check_rules),
    ("100.000 ngày; bản cũ gặp RecursionError với 3.000 ngày", check_long),
    ("ghi ngày mua và dữ liệu sai", check_add),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '3',
    '1',
    '3',
    '2',
    '2026-11-14',
    '2',
    '2026-11-14',
    '2',
    '14/11/2026',
    '2',
    '2026-11-20',
    '3',
    '1',
    '0',
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
