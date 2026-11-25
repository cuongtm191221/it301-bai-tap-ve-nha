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
import soan_van_ban
from soan_van_ban import SlowEditor, FastEditor, make_editor, workload, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def outcome(task):
    try:
        return ("ok", task())
    except ValueError as error:
        return ("lỗi", str(error))


def check_sample():
    e = make_editor(FastEditor)
    assert e.lines() == ["CÔNG VĂN SỐ 125/VNPT", "Kính gửi: Phòng Kế hoạch", "V/v: Lịch bảo trì hệ thống tháng 12"]
    assert e.edit_line(" 2 ", " Kính gửi: Phòng Kỹ thuật ") == "sửa dòng 2" and e.delete_line("1") == "xóa dòng 1"
    assert e.lines() == ["Kính gửi: Phòng Kỹ thuật", "V/v: Lịch bảo trì hệ thống tháng 12"]
    assert e.undo() == "xóa dòng 1" and e.undo() == "sửa dòng 2" and e.lines()[1] == "Kính gửi: Phòng Kế hoạch"
    assert e.redo() == "sửa dòng 2" and e.add_line("Trân trọng.") == "thêm dòng 4"
    raises("Không có thao tác để làm lại", e.redo)
    raises("Dòng phải từ 1 đến 4", lambda: e.edit_line("9", "abc"))
    raises("Dòng phải từ 1 đến 4", lambda: e.edit_line("x", ""))
    raises("Nội dung dòng phải có từ 1 đến 80 ký tự", lambda: e.edit_line("1", "   "))
    for _ in range(5):
        e.undo()
    assert e.lines() == []
    raises("Không có thao tác để hoàn tác", e.undo)
    raises("Văn bản chưa có dòng nào", lambda: e.delete_line("1"))
    e.lines().append("x")
    assert e.lines() == [], "lines() phải trả bản sao"


def check_same():
    rng = random.Random(9)
    texts = ["A", "B", "  C  ", "", "x" * 81]
    for _ in range(200):
        slow, fast = SlowEditor(), FastEditor()
        for _ in range(rng.randint(0, 25)):
            op = rng.choice(["add", "add", "edit", "delete", "undo", "undo", "redo", "lines"])
            idx, text = str(rng.randint(0, 4)), rng.choice(texts)
            if op == "add":
                a, b = outcome(lambda: slow.add_line(text)), outcome(lambda: fast.add_line(text))
            elif op == "edit":
                a, b = outcome(lambda: slow.edit_line(idx, text)), outcome(lambda: fast.edit_line(idx, text))
            elif op == "delete":
                a, b = outcome(lambda: slow.delete_line(idx)), outcome(lambda: fast.delete_line(idx))
            elif op == "undo":
                a, b = outcome(slow.undo), outcome(fast.undo)
            elif op == "redo":
                a, b = outcome(slow.redo), outcome(fast.redo)
            else:
                a, b = slow.lines(), fast.lines()
            assert a == b, f"thao tác {op}: bản cũ ra {a}, bản mới ra {b}"
        assert slow.lines() == fast.lines()


def check_rules():
    source = inspect.getsource(FastEditor).split('"""', 2)[-1]
    assert "SlowEditor" not in source and "_snapshots" not in source, "FastEditor không được dùng bản cũ"
    for name in ("add_line", "edit_line", "delete_line", "undo", "redo"):
        body = inspect.getsource(getattr(FastEditor, name)).split('"""', 2)[-1]
        for banned in ("[:]", ".copy(", "list(", "self.lines()", "for ", "while"):
            assert banned not in body, f"FastEditor.{name} không được chép cả văn bản ({banned})"


def check_fast():
    got = run_limited(lambda: workload(FastEditor, 50000), 1, "bản mới với 50.000 dòng quá 1 giây")
    assert len(got) == 50000 and got[0] == "Sửa 0" and got[24999] == "Sửa 24999" and got[25000] == "Dòng 25000"


def check_benchmark():
    rows = run_limited(lambda: benchmark((50, 100)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [50, 100] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "1| CÔNG VĂN SỐ 125/VNPT", "3| V/v: Lịch bảo trì hệ thống tháng 12", "Đã sửa dòng 2.", "Đã xóa dòng 1.",
        "Đã hoàn tác: xóa dòng 1.", "Đã hoàn tác: sửa dòng 2.", "2| Kính gửi: Phòng Kế hoạch", "Đã làm lại: sửa dòng 2.",
        "Đã thêm dòng 4.", "Lỗi: Không có thao tác để làm lại", "Lỗi: Dòng phải từ 1 đến 4", "Lỗi: Dòng phải từ 1 đến 4",
        "Đã hoàn tác: thêm dòng 4.", "Đã hoàn tác: thêm dòng 1.", "Lỗi: Không có thao tác để hoàn tác", "(văn bản trống)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 8.", "Đã lưu văn bản. Tạm biệt!",
    ])


CHECKS = [
    ("FastEditor trên dữ liệu mẫu: mô tả, lỗi, hoàn tác hết", check_sample),
    ("khớp bản cũ trên 200 chuỗi thao tác ngẫu nhiên", check_same),
    ("không chép cả văn bản, không dùng bản cũ", check_rules),
    ("bản mới với 50.000 dòng trong 1 giây", check_fast),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '2',
    'Kính gửi: Phòng Kỹ thuật',
    '4',
    '1',
    '5',
    '5',
    '1',
    '6',
    '2',
    'Trân trọng.',
    '6',
    '3',
    '9',
    'abc',
    '4',
    'x',
    '5',
    '5',
    '5',
    '5',
    '5',
    '5',
    '1',
    'x',
    '8',
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
