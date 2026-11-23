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
import bao_cao_ca
from bao_cao_ca import make_orders, make_big_orders, report_slow, report_fast, add_order, find_order, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_sample():
    got = report_fast(make_orders(), 3)
    assert got == (11, 4, "Trà đào cam sả", 4, ["TCH0006", "TCH0005", "TCH0004"]), f"báo cáo mẫu ra {got}"


def check_edges():
    orders = make_orders()
    for top in (0, 1, 6, 10):
        assert report_fast(orders, top) == report_slow(orders, top), f"top = {top}: khác bản cũ"
    assert report_fast([], 3) == (0, 0, None, 0, []), "sổ rỗng"
    tie = [["A", "Bạc xỉu", 2], ["B", "Cold brew", 2]]
    assert report_fast(tie, 3)[2:4] == ("Bạc xỉu", 2), "bằng số ly phải lấy món xuất hiện trước"
    assert orders == make_orders(), "report_fast làm đổi sổ"


def check_random():
    rng = random.Random(9)
    for _ in range(200):
        orders = [[f"T{k}", f"M{rng.randint(0, 5)}", rng.randint(1, 4)] for k in range(rng.randint(0, 40))]
        top = rng.randint(0, 45)
        assert report_fast(orders, top) == report_slow(orders, top), f"khác bản cũ với {orders}, top = {top}"


def check_rules():
    src = inspect.getsource(bao_cao_ca.report_fast)
    body = src.split('"""', 2)[-1]
    for banned in ("report_slow", "insert(0", "pop(0", "dict(", "set(", "{"):
        assert banned not in body, f"report_fast không được dùng {banned}"


def check_fast():
    orders = make_big_orders(200000)
    got = run_limited(lambda: report_fast(orders, 3), 2, "report_fast với 200.000 đơn quá 2 giây")
    assert got[0] == 500000 and got[1] == 30 and got[4] == ["TCH200000", "TCH199999", "TCH199998"], f"200.000 đơn ra {got[:2]}, {got[4]}"


def check_app():
    orders = make_orders()
    assert add_order(orders, " 3 ", "2") == ["TCH0007", "Bạc xỉu", 2], "ghi đơn mới sai"
    raises("Món phải là số từ 1 đến 5", lambda: add_order(orders, "6", "1"))
    raises("Món phải là số từ 1 đến 5", lambda: add_order(orders, "0", "1"))
    raises("Số ly phải là số nguyên từ 1 đến 20", lambda: add_order(orders, "1", "21"))
    raises("Số ly phải là số nguyên từ 1 đến 20", lambda: add_order(orders, "1", "x"))
    assert len(orders) == 7 and find_order(orders, " tch0003")[1] == "Cà phê sữa đá" and find_order(orders, "TCH9") is None


def check_benchmark():
    rows = run_limited(lambda: benchmark((300, 600)), 10, "đo hiệu năng quá 10 giây")
    assert [r[0] for r in rows] == [300, 600] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Tổng: 11 ly, 4 món.", "Bán chạy nhất: Trà đào cam sả (4 ly).", "3 đơn gần nhất: TCH0006, TCH0005, TCH0004",
        "Đã ghi TCH0007: 2 ly Trà đào cam sả.", "Lỗi: Món phải là số từ 1 đến 5", "Đã ghi TCH0008: 1 ly Cà phê sữa đá.",
        "Lỗi: Món phải là số từ 1 đến 5", "Bán chạy nhất: Trà đào cam sả (6 ly).", "3 đơn gần nhất: TCH0008, TCH0007, TCH0006",
        "TCH0003: 3 ly Cà phê sữa đá.", "Không tìm thấy đơn.", "Lỗi: Số ly phải là số nguyên từ 1 đến 20",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã chốt ca. Hẹn gặp lại!",
    ])


CHECKS = [
    ("báo cáo mẫu", check_sample),
    ("top ở biên, sổ rỗng, bằng số ly, không đổi sổ", check_edges),
    ("khớp bản cũ trên 200 sổ ngẫu nhiên", check_random),
    ("ràng buộc của report_fast", check_rules),
    ("report_fast với 200.000 đơn", check_fast),
    ("ghi đơn, tra cứu, dữ liệu sai", check_app),
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
    '6',
    '1',
    '1',
    '1',
    '1',
    '1',
    '0',
    '3',
    '2',
    '3',
    'tch0003',
    '3',
    'TCH9999',
    '1',
    '1',
    '21',
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
