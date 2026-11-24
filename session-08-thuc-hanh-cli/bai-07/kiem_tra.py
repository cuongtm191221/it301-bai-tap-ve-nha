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
import hanh_trinh
from hanh_trinh import Route, make_route, make_big_route, add_airport, reverse_v1, reverse_v2, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def nodes_of(route):
    out, node = [], route.head
    while node is not None:
        out.append(node)
        node = node.next
    return out


def verify_rev(fn, values):
    route = Route()
    for v in values:
        route.add_last(v)
    before = set(map(id, nodes_of(route)))
    fn(route)
    after = nodes_of(route)
    got = [n.value for n in after]
    assert got == values[::-1], f"{fn.__name__} trên {values} ra {got}"
    assert set(map(id, after)) == before, f"{fn.__name__} không được tạo node mới"
    if values:
        assert route.tail is after[-1] and route.tail.next is None, f"{fn.__name__}: tail sai sau khi đảo"
    else:
        assert route.head is None and route.tail is None


def check_v1():
    for values in (["HAN", "DAD", "SGN", "PQC"], ["HAN", "DAD", "SGN"], ["HAN"], [], ["HAN", "SGN"]):
        verify_rev(reverse_v1, values)


def check_v2():
    for values in (["HAN", "DAD", "SGN", "PQC"], ["HAN", "DAD", "SGN"], ["HAN"], [], ["HAN", "SGN"]):
        verify_rev(reverse_v2, values)
    for f in (hanh_trinh.reverse_v1, hanh_trinh.reverse_v2):
        body = inspect.getsource(f).split('"""', 2)[-1]
        assert "[" not in body and "list(" not in body and "Node(" not in body, f"{f.__name__} không được dùng list, không tạo node"


def check_same():
    rng = random.Random(7)
    for _ in range(200):
        values = [rng.randint(0, 9) for _ in range(rng.randint(0, 12))]
        verify_rev(reverse_v1, values)
        verify_rev(reverse_v2, values)
    route = make_route()
    reverse_v2(route); reverse_v2(route)
    assert route.to_text() == "HAN -> DAD -> SGN -> PQC -> None", "đảo hai lần phải về như cũ"


def check_fast():
    route = make_big_route(200000)
    run_limited(lambda: reverse_v2(route), 1, "giải pháp 2 với 200.000 điểm quá 1 giây")
    assert route.head.value == 199999 and route.tail.value == 0 and route.tail.next is None


def check_add():
    route = make_route()
    assert add_airport(route, " cxr ") == "CXR" and route.tail.value == "CXR"
    raises("Sân bay trùng với điểm cuối hành trình", lambda: add_airport(route, "CXR"))
    for bad in ["HN1", "HA", "HANO", "", "ĐAD"]:
        raises("Mã sân bay phải gồm 3 chữ cái", lambda: add_airport(route, bad))
    reverse_v2(route)
    assert add_airport(route, "VCA") == "VCA" and route.to_text() == "CXR -> PQC -> SGN -> DAD -> HAN -> VCA -> None", "thêm sau khi đảo"


def check_benchmark():
    rows = run_limited(lambda: benchmark((100, 200)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [100, 200] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "HAN -> DAD -> SGN -> PQC -> None", "Chiều về: PQC -> SGN -> DAD -> HAN -> None", "Đã thêm CXR.",
        "Lỗi: Sân bay trùng với điểm cuối hành trình", "Lỗi: Mã sân bay phải gồm 3 chữ cái",
        "Chiều về: CXR -> HAN -> DAD -> SGN -> PQC -> None", "Lựa chọn không hợp lệ.", "n | giải pháp 1 (ms) | giải pháp 2 (ms)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Chúc quý khách thượng lộ bình an!",
    ])


CHECKS = [
    ("giải pháp 1: đảo đúng, không tạo node, tail đúng", check_v1),
    ("giải pháp 2: đảo đúng, không tạo node, không dùng list", check_v2),
    ("hai giải pháp trên 200 hành trình ngẫu nhiên", check_same),
    ("giải pháp 2 với 200.000 điểm", check_fast),
    ("thêm sân bay, dữ liệu sai, thêm sau khi đảo", check_add),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '1',
    '2',
    'cxr',
    '2',
    'CXR',
    '2',
    'HN1',
    '3',
    '2',
    '3',
    'x',
    '4',
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
