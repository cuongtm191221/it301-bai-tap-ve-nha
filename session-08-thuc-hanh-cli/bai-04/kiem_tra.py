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
from lich_su_xem import WatchHistory, make_history, watch, undo_last, import_old


def raises(kind, message, task):
    try:
        task()
    except kind as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo {kind.__name__}("{message}")')


def links_ok(h):
    """Đi xuôi và đi ngược phải khớp nhau, đúng size, head.prev và tail.next là None."""
    forward, node, last = [], h.head, None
    while node is not None:
        assert node.prev is last, f"prev của {node.value} sai"
        forward.append(node.value)
        last, node = node, node.next
    assert last is h.tail, "tail không phải node cuối khi đi xuôi"
    assert len(forward) == h.size, f"size là {h.size} nhưng có {len(forward)} node"
    return forward


def check_add():
    h = WatchHistory()
    assert h.to_text_backward() == "None" and h.size == 0
    h.add_first("B")
    assert h.head is h.tail and h.size == 1
    h.add_last("C"); h.add_first("A"); h.add_last("D")
    assert links_ok(h) == ["A", "B", "C", "D"] and h.to_text_backward() == "D -> C -> B -> A -> None"


def check_remove():
    h = WatchHistory()
    for v in "ABC":
        h.add_last(v)
    assert h.remove_first() == "A" and h.head.prev is None and links_ok(h) == ["B", "C"]
    assert h.remove_last() == "C" and h.tail.next is None and links_ok(h) == ["B"]
    assert h.remove_last() == "B" and h.head is None and h.tail is None and h.size == 0, "xóa node duy nhất"
    raises(IndexError, "danh sách rỗng, không có phần tử để xóa", h.remove_first)
    raises(IndexError, "danh sách rỗng, không có phần tử để xóa", h.remove_last)
    h.add_last("E"); h.add_first("D")
    assert links_ok(h) == ["D", "E"] and h.to_text_backward() == "E -> D -> None", "thêm lại sau khi rỗng"


def check_business():
    h = make_history()
    assert watch(h, " Ký sự Tây Bắc ") == ("Ký sự Tây Bắc", None) and watch(h, "B4") == ("B4", None)
    assert watch(h, "V") == ("V", "Hành trình biển xanh") and h.size == 6 and h.head.prev is None
    raises(ValueError, "Lịch sử đã đủ 6 mục, không nhập thêm mục cũ", lambda: import_old(h, "Phim cũ"))
    raises(ValueError, "Tên phim phải có từ 1 đến 40 ký tự", lambda: import_old(h, "   "))
    assert undo_last(h) == "V" and undo_last(h) == "B4" and import_old(h, "Thời sự sáng") == "Thời sự sáng"
    assert links_ok(h) == ["Thời sự sáng", "Bếp nhà mình tập 3", "Trận cầu đỉnh cao", "Hoạt hình Thỏ con", "Ký sự Tây Bắc"]
    for bad in ["", "x" * 41]:
        raises(ValueError, "Tên phim phải có từ 1 đến 40 ký tự", lambda: watch(h, bad))
    raises(ValueError, "Lịch sử xem đang trống", lambda: undo_last(WatchHistory()))


def check_size_constant():
    body = inspect.getsource(WatchHistory.add_last).split('"""', 2)[-1] + inspect.getsource(WatchHistory.remove_first).split('"""', 2)[-1]
    assert "while" not in body and "for " not in body, "thêm, xóa ở hai đầu không được duyệt danh sách"
    for name in ("to_text_backward", "add_first", "add_last", "remove_first", "remove_last"):
        body = inspect.getsource(getattr(WatchHistory, name)).split('"""', 2)[-1]
        assert "list(" not in body and ".append(" not in body.replace("parts.append(", ""), f"{name} không được dùng list Python để lưu"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Hoạt hình Thỏ con -> Trận cầu đỉnh cao -> Bếp nhà mình tập 3 -> Hành trình biển xanh -> None", "4 mục",
        "Hành trình biển xanh -> Bếp nhà mình tập 3 -> Trận cầu đỉnh cao -> Hoạt hình Thỏ con -> None",
        "Đã ghi Ký sự Tây Bắc vào lịch sử.", "Đã ghi Vui khỏe mỗi ngày vào lịch sử.", "Đã bỏ mục cũ nhất: Hành trình biển xanh.",
        "Lỗi: Lịch sử đã đủ 6 mục, không nhập thêm mục cũ", "Đã xóa Vui khỏe mỗi ngày khỏi lịch sử.",
        "Đã xóa Bếp nhà mình tập 4 khỏi lịch sử.", "Đã nhập Thời sự sáng vào đầu lịch sử.",
        "Ký sự Tây Bắc -> Hoạt hình Thỏ con -> Trận cầu đỉnh cao -> Bếp nhà mình tập 3 -> Thời sự sáng -> None", "5 mục",
        "Lựa chọn không hợp lệ.", "Lỗi: Tên phim phải có từ 1 đến 40 ký tự",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Hẹn gặp lại trên Galaxy Play!",
    ])


CHECKS = [
    ("add_first, add_last, to_text_backward, liên kết prev và next", check_add),
    ("remove_first, remove_last, node duy nhất, rỗng", check_remove),
    ("xem phim, giới hạn 6 mục, xóa mục vừa xem, nhập mục cũ", check_business),
    ("thêm, xóa ở hai đầu không duyệt danh sách, không dùng list", check_size_constant),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '1',
    '1',
    '2',
    '2',
    'Ký sự Tây Bắc',
    '2',
    'Bếp nhà mình tập 4',
    '2',
    'Vui khỏe mỗi ngày',
    '4',
    'Phim cũ',
    '3',
    '3',
    '4',
    'Thời sự sáng',
    '1',
    '1',
    '1',
    'x',
    '2',
    '   ',
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
