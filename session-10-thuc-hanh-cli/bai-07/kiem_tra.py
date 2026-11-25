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
import cap_treo
from cap_treo import QueueV1, QueueV2, Station, make_station, join, board, switch, workload, benchmark


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


def basic(cls):
    q = cls(3)
    raises(IndexError, "hàng đợi rỗng", q.dequeue)
    raises(IndexError, "hàng đợi rỗng", q.peek)
    for v in "abc":
        q.enqueue(v)
    assert q.is_full() and q.size() == 3 and q.items() == ["a", "b", "c"]
    raises(ValueError, "Hàng chờ đã đầy", lambda: q.enqueue("d"))
    assert q.dequeue() == "a" and q.peek() == "b" and not q.is_full()
    q.enqueue("d")
    assert q.items() == ["b", "c", "d"] and q.size() == 3, f"{cls.__name__}: quay vòng sai, ra {q.items()}"
    assert [q.dequeue() for _ in range(3)] == ["b", "c", "d"] and q.size() == 0 and q.items() == []
    q.enqueue("e")
    assert q.peek() == "e" and q.items() == ["e"]


def check_v1():
    basic(QueueV1)


def check_v2():
    basic(QueueV2)
    for name in ("enqueue", "dequeue", "peek", "size", "is_full"):
        body = inspect.getsource(getattr(QueueV2, name)).split('"""', 2)[-1]
        for banned in (".append(", ".pop(", ".insert(", "del ", ":]", "[:", "deque", "while", "for "):
            assert banned not in body, f"QueueV2.{name} không được dùng {banned.strip()}"


def check_same():
    rng = random.Random(7)
    for _ in range(200):
        cap = rng.randint(1, 5)
        a, b = QueueV1(cap), QueueV2(cap)
        for step in range(30):
            op = rng.choice(["enq", "enq", "deq", "peek", "items"])
            if op == "enq":
                r1, r2 = outcome(lambda: a.enqueue(step)), outcome(lambda: b.enqueue(step))
            elif op == "deq":
                r1, r2 = outcome(a.dequeue), outcome(b.dequeue)
            elif op == "peek":
                r1, r2 = outcome(a.peek), outcome(b.peek)
            else:
                r1, r2 = (a.items(), a.size(), a.is_full()), (b.items(), b.size(), b.is_full())
            assert r1 == r2, f"thao tác {op}, sức chứa {cap}: giải pháp 1 ra {r1}, giải pháp 2 ra {r2}"


def check_fast():
    run_limited(lambda: workload(QueueV2, 100000), 1, "giải pháp 2: 100.000 chỗ, hai vòng thêm đầy lấy hết quá 1 giây")


def check_business():
    st = make_station(QueueV2)
    assert st.queue.items() == ["CT%04d" % k for k in range(1, 9)]
    assert join(st, " 2 ") == ["CT0009", "CT0010"]
    raises(ValueError, "Hàng chờ chỉ còn 2 chỗ", lambda: join(st, "5"))
    for bad in ["0", "11", "a", ""]:
        raises(ValueError, "Số khách phải từ 1 đến 10", lambda: join(st, bad))
    assert st.queue.size() == 10 and st.issued == 10
    assert board(st) == ["CT0001", "CT0002", "CT0003", "CT0004", "CT0005", "CT0006"]
    switch(st, QueueV1)
    assert type(st.queue) is QueueV1 and st.queue.items() == ["CT0007", "CT0008", "CT0009", "CT0010"]
    assert board(st) == ["CT0007", "CT0008", "CT0009", "CT0010"]
    raises(ValueError, "Không có khách đang chờ", lambda: board(st))


def check_benchmark():
    rows = run_limited(lambda: benchmark((200, 400)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [200, 400] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "CT0001, CT0002, CT0003, CT0004, CT0005, CT0006, CT0007, CT0008", "Đang chờ 8/12 khách", "Đang dùng giải pháp 2, giữ 8 khách.",
        "Lỗi: Hàng chờ chỉ còn 4 chỗ", "Đã cấp vé CT0009 đến CT0012.", "Đang chờ 12/12 khách (đầy)",
        "Cabin chở: CT0001, CT0002, CT0003, CT0004, CT0005, CT0006", "Đã cấp vé CT0013 đến CT0018.",
        "Cabin chở: CT0007, CT0008, CT0009, CT0010, CT0011, CT0012", "Cabin chở: CT0013, CT0014, CT0015, CT0016, CT0017, CT0018",
        "Lỗi: Không có khách đang chờ", "Lựa chọn không hợp lệ.", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 6.",
        "Cáp treo dừng hoạt động. Tạm biệt!",
    ])


CHECKS = [
    ("giải pháp 1: thêm, lấy, đầy, rỗng, thêm sau khi lấy", check_v1),
    ("giải pháp 2: cùng hành vi, không append, pop, insert, cắt lát", check_v2),
    ("hai giải pháp trên 200 chuỗi thao tác ngẫu nhiên", check_same),
    ("giải pháp 2 với khu chờ 100.000 chỗ", check_fast),
    ("xếp hàng theo nhóm, cabin rời ga, chuyển giải pháp", check_business),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '4',
    '2',
    '2',
    '5',
    '2',
    '4',
    '1',
    '3',
    '2',
    '6',
    '3',
    '3',
    '3',
    '4',
    'x',
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
