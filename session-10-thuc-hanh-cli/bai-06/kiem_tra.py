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
from collections import deque
import man_hinh_bep
from man_hinh_bep import Board, make_board, add_order, finish, keep_last_del, keep_last_deque, bench_window


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def codes(board):
    return [o[0] for o in board.orders]


def check_add():
    b = make_board()
    assert codes(b) == ["JB001", "JB002", "JB003", "JB004", "JB005"]
    assert add_order(b, " Cơm gà sốt cay ") == (("JB006", "Cơm gà sốt cay"), None)
    assert add_order(b, "Khoai tây chiên") == (("JB007", "Khoai tây chiên"), ("JB001", "Gà giòn 2 miếng"))
    assert codes(b) == ["JB002", "JB003", "JB004", "JB005", "JB006", "JB007"] and type(b.orders) is deque and b.orders.maxlen == 6
    for bad in ["", "   ", "x" * 41]:
        raises("Tên món phải có từ 1 đến 40 ký tự", lambda: add_order(b, bad))
    assert b.issued == 7


def check_finish():
    b = make_board()
    assert finish(b, " jb004 ") == ("JB004", "Gà giòn 1 miếng") and codes(b) == ["JB001", "JB002", "JB003", "JB005"]
    raises("Đơn JB004 không có trên màn hình", lambda: finish(b, "JB004"))
    raises("Đơn JB999 không có trên màn hình", lambda: finish(b, "jb999"))
    for item in ["A", "B", "C"]:
        add_order(b, item)
    assert codes(b) == ["JB002", "JB003", "JB005", "JB006", "JB007", "JB008"], "sau khi xong một đơn, màn hình còn chỗ"


def check_keep():
    for n, m in [(3, 10), (5, 5), (5, 2), (1, 4)]:
        got = keep_last_deque(n, m)
        assert type(got) is deque and got.maxlen == n and list(got) == keep_last_del(n, m), f"keep_last_deque({n}, {m}) ra {list(got)}"
    body = inspect.getsource(man_hinh_bep.keep_last_deque).split('"""', 2)[-1]
    assert "maxlen" in body and "popleft" not in body and "del " not in body, "dùng maxlen, không tự xóa"


def check_bench():
    rows = run_limited(lambda: bench_window((50, 100), m=2000), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [50, 100] and all(len(r) == 4 and min(r[1:]) > 0 for r in rows), f"bench_window ra {rows}"
    rows = run_limited(lambda: bench_window((1000, 4000)), 30, "đo quá 30 giây")
    assert rows[1][2] > rows[0][2] * 2, f"cắt lát phải chậm dần khi n tăng, ra {rows}"
    assert rows[1][3] < rows[0][3] * 3, f"deque gần như không đổi khi n tăng, ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "JB001 | Gà giòn 2 miếng", "JB005 | Kem sundae", "Đang hiện 5/6 đơn", "Đã thêm JB006: Cơm gà sốt cay.",
        "Đã thêm JB007: Khoai tây chiên.", "JB001 rời màn hình.", "Đang hiện 6/6 đơn", "Đã xong JB004: Gà giòn 1 miếng.",
        "Lỗi: Đơn JB001 không có trên màn hình", "Lỗi: Tên món phải có từ 1 đến 40 ký tự", "Đã thêm JB008: Nước cam.",
        "JB008 | Nước cam", "Đang hiện 6/6 đơn", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Bếp đóng ca. Tạm biệt!",
    ])
    assert "rời màn hình" not in out.split("Đã thêm JB008")[1].split("[")[0], "còn chỗ thì không có đơn nào rời màn hình"


CHECKS = [
    ("thêm đơn, đủ 6 đơn thì đơn cũ nhất rời màn hình", check_add),
    ("bếp làm xong đơn, mã không có", check_finish),
    ("keep_last_deque dùng maxlen, khớp cách cũ", check_keep),
    ("hàm đo; cắt lát chậm dần, deque gần như không đổi", check_bench),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    'Cơm gà sốt cay',
    '2',
    'Khoai tây chiên',
    '1',
    '3',
    'jb004',
    '3',
    'JB001',
    '2',
    '   ',
    '2',
    'Nước cam',
    '1',
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
