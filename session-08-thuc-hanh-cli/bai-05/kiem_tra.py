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
from thong_bao import NoticeFeed, make_feed, push, latest, notice_at, bench_front, bench_index


def raises(kind, message, task):
    try:
        task()
    except kind as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo {kind.__name__}("{message}")')


def check_feed():
    feed = NoticeFeed()
    raises(IndexError, "Chỉ số ngoài phạm vi", lambda: feed.get(0))
    for v in "ABC":
        feed.add_first(v)
    assert feed.size == 3 and [feed.get(i) for i in range(3)] == ["C", "B", "A"] and feed.head.next.next.next is None
    for bad in (3, -1):
        raises(IndexError, "Chỉ số ngoài phạm vi", lambda: feed.get(bad))


def check_business():
    feed = make_feed()
    assert latest(feed, "2") == ["TK1003 đã xác nhận", "TK1001 đã giao"] and len(latest(feed, "99")) == 5
    assert push(feed, " TK1003 đang giao ") == "TK1003 đang giao" and feed.size == 6
    assert notice_at(feed, "1") == "TK1003 đang giao" and notice_at(feed, "6") == "TK1001 đã xác nhận"
    for bad in ["0", "7", "x", "-1"]:
        raises(ValueError, "Thứ tự phải từ 1 đến 6", lambda: notice_at(feed, bad))
    for bad in ["0", "abc", ""]:
        raises(ValueError, "Số thông báo phải là số nguyên dương", lambda: latest(feed, bad))
    for bad in ["", "x" * 61]:
        raises(ValueError, "Thông báo phải có từ 1 đến 60 ký tự", lambda: push(feed, bad))
    assert latest(NoticeFeed(), "3") == []


def check_linked_only():
    for name in ("add_first", "get"):
        body = inspect.getsource(getattr(NoticeFeed, name)).split('"""', 2)[-1]
        assert "[" not in body and "list(" not in body and ".append(" not in body, f"{name} không được dùng list Python"
    body = inspect.getsource(NoticeFeed.add_first).split('"""', 2)[-1]
    assert "while" not in body and "for " not in body, "add_first không được duyệt danh sách"


def check_bench():
    rows = run_limited(lambda: bench_front((200, 400)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [200, 400] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"bench_front ra {rows}"
    rows = run_limited(lambda: bench_index((200, 400), probes=20), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [200, 400] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"bench_index ra {rows}"


def check_shape():
    rows = run_limited(lambda: bench_index((2000, 8000), probes=200), 10, "đo quá 10 giây")
    assert rows[1][2] > rows[0][2] * 2, f"đọc theo vị trí trên danh sách liên kết phải tăng theo n, ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "1. TK1003 đã xác nhận", "3. TK1002 đã xác nhận", "Đã thêm. Có 6 thông báo.", "1. TK1003 đang giao", "6. TK1001 đã xác nhận",
        "TK1003 đã xác nhận", "Lỗi: Thứ tự phải từ 1 đến 6", "Lỗi: Thứ tự phải từ 1 đến 6", "Lỗi: Số thông báo phải là số nguyên dương",
        "Lỗi: Thông báo phải có từ 1 đến 60 ký tự", "Lựa chọn không hợp lệ.",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Cảm ơn bạn đã mua sắm trên Tiki!",
    ])


CHECKS = [
    ("add_first, get, chỉ số sai", check_feed),
    ("thêm, xem k thông báo, xem theo thứ tự, dữ liệu sai", check_business),
    ("chỉ dùng danh sách liên kết; add_first không duyệt", check_linked_only),
    ("hai hàm đo", check_bench),
    ("đọc theo vị trí trên danh sách liên kết tăng theo n", check_shape),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '2',
    'TK1003 đang giao',
    '1',
    '10',
    '3',
    '2',
    '3',
    '7',
    '3',
    '0',
    '1',
    'abc',
    '2',
    '   ',
    '4',
    'x',
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
