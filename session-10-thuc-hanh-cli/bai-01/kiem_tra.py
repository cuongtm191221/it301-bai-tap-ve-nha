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
from soan_tin import ArrayStack, Draft, type_word, delete_word, undo, redo


def raises(kind, message, task):
    try:
        task()
    except kind as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo {kind.__name__}("{message}")')


def check_stack():
    s = ArrayStack()
    assert s.is_empty() and s.size() == 0
    raises(IndexError, "ngăn xếp rỗng", s.pop)
    raises(IndexError, "ngăn xếp rỗng", s.peek)
    for v in "ABC":
        s.push(v)
    assert s.size() == 3 and s.peek() == "C" and s.size() == 3, "peek không lấy phần tử ra"
    assert s.pop() == "C" and s.pop() == "B" and s.peek() == "A" and not s.is_empty()
    assert s.pop() == "A" and s.is_empty()
    for name in ("push", "pop"):
        body = inspect.getsource(getattr(ArrayStack, name)).split('"""', 2)[-1]
        assert "insert(" not in body and "pop(0)" not in body, f"{name}: đỉnh phải ở cuối list"


def check_type_delete():
    d = Draft()
    assert type_word(d, " Chào ") == "Chào" and type_word(d, "anh") == "anh" and d.text() == "Chào anh"
    for bad in ["", "   ", "hai từ", "x" * 21]:
        raises(ValueError, "Mỗi lần gõ một từ, 1 đến 20 ký tự", lambda: type_word(d, bad))
    assert delete_word(d) == "anh" and d.text() == "Chào" and d.undo_stack.size() == 3
    delete_word(d)
    raises(ValueError, "Tin nhắn đang trống", lambda: delete_word(d))
    assert d.text() == "(trống)"


def check_undo_redo():
    d = Draft()
    for w in ["Chào", "anh", "Hùng"]:
        type_word(d, w)
    delete_word(d)
    assert undo(d) == ("xóa", "Hùng") and d.text() == "Chào anh Hùng", "hoàn tác xóa phải thêm lại từ"
    assert undo(d) == ("gõ", "Hùng") and d.text() == "Chào anh"
    assert redo(d) == ("gõ", "Hùng") and d.text() == "Chào anh Hùng"
    assert redo(d) == ("xóa", "Hùng") and d.text() == "Chào anh"
    raises(ValueError, "Không có thao tác để làm lại", lambda: redo(d))
    undo(d); undo(d)
    type_word(d, "chị")
    raises(ValueError, "Không có thao tác để làm lại", lambda: redo(d))
    assert d.text() == "Chào anh chị"
    for _ in range(3):
        undo(d)
    assert d.text() == "(trống)"
    raises(ValueError, "Không có thao tác để hoàn tác", lambda: undo(d))


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Tin nhắn: Chào anh Hùng", "Đã xóa \"Hùng\". Tin nhắn: Chào anh", "Tin nhắn: Chào anh Lan",
        "Đã hoàn tác (gõ \"Lan\"). Tin nhắn: Chào anh", "Đã hoàn tác (xóa \"Hùng\"). Tin nhắn: Chào anh Hùng",
        "Đã làm lại (xóa \"Hùng\"). Tin nhắn: Chào anh", "Tin nhắn: Chào anh ơi", "Lỗi: Không có thao tác để làm lại",
        "Lỗi: Mỗi lần gõ một từ, 1 đến 20 ký tự", "Đã hoàn tác (gõ \"ơi\"). Tin nhắn: Chào anh",
        "Đã hoàn tác (gõ \"Chào\"). Tin nhắn: (trống)", "Lỗi: Không có thao tác để hoàn tác",
        "Đã làm lại (gõ \"Chào\"). Tin nhắn: Chào", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 6.", "Đã lưu bản nháp. Tạm biệt!",
    ])


CHECKS = [
    ("ArrayStack: push, pop, peek, is_empty, size, rỗng", check_stack),
    ("gõ từ, xóa từ, dữ liệu sai", check_type_delete),
    ("hoàn tác, làm lại, thao tác mới xóa làm lại", check_undo_redo),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '2',
    'Lan',
    '4',
    '4',
    '5',
    '2',
    'ơi',
    '5',
    '2',
    'hai từ',
    '4',
    '4',
    '4',
    '4',
    '4',
    '4',
    '5',
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
