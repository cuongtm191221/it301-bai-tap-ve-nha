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


import sys
import inspect
from collections import deque
import thanh_toan
from thanh_toan import PaymentQueue, make_queue, submit, process, bench_drain, memory_report


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_submit():
    q = make_queue()
    assert len(q.requests) == 4 and q.requests[0] == ("YC00001", "0901112223", 150000)
    assert submit(q, " 0977123456 ", " 300000 ") == ("YC00005", "0977123456", 300000) and q.requests[-1][0] == "YC00005"
    for bad in ["977123456", "1977123456", "09771234567", ""]:
        raises("Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0", lambda: submit(q, bad, "1000"))
    for bad in ["999", "50000001", "1.5", "-1000", ""]:
        raises("Số tiền phải là số nguyên từ 1.000 đến 50.000.000", lambda: submit(q, "0977123456", bad))
    assert len(q.requests) == 5


def check_process():
    q = make_queue()
    assert [r[0] for r in process(q, "3")] == ["YC00001", "YC00002", "YC00003"] and len(q.requests) == 1
    assert [r[0] for r in process(q, "10")] == ["YC00004"]
    raises("Không có yêu cầu đang chờ", lambda: process(q, "1"))
    for bad in ["0", "abc", "-2", ""]:
        raises("Số yêu cầu phải là số nguyên dương", lambda: process(make_queue(), bad))
    body = inspect.getsource(thanh_toan.process).split('"""', 2)[-1]
    assert "pop(0)" not in body and "popleft(" in body, "process phải lấy bằng popleft"
    assert submit(q, "0911111111", "1000")[0] == "YC00005", "mã không dùng lại"


def check_bench():
    rows = run_limited(lambda: bench_drain((500, 1000)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [500, 1000] and all(len(r) == 4 and min(r[1:]) > 0 for r in rows), f"bench_drain ra {rows}"
    rows = run_limited(lambda: bench_drain((40000, 160000)), 30, "đo quá 30 giây")
    assert rows[1][1] > rows[0][1] * 6, f"list.pop(0) phải tăng nhanh hơn tuyến tính, ra {rows}"
    assert rows[1][3] < rows[0][3] * 8, f"deque.popleft phải tăng gần tuyến tính, ra {rows}"


def check_memory():
    got = memory_report(1000)
    assert got == (sys.getsizeof(list(range(1000))), sys.getsizeof(deque(range(1000)))), f"memory_report(1000) ra {got}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "YC00001 | 0901112223 | 150.000đ", "YC00004 | 0909090909 | 800.000đ", "Đang chờ: 4 yêu cầu", "Đã nhận YC00005: 300.000đ.",
        "Lỗi: Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0", "Lỗi: Số tiền phải là số nguyên từ 1.000 đến 50.000.000",
        "Đã xử lý YC00001: 150.000đ", "Đã xử lý YC00002: 2.500.000đ", "Lỗi: Số yêu cầu phải là số nguyên dương",
        "Đã xử lý YC00005: 300.000đ", "Lỗi: Không có yêu cầu đang chờ",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "MoMo cảm ơn bạn!",
    ])


CHECKS = [
    ("gửi yêu cầu, dữ liệu sai", check_submit),
    ("xử lý k yêu cầu bằng popleft, hàng trống", check_process),
    ("hàm đo; pop(0) tăng nhanh, deque tăng gần tuyến tính", check_bench),
    ("bộ nhớ list và deque đo thật", check_memory),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    '0977123456',
    '300000',
    '2',
    '977123456',
    '1000',
    '2',
    '0977123456',
    '999',
    '3',
    '2',
    '3',
    'abc',
    '3',
    '10',
    '3',
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
