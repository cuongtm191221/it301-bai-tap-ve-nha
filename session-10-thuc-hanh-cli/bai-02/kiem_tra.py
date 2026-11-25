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
from tong_dai import LinkedQueue, make_queue, incoming, answer


def raises(kind, message, task):
    try:
        task()
    except kind as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo {kind.__name__}("{message}")')


def check_queue():
    q = LinkedQueue()
    assert q.is_empty() and q.size() == 0
    raises(IndexError, "hàng đợi rỗng", q.dequeue)
    raises(IndexError, "hàng đợi rỗng", q.peek)
    for v in "ABC":
        q.enqueue(v)
    assert q.size() == 3 and q.peek() == "A" and q.peek() == "A" and q.size() == 3, "peek không lấy ra"
    assert q.dequeue() == "A" and q.dequeue() == "B" and q.dequeue() == "C"
    assert q.is_empty() and q.head is None and q.tail is None, "lấy phần tử cuối cùng phải đưa head, tail về None"
    q.enqueue("D")
    assert q.head is q.tail and q.peek() == "D" and q.size() == 1, "thêm lại sau khi rỗng"


def check_rules():
    for name in ("enqueue", "dequeue", "peek", "is_empty", "size"):
        body = inspect.getsource(getattr(LinkedQueue, name)).split('"""', 2)[-1]
        assert "while" not in body and "for " not in body and "[" not in body and "list(" not in body, f"{name} không được duyệt, không dùng list"


def check_business():
    q = make_queue()
    assert q.size() == 3 and q.peek() == ("CG001", "0901234567")
    assert incoming(q, " 0977555888 ") == ("CG004", "0977555888")
    raises(ValueError, "Số 0912000111 đang trong hàng chờ", lambda: incoming(q, "0912000111"))
    for bad in ["977555888", "1977555888", "09775558889", "09775a5888", ""]:
        raises(ValueError, "Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0", lambda: incoming(q, bad))
    assert [answer(q)[0] for _ in range(4)] == ["CG001", "CG002", "CG003", "CG004"]
    raises(ValueError, "Không có cuộc gọi đang chờ", lambda: answer(q))
    assert incoming(q, "0901234567") == ("CG005", "0901234567"), "số đã được nghe có thể gọi lại, mã không dùng lại"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "1. CG001 | 0901234567", "3. CG003 | 0388765432", "Đang chờ: 3 cuộc gọi", "Đang nghe CG001 (0901234567).",
        "Tiếp theo: CG002 (0912000111)", "Đã xếp CG004 (0977555888), vị trí 3.", "Lỗi: Số 0912000111 đang trong hàng chờ",
        "Lỗi: Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0", "Đang nghe CG004 (0977555888).", "Lỗi: Không có cuộc gọi đang chờ",
        "Không có cuộc gọi đang chờ.", "Đã xếp CG005 (0866123123), vị trí 1.", "1. CG005 | 0866123123", "Đang chờ: 1 cuộc gọi",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Tổng đài kết thúc ca trực. Tạm biệt!",
    ])


CHECKS = [
    ("LinkedQueue: enqueue, dequeue, peek, rỗng, thêm lại", check_queue),
    ("các phương thức không duyệt, không dùng list", check_rules),
    ("cuộc gọi đến, nhận cuộc gọi, dữ liệu sai", check_business),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '4',
    '2',
    '0977555888',
    '2',
    '0912000111',
    '2',
    '977555888',
    '3',
    '3',
    '3',
    '3',
    '4',
    '2',
    '0866123123',
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
