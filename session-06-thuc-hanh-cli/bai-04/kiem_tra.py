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
import lo_trinh
from lo_trinh import make_route, insert_stop, remove_stop, reverse_range, reverse_route, rotate_route


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def no_shortcuts(func):
    body = inspect.getsource(func).split('"""', 2)[-1]
    for banned in (".insert(", ".pop(0", ".pop(pos", ".pop(i", "reverse(", "[::-1]", "reversed(", ":]", "[:"):
        assert banned not in body, f"{func.__name__} không được dùng {banned}"


def check_insert():
    r = make_route()
    assert insert_stop(r, 2, " Vincom Đồng Khởi ") == 4 and r[1] == "Vincom Đồng Khởi" and r[2] == "Chợ Bến Thành", "chèn vào vị trí 2 sai"
    assert insert_stop(r, 7, "Ga Sài Gòn") == 0 and r[-1] == "Ga Sài Gòn", "chèn vào cuối phải dịch 0 điểm"
    assert insert_stop(r, 1, "Kho Quận 7") == 7 and r[0] == "Kho Quận 7", "chèn vào đầu phải dịch cả 7 điểm"
    raises("Vị trí phải từ 1 đến 9", lambda: insert_stop(r, 10, "X"))
    raises("Vị trí phải từ 1 đến 9", lambda: insert_stop(r, 0, "X"))
    raises("Tên điểm dừng phải có từ 1 đến 40 ký tự", lambda: insert_stop(r, 1, "   "))
    assert len(r) == 8
    no_shortcuts(lo_trinh.insert_stop)


def check_remove():
    r = make_route()
    assert remove_stop(r, 3) == ("Nhà thờ Đức Bà", 2) and r == ["Kho Quận 1", "Chợ Bến Thành", "Landmark 81", "Thảo Điền"]
    assert remove_stop(r, 4) == ("Thảo Điền", 0)
    raises("Vị trí phải từ 1 đến 3", lambda: remove_stop(r, 4))
    raises("Vị trí phải từ 1 đến 0", lambda: remove_stop([], 1))
    no_shortcuts(lo_trinh.remove_stop)


def check_reverse():
    r = make_route()
    assert reverse_route(r) == 2 and r == make_route()[::-1], "đảo ngược 5 điểm phải đổi chỗ 2 lần"
    assert reverse_route([]) == 0
    x = [1, 2, 3, 4, 5, 6]
    assert reverse_range(x, 1, 4) == 2 and x == [1, 5, 4, 3, 2, 6]
    no_shortcuts(lo_trinh.reverse_range)


def check_rotate():
    r = make_route()
    rotate_route(r, 3)
    assert r == ["Nhà thờ Đức Bà", "Landmark 81", "Thảo Điền", "Kho Quận 1", "Chợ Bến Thành"], f"xoay bắt đầu từ điểm 3 ra {r}"
    r = make_route()
    rotate_route(r, 1)
    assert r == make_route(), "bắt đầu từ điểm 1 phải giữ nguyên"
    r = make_route()
    rotate_route(r, 5)
    assert r[0] == "Thảo Điền" and r[1] == "Kho Quận 1"
    raises("Vị trí phải từ 1 đến 5", lambda: rotate_route(make_route(), 6))
    no_shortcuts(lo_trinh.rotate_route)


def check_big():
    def job():
        r = list(range(200000))
        swaps = rotate_route(r, 100001)
        return r[0], r[-1], swaps
    got = run_limited(job, 2, "xoay 200.000 điểm quá 2 giây")
    assert got == (100000, 99999, 200000), f"xoay 200.000 điểm ra {got}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "1. Kho Quận 1 -> 2. Chợ Bến Thành", "Đã chèn vào vị trí 2 (dịch 4 điểm).", "Lỗi: Vị trí phải từ 1 đến 7",
        "Lỗi: Vị trí phải từ 1 đến 6", "Đã xoay (6 lần đổi chỗ).", "1. Chợ Bến Thành", "Đã đảo ngược (3 lần đổi chỗ).",
        "Lỗi: Vị trí phải là số nguyên", "Lỗi: Tên điểm dừng phải có từ 1 đến 40 ký tự",
        "Lựa chọn không hợp lệ.", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Chúc tài xế giao hàng thuận lợi!",
    ])


CHECKS = [
    ("chèn điểm dừng, đếm số điểm dịch", check_insert),
    ("xóa điểm dừng, đếm số điểm dịch", check_remove),
    ("đảo ngược bằng hai chỉ số", check_reverse),
    ("xoay lộ trình tại chỗ", check_rotate),
    ("xoay 200.000 điểm", check_big),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    '2',
    'Vincom Đồng Khởi',
    '2',
    '9',
    'X',
    '3',
    '0',
    '4',
    '2',
    '3',
    '1',
    '4',
    '1',
    '3',
    'abc',
    '2',
    '1',
    '',
    '4',
    '5',
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
