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
import hang_cho
from hang_cho import Node, WaitingLine, take_ticket, make_line, call_next, position, leave


def raises(kind, message, task):
    try:
        task()
    except kind as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo {kind.__name__}("{message}")')


def build(*values):
    line = WaitingLine()
    for v in values:
        line.add_last(v)
    return line


def check_add_count_find():
    line = WaitingLine()
    assert line.count() == 0 and line.find("A") is None and line.to_text() == "None", "danh sách rỗng"
    line.add_last("A")
    assert line.head is line.tail and line.head.value == "A" and line.count() == 1, "một phần tử: head và tail cùng một node"
    line.add_last("B"); line.add_last("C")
    assert line.to_text() == "A -> B -> C -> None" and line.tail.value == "C" and line.tail.next is None
    assert line.count() == 3 and line.find("A") == 0 and line.find("C") == 2 and line.find("X") is None
    line.add_last("A")
    assert line.find("A") == 0, "find trả vị trí đầu tiên"


def check_remove_first():
    line = build("A", "B")
    assert line.remove_first() == "A" and line.to_text() == "B -> None"
    assert line.remove_first() == "B" and line.head is None and line.tail is None, "lấy node cuối cùng phải đưa cả head, tail về None"
    raises(IndexError, "danh sách rỗng, không có phần tử để lấy", line.remove_first)
    line.add_last("C")
    assert line.to_text() == "C -> None" and line.head is line.tail, "thêm lại sau khi rỗng"


def check_remove():
    line = build("A", "B", "C", "D")
    assert line.remove("X") is False and WaitingLine().remove("A") is False
    assert line.remove("A") is True and line.to_text() == "B -> C -> D -> None", "xóa head"
    assert line.remove("C") is True and line.to_text() == "B -> D -> None", "xóa giữa"
    assert line.remove("D") is True and line.tail.value == "B", "xóa tail thì tail lùi về node trước"
    line.add_last("E")
    assert line.to_text() == "B -> E -> None", f"thêm sau khi xóa tail ra {line.to_text()}"
    assert line.remove("B") and line.remove("E") and line.head is None and line.tail is None, "xóa node duy nhất"


def check_business():
    line = make_line()
    assert line.to_text() == "VP001 -> VP002 -> VP003 -> VP004 -> None" and line.issued == 4
    assert call_next(line) == "VP001" and take_ticket(line) == "VP005"
    assert position(line, " vp003 ") == 2 and position(line, "VP005") == 4
    for bad in ["VP3", "VX003", "VP00a", "", "VP0001"]:
        raises(ValueError, "Số thứ tự phải có dạng VP và 3 chữ số", lambda: position(line, bad))
    raises(ValueError, "Không có số VP001 trong hàng chờ", lambda: position(line, "VP001"))
    assert leave(line, "vp005") == "VP005" and take_ticket(line) == "VP006"
    assert line.to_text() == "VP002 -> VP003 -> VP004 -> VP006 -> None"
    raises(ValueError, "Không có số VP009 trong hàng chờ", lambda: leave(line, "VP009"))


def check_no_list():
    for name in ("add_last", "remove_first", "count", "find", "remove"):
        body = inspect.getsource(getattr(WaitingLine, name)).split('"""', 2)[-1]
        assert "[" not in body and "list(" not in body and ".append(" not in body, f"{name} không được dùng list Python"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "VP001 -> VP002 -> VP003 -> VP004 -> None", "Đang chờ: 4 khách", "Mời khách số VP001 đến quầy.",
        "Đã cấp số VP005. Phía trước có 3 khách.", "VP003 đang ở vị trí 2, còn 1 khách phía trước.",
        "Lỗi: Số thứ tự phải có dạng VP và 3 chữ số", "Khách số VP005 đã rời hàng chờ.", "Đã cấp số VP006. Phía trước có 3 khách.",
        "VP002 -> VP003 -> VP004 -> VP006 -> None", "Lỗi: Không có số VP001 trong hàng chờ", "Mời khách số VP006 đến quầy.",
        "Không còn khách trong hàng chờ.", "Đã cấp số VP007. Phía trước có 0 khách.", "VP007 -> None",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 6.", "Bưu cục đóng cửa. Hẹn gặp lại!",
    ])


CHECKS = [
    ("add_last, count, find trên danh sách rỗng, một node, nhiều node", check_add_count_find),
    ("remove_first, lấy hết rồi thêm lại", check_remove_first),
    ("remove trúng head, giữa, tail, node duy nhất", check_remove),
    ("cấp số, tra vị trí, khách bỏ về, dữ liệu sai", check_business),
    ("không dùng list Python trong các phương thức", check_no_list),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '2',
    '4',
    'vp003',
    '4',
    'VP3',
    '5',
    'VP005',
    '2',
    '1',
    '5',
    'VP001',
    '3',
    '3',
    '3',
    '3',
    '3',
    '2',
    '1',
    'x',
    '6',
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
