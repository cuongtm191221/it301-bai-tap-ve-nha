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
import vi_dien_tu
from vi_dien_tu import make_txs, make_big_txs, net_rec, net_loop, balance, largest_spend, add_tx, benchmark, recursion_fails


def recursive_only(func):
    body = inspect.getsource(func).split('"""', 2)[-1]
    assert func.__name__ + "(" in body, f"{func.__name__} phải gọi lại chính nó (đệ quy)"
    assert "for " not in body and "while " not in body, f"{func.__name__} không được dùng vòng lặp"
    assert "[i + 1:]" not in body and "[1:]" not in body, f"{func.__name__} phải đệ quy theo chỉ số, không cắt list"


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_net():
    txs = make_txs()
    assert net_rec(txs) == 411000 and net_loop(txs) == 411000, f"số dư mẫu ra {net_rec(txs)}, {net_loop(txs)}"
    assert net_rec([]) == 0 and net_loop([]) == 0 and net_rec(txs, 6) == 0
    recursive_only(vi_dien_tu.net_rec)
    body = inspect.getsource(vi_dien_tu.net_loop).split('"""', 2)[-1]
    assert "net_loop(" not in body and "net_rec(" not in body, "net_loop phải dùng vòng lặp, không đệ quy"


def check_balance_choice():
    small = make_big_txs(500)
    big = make_big_txs(100000)
    assert balance(small) == (net_loop(small), "đệ quy"), "500 giao dịch phải dùng đệ quy"
    got = run_limited(lambda: balance(big), 2, "100.000 giao dịch quá 2 giây")
    assert got == (net_loop(big), "vòng lặp"), f"100.000 giao dịch phải dùng vòng lặp, ra {got[1]}"


def check_recursion_error():
    assert recursion_fails(5000) is True and recursion_fails(100) is False, "đệ quy 5.000 tầng phải gặp RecursionError, 100 tầng thì không"


def check_largest():
    txs = make_txs()
    assert largest_spend(txs)[0] == "ZP003" and largest_spend([]) is None, "khoản chi lớn nhất sai"
    assert largest_spend([["A", "NAP", 9]]) is None
    assert largest_spend([["A", "CHI", 5], ["B", "CHI", 5]])[0] == "A", "bằng nhau phải lấy khoản đứng trước"
    recursive_only(vi_dien_tu.largest_spend)


def check_add():
    txs = make_txs()
    assert add_tx(txs, " chi ", "150000") == ["ZP007", "CHI", 150000] and net_loop(txs) == 261000
    raises("Số dư không đủ: còn 261.000đ", lambda: add_tx(txs, "CHI", "261001"))
    raises("Loại phải là NAP hoặc CHI", lambda: add_tx(txs, "rut", "100"))
    for bad in ["0", "-5", "1.5", ""]:
        raises("Số tiền phải là số nguyên dương", lambda: add_tx(txs, "NAP", bad))
    assert len(txs) == 7 and add_tx(txs, "CHI", "261000")[2] == 261000 and net_loop(txs) == 0, "chi đúng bằng số dư phải được"


def check_benchmark():
    rows = run_limited(lambda: benchmark((50, 100), number=3), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [50, 100] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Số dư: 411.000đ (tính bằng đệ quy, 6 giao dịch)", "Khoản chi lớn nhất: ZP003 120.000đ", "Đã ghi ZP007. Số dư: 261.000đ",
        "Lỗi: Số dư không đủ: còn 261.000đ", "Lỗi: Loại phải là NAP hoặc CHI", "Lỗi: Số tiền phải là số nguyên dương",
        "Khoản chi lớn nhất: ZP007 150.000đ", "Đã nạp lịch sử 20006 giao dịch.", "(tính bằng vòng lặp, 20006 giao dịch)",
        "n | đệ quy (ms) | vòng lặp (ms)", "Đệ quy với 5000 giao dịch: gặp RecursionError",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã đăng xuất ví. Tạm biệt!",
    ])


CHECKS = [
    ("số dư bằng đệ quy theo chỉ số và bằng vòng lặp", check_net),
    ("chọn cách tính theo độ dài lịch sử", check_balance_choice),
    ("đệ quy quá sâu gặp RecursionError", check_recursion_error),
    ("khoản chi lớn nhất (đệ quy)", check_largest),
    ("nạp, chi và dữ liệu sai", check_add),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    'chi',
    '150000',
    '2',
    'CHI',
    '999999',
    '2',
    'rut',
    '100',
    '2',
    'NAP',
    '0',
    '1',
    '3',
    '1',
    '4',
    'abc',
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
