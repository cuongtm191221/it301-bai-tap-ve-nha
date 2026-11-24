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
import lenh_cho
from lenh_cho import Node, OrderLine, make_line, submit, pending_total, process, bench_drain, memory_per_item


def raises(kind, message, task):
    try:
        task()
    except kind as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo {kind.__name__}("{message}")')


def check_line():
    line = OrderLine()
    raises(IndexError, "danh sách rỗng, không có phần tử để lấy", line.remove_first)
    for v in "ABC":
        line.add_last(v)
    assert line.size == 3 and line.remove_first() == "A" and line.remove_first() == "B" and line.size == 1
    assert line.remove_first() == "C" and line.head is None and line.tail is None and line.size == 0, "lấy node cuối cùng"
    line.add_last("D")
    assert line.head is line.tail and line.size == 1, "thêm lại sau khi rỗng"
    for name in ("add_last", "remove_first"):
        body = inspect.getsource(getattr(OrderLine, name)).split('"""', 2)[-1]
        assert "while" not in body and "for " not in body and "[" not in body, f"{name} không được duyệt, không dùng list"


def check_business():
    line = make_line()
    assert line.size == 4 and pending_total(line) == 138250000 and line.head.value[0] == "LC0001"
    assert submit(line, " 1500207778889 ", " 5000000 ") == ("LC0005", "1500207778889", 5000000)
    for bad in ["15002077", "150020777888a", "", "15002077788891"]:
        raises(ValueError, "Số tài khoản phải gồm 13 chữ số", lambda: submit(line, bad, "100000"))
    for bad in ["5000", "500000001", "1.5", "-20000", ""]:
        raises(ValueError, "Số tiền phải là số nguyên từ 10.000 đến 500.000.000", lambda: submit(line, "1500207778889", bad))
    assert [o[0] for o in process(line, "2")] == ["LC0001", "LC0002"] and line.size == 3
    assert [o[0] for o in process(line, "10")] == ["LC0003", "LC0004", "LC0005"] and line.size == 0
    raises(ValueError, "Không có lệnh chờ xử lý", lambda: process(line, "1"))
    for bad in ["0", "x", "-1"]:
        raises(ValueError, "Số lệnh phải là số nguyên dương", lambda: process(make_line(), bad))
    assert submit(line, "1500207778889", "10000")[0] == "LC0006", "mã lệnh không dùng lại"


def check_bench():
    rows = run_limited(lambda: bench_drain((300, 600)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [300, 600] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"bench_drain ra {rows}"
    rows = run_limited(lambda: bench_drain((20000, 80000)), 20, "đo quá 20 giây")
    assert rows[1][2] < rows[0][2] * 8, f"remove_first phải tăng gần tuyến tính, ra {rows}"


def check_memory():
    slot, node = memory_per_item()
    expect_slot = (sys.getsizeof([0] * 1000) - sys.getsizeof([])) / 1000
    sample = Node(0)
    assert abs(slot - expect_slot) < 1e-9 and node == sys.getsizeof(sample) + sys.getsizeof(sample.__dict__), f"ra {slot}, {node}"
    assert node > slot


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "LC0001 | 1500201234567 | 2.500.000đ", "LC0004 | 5400201112223 | 120.000.000đ", "Tổng: 4 lệnh, 138.250.000đ",
        "Đã nhập LC0005: 5.000.000đ. Còn 5 lệnh chờ.", "Lỗi: Số tài khoản phải gồm 13 chữ số",
        "Lỗi: Số tiền phải là số nguyên từ 10.000 đến 500.000.000", "Đã xử lý LC0001: 2.500.000đ", "Đã xử lý LC0002: 15.000.000đ",
        "Còn 3 lệnh chờ.", "Tổng: 3 lệnh, 125.750.000đ", "Đã xử lý LC0005: 5.000.000đ", "Còn 0 lệnh chờ.",
        "Lỗi: Không có lệnh chờ xử lý", "Lỗi: Số lệnh phải là số nguyên dương",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Agribank cảm ơn quý khách!",
    ])


CHECKS = [
    ("add_last, remove_first, size, rỗng; không duyệt", check_line),
    ("nhập lệnh, tổng tiền, xử lý k lệnh, dữ liệu sai", check_business),
    ("hàm đo; remove_first tăng gần tuyến tính", check_bench),
    ("bộ nhớ mỗi phần tử đo thật", check_memory),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    '1500207778889',
    '5000000',
    '2',
    '15002077',
    '100000',
    '2',
    '1500207778889',
    '5000',
    '3',
    '2',
    '1',
    '3',
    '10',
    '3',
    '1',
    '3',
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
