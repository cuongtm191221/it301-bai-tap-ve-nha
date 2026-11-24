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
import quay_thu_ngan
from quay_thu_ngan import Lane, make_store, make_big_lanes, join, serve, merge_v1, merge_v2, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def lane_of(values):
    lane = Lane()
    for v in values:
        lane.add_last(v)
    return lane


def nodes(lane):
    out, node = [], lane.head
    while node is not None:
        out.append(node)
        node = node.next
    return out


def verify_merge(fn, xs, ys):
    a, b = lane_of(xs), lane_of(ys)
    before = set(map(id, nodes(a) + nodes(b)))
    moved = fn(a, b)
    after = nodes(a)
    got = [n.value for n in after]
    assert got == sorted(xs + ys), f"{fn.__name__}({xs}, {ys}) ra {got}"
    assert moved == len(ys), f"{fn.__name__} phải trả số khách chuyển ({len(ys)}), ra {moved}"
    assert set(map(id, after)) == before, f"{fn.__name__} không được tạo node mới"
    assert b.head is None and b.tail is None, f"{fn.__name__}: quầy 2 phải rỗng"
    if after:
        assert a.head is after[0] and a.tail is after[-1] and a.tail.next is None, f"{fn.__name__}: head, tail quầy 1 sai"
    else:
        assert a.head is None and a.tail is None
    a.add_last(10**9)
    assert a.to_text().endswith(f"{10**9} -> None"), f"{fn.__name__}: thêm khách sau khi gộp bị sai"


CASES = [([101, 104, 105, 109], [103, 106, 107, 108, 110]), ([], [1, 2]), ([1, 2], []), ([], []), ([5, 9], [1, 2]), ([1, 2], [5, 9])]


def check_v1():
    for xs, ys in CASES:
        verify_merge(merge_v1, xs, ys)


def check_v2():
    for xs, ys in CASES:
        verify_merge(merge_v2, xs, ys)
    for f in (quay_thu_ngan.merge_v1, quay_thu_ngan.merge_v2):
        body = inspect.getsource(f).split('"""', 2)[-1]
        assert "[" not in body and "list(" not in body and "Node(" not in body and "sorted(" not in body, f"{f.__name__} không được dùng list, tạo node, sorted"


def check_same():
    rng = random.Random(8)
    for _ in range(200):
        numbers = rng.sample(range(1, 60), rng.randint(0, 16))
        cut = rng.randint(0, len(numbers))
        xs, ys = sorted(numbers[:cut]), sorted(numbers[cut:])
        verify_merge(merge_v1, xs, ys)
        verify_merge(merge_v2, xs, ys)


def check_fast():
    a, b = make_big_lanes(100000)
    moved = run_limited(lambda: merge_v2(a, b), 1, "giải pháp 2 với 2 x 100.000 khách quá 1 giây")
    assert moved == 100000 and a.head.value == 0 and a.tail.value == 199999 and b.head is None


def check_business():
    store = make_store()
    assert store.lanes[0].to_text() == "101 -> 104 -> 105 -> 109 -> None" and store.lanes[1].to_text() == "103 -> 106 -> 107 -> 108 -> 110 -> None"
    assert join(store, " 1 ") == 111 and join(store, "2") == 112
    for bad in ["3", "0", "a", ""]:
        raises("Quầy phải là 1 hoặc 2", lambda: join(store, bad))
    assert serve(store, "2") == 103 and serve(store, "1") == 101
    merge_v2(store.lanes[0], store.lanes[1])
    raises("Quầy 2 không có khách", lambda: serve(store, "2"))
    assert join(store, "2") == 113 and serve(store, "2") == 113


def check_benchmark():
    rows = run_limited(lambda: benchmark((100, 200)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [100, 200] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Quầy 1: 101 -> 104 -> 105 -> 109 -> None", "Quầy 2: 103 -> 106 -> 107 -> 108 -> 110 -> None", "Khách số 111 vào quầy 1.",
        "Lỗi: Quầy phải là 1 hoặc 2", "Quầy 2 phục vụ khách số 103.", "Đã chuyển 4 khách sang quầy 1.",
        "Quầy 1: 101 -> 104 -> 105 -> 106 -> 107 -> 108 -> 109 -> 110 -> 111 -> None", "Quầy 2: None", "Lỗi: Quầy 2 không có khách",
        "Lựa chọn không hợp lệ.", "Đã chuyển 0 khách sang quầy 1.", "n | giải pháp 1 (ms) | giải pháp 2 (ms)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 6.", "Co.opmart cảm ơn quý khách!",
    ])


CHECKS = [
    ("giải pháp 1: gộp đúng thứ tự, không tạo node, head, tail đúng", check_v1),
    ("giải pháp 2: gộp đúng, không tạo node, không dùng list", check_v2),
    ("hai giải pháp trên 200 cặp quầy ngẫu nhiên", check_same),
    ("giải pháp 2 với hai quầy 100.000 khách", check_fast),
    ("khách vào quầy, phục vụ, dữ liệu sai", check_business),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    '1',
    '2',
    '3',
    '4',
    '2',
    '3',
    '2',
    '1',
    '4',
    '2',
    '3',
    'x',
    '3',
    '1',
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
