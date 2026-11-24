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
import but_toan
from but_toan import SlowJournal, FastJournal, make_journal, record, undo, workload, benchmark


def raises(kind, message, task):
    try:
        task()
    except kind as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo {kind.__name__}("{message}")')


def outcome(task):
    try:
        return ("ok", task())
    except (IndexError, ValueError) as error:
        return (type(error).__name__, str(error))


def check_sample():
    j = make_journal(FastJournal)
    assert j.balance() == 12350000 and j.size() == 4 and j.issued == 4
    assert [e[0] for e in j.recent(3)] == ["BT0004", "BT0003", "BT0002"] and len(j.recent(99)) == 4
    assert undo(j) == ("BT0004", "Thu tiền khách hàng B", 7200000) and j.balance() == 5150000 and j.size() == 3
    assert record(j, " Chi tiền điện ", "-1250000") == ("BT0005", "Chi tiền điện", -1250000) and j.balance() == 3900000
    for _ in range(4):
        undo(j)
    assert j.head is None and j.tail is None and j.size() == 0 and j.balance() == 0 and j.recent(3) == []
    raises(ValueError, "Không còn bút toán để hoàn tác", lambda: undo(j))
    raises(IndexError, "danh sách rỗng, không có phần tử để xóa", j.remove_last)
    assert record(j, "Thu", "5")[0] == "BT0006" and j.head is j.tail


def check_same():
    rng = random.Random(10)
    for _ in range(200):
        slow, fast = SlowJournal(), FastJournal()
        for _ in range(rng.randint(0, 25)):
            op = rng.choice(["add", "add", "undo", "recent", "balance"])
            if op == "add":
                desc, amount = rng.choice(["Thu", "Chi", "  ", "x" * 51]), rng.choice(["100", "-50", "0", "a", "-"])
                a, b = outcome(lambda: record(slow, desc, amount)), outcome(lambda: record(fast, desc, amount))
            elif op == "undo":
                a, b = outcome(lambda: undo(slow)), outcome(lambda: undo(fast))
            elif op == "recent":
                k = rng.randint(1, 5)
                a, b = slow.recent(k), fast.recent(k)
            else:
                a, b = (slow.balance(), slow.size()), (fast.balance(), fast.size())
            assert a == b, f"thao tác {op}: bản cũ ra {a}, bản mới ra {b}"
        assert slow.recent(100) == fast.recent(100)


def check_rules():
    for name in ("add_last", "remove_last", "size", "balance"):
        body = inspect.getsource(getattr(FastJournal, name)).split('"""', 2)[-1]
        assert "while" not in body and "for " not in body and "list(" not in body and ".append(" not in body, f"FastJournal.{name} không được duyệt, không dùng list"
    source = inspect.getsource(FastJournal).split('"""', 2)[-1]
    assert "SlowJournal" not in source and "DNode(" in source, "FastJournal phải dùng DNode, không dùng bản cũ"
    j = FastJournal()
    for k in range(5):
        j.add_last(("BT", "x", k))
    node, last = j.head, None
    while node is not None:
        assert node.prev is last, "liên kết prev sai"
        last, node = node, node.next
    assert last is j.tail


def check_fast():
    got = run_limited(lambda: workload(FastJournal, 100000), 1, "bản mới với 100.000 bút toán quá 1 giây")
    assert got == 1250025000, f"số dư cuối ra {got}"


def check_record():
    j = make_journal(FastJournal)
    for bad in ["", "   ", "x" * 51]:
        raises(ValueError, "Diễn giải phải có từ 1 đến 50 ký tự", lambda: record(j, bad, "100"))
    for bad in ["0", "-0", "1.5", "abc", "", "-", "--5"]:
        raises(ValueError, "Số tiền phải là số nguyên khác 0", lambda: record(j, "Chi", bad))
    assert j.size() == 4 and j.issued == 4


def check_benchmark():
    rows = run_limited(lambda: benchmark((100, 200)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [100, 200] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Đã hoàn tác BT0004 (+7.200.000đ).", "Số dư: +5.150.000đ (3 bút toán)", "Đã ghi BT0005: -1.250.000đ.",
        "Lỗi: Diễn giải phải có từ 1 đến 50 ký tự", "Lỗi: Số tiền phải là số nguyên khác 0", "Đã hoàn tác BT0005 (-1.250.000đ).",
        "Đã hoàn tác BT0003 (-9.000.000đ).", "Số dư: +14.150.000đ (2 bút toán)", "BT0002 | Chi mua văn phòng phẩm | -850.000đ",
        "BT0001 | Thu tiền khách hàng A | +15.000.000đ", "Lỗi: Số bút toán phải là số nguyên dương", "Đã hoàn tác BT0001 (+15.000.000đ).",
        "Lỗi: Không còn bút toán để hoàn tác", "Số dư: +0đ (0 bút toán)", "n | bản cũ (ms) | bản mới (ms)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 6.", "Đã khóa sổ. Tạm biệt!",
    ])


CHECKS = [
    ("FastJournal trên dữ liệu mẫu, hoàn tác hết, rỗng, ghi lại", check_sample),
    ("khớp bản cũ trên 200 chuỗi thao tác ngẫu nhiên", check_same),
    ("không duyệt ở thao tác cuối, số dư, kích thước; dùng DNode", check_rules),
    ("bản mới với 100.000 bút toán trong 1 giây", check_fast),
    ("ghi bút toán, dữ liệu sai", check_record),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '3',
    '4',
    '2',
    'Chi tiền điện',
    '-1250000',
    '2',
    '   ',
    '500',
    '2',
    'Thu tạm ứng',
    '0',
    '3',
    '3',
    '4',
    '1',
    '10',
    '1',
    '0',
    '3',
    '3',
    '3',
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
