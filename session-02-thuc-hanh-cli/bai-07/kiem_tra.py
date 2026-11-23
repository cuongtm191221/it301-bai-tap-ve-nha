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
from doi_soat import make_books, make_big_books, add_tx, summary, reconcile_v1, reconcile_v2, benchmark

EXPECTED = (["VP1005"], ["VP1004"], [("VP1003", 89000, 98000)])


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_add_summary():
    system, bank = make_books()
    assert summary(system) == (5, 4299000) and summary(bank) == (5, 3793000), "tóm tắt hai sổ sai"
    assert add_tx(bank, " vp1005", "560000") == ["VP1005", 560000], "thêm giao dịch sai"
    raises("Mã VP1001 đã có trong sổ", lambda: add_tx(system, "vp1001", "10"))
    raises("Mã giao dịch phải gồm VP và 4 chữ số trở lên", lambda: add_tx(system, "VP12", "10"))
    raises("Mã giao dịch phải gồm VP và 4 chữ số trở lên", lambda: add_tx(system, "AB1234", "10"))
    for bad in ["0", "-1", "1.5", ""]:
        raises("Số tiền phải là số nguyên dương", lambda: add_tx(system, "VP2000", bad))
    assert len(system) == 5, "dữ liệu sai không được thêm vào sổ"


def check_v1():
    system, bank = make_books()
    assert reconcile_v1(system, bank) == EXPECTED, f"giải pháp 1 ra {reconcile_v1(system, bank)}"
    assert (system, bank) == make_books(), "giải pháp 1 làm đổi sổ"


def check_v2():
    system, bank = make_books()
    assert reconcile_v2(system, bank) == EXPECTED, f"giải pháp 2 ra {reconcile_v2(system, bank)}"
    assert (system, bank) == make_books(), "giải pháp 2 làm đổi sổ"


def check_edges():
    for f in (reconcile_v1, reconcile_v2):
        assert f([], []) == ([], [], []), f"{f.__name__}: hai sổ rỗng"
        assert f([["VP1", 5]], []) == (["VP1"], [], []) and f([], [["VP2", 5]]) == ([], ["VP2"], []), f"{f.__name__}: một sổ rỗng"


def check_same_random():
    rng = random.Random(7)
    for _ in range(200):
        codes = [f"VP{k:04d}" for k in rng.sample(range(40), rng.randint(0, 25))]
        system = [[c, rng.randint(1, 3)] for c in codes if rng.random() < 0.8]
        bank = [[c, rng.randint(1, 3)] for c in codes if rng.random() < 0.8]
        rng.shuffle(bank)
        assert reconcile_v1(system, bank) == reconcile_v2(system, bank), f"hai giải pháp khác kết quả với {system} và {bank}"


def check_v2_fast():
    system, bank = make_big_books(100000)
    got = run_limited(lambda: reconcile_v2(system, bank), 2, "giải pháp 2 với 100.000 giao dịch quá 2 giây")
    assert len(got[0]) == 2000 and len(got[2]) == 1010, f"100.000 giao dịch: {len(got[0])} thiếu, {len(got[2])} lệch"


def check_benchmark():
    rows = run_limited(lambda: benchmark((200, 400)), 10, "đo hiệu năng quá 10 giây")
    assert [r[0] for r in rows] == [200, 400] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Hệ thống: 5 giao dịch, tổng 4.299.000đ", "Ngân hàng: 5 giao dịch, tổng 3.793.000đ",
        "Chỉ có ở hệ thống: VP1005", "Chỉ có ở ngân hàng: VP1004", "Lệch số tiền: VP1003 hệ thống 89.000đ, ngân hàng 98.000đ",
        "Chỉ có ở hệ thống: VP1005", "Đã thêm VP1005 560.000đ. Sổ có 6 giao dịch.", "Chỉ có ở hệ thống: (không có)",
        "Lỗi: Mã VP1001 đã có trong sổ", "Lỗi: Mã giao dịch phải gồm VP và 4 chữ số trở lên", "Lỗi: Số tiền phải là số nguyên dương",
        "Lựa chọn không hợp lệ.", "Lựa chọn không hợp lệ.", "n | giải pháp 1 (ms) | giải pháp 2 (ms)", "4000 |",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã lưu biên bản đối soát. Tạm biệt!",
    ])


CHECKS = [
    ("thêm giao dịch, tóm tắt, dữ liệu sai", check_add_summary),
    ("giải pháp 1 trên dữ liệu mẫu", check_v1),
    ("giải pháp 2 trên dữ liệu mẫu", check_v2),
    ("sổ rỗng", check_edges),
    ("hai giải pháp cùng kết quả trên 200 bộ ngẫu nhiên", check_same_random),
    ("giải pháp 2 với 100.000 giao dịch", check_v2_fast),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '1',
    '3',
    '2',
    '2',
    '2',
    'vp1005',
    '560000',
    '3',
    '2',
    '2',
    '1',
    'VP1001',
    '10',
    '2',
    '1',
    'VP12',
    '10',
    '2',
    '2',
    'VP1007',
    '0',
    '2',
    '3',
    '3',
    '0',
    '4',
    '6',
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
