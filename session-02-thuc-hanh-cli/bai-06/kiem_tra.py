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


from so_quy import make_book, balance, running_balances, next_code, add_tx, totals, top_expenses, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_balance():
    book = make_book()
    assert balance(book) == 3150000 and balance([]) == 2000000, f"số dư mẫu ra {balance(book)}"
    got = running_balances(book)
    assert got == [2450000, 2330000, 3310000, 3010000, 3225000, 3150000], f"số dư sau từng giao dịch ra {got}"
    assert running_balances([]) == [], "sổ rỗng phải trả list rỗng"


def check_running_fast():
    book = [[f"GD{k}", "THU", 1000] for k in range(40000)]
    got = run_limited(lambda: running_balances(book), 1, "40.000 giao dịch quá 1 giây: số dư từng dòng phải tính trong một lượt")
    assert got[-1] == 2000000 + 40000 * 1000


def check_add():
    book = make_book()
    assert next_code(book) == "GD007" and next_code([]) == "GD001", "mã giao dịch tiếp theo sai"
    assert add_tx(book, " chi ", "500000") == ["GD007", "CHI", 500000] and balance(book) == 2650000, "ghi CHI 500.000 sai"
    cases = [(("rut", "1000"), "Loại giao dịch phải là THU hoặc CHI"), (("THU", "0"), "Số tiền phải là số nguyên dương"),
             (("THU", "-5"), "Số tiền phải là số nguyên dương"), (("THU", "1.5"), "Số tiền phải là số nguyên dương"),
             (("CHI", "2650001"), "Không đủ tiền trong quỹ: số dư 2.650.000đ")]
    for args, message in cases:
        before = [tx[:] for tx in book]
        raises(message, lambda: add_tx(book, *args))
        assert book == before, f"{args}: sổ bị thay đổi dù dữ liệu sai"
    assert add_tx(book, "CHI", "2650000")[2] == 2650000 and balance(book) == 0, "chi đúng bằng số dư phải được"


def check_report():
    book = make_book()
    assert totals(book) == (1645000, 495000, 3150000), f"tổng thu chi ra {totals(book)}"
    top = top_expenses(book, 3)
    assert [tx[0] for tx in top] == ["GD004", "GD002", "GD006"], f"top chi ra {top}"
    assert book == make_book(), "top_expenses làm đổi sổ"
    tie = [["A", "CHI", 5], ["B", "THU", 9], ["C", "CHI", 5]]
    assert [tx[0] for tx in top_expenses(tie, 3)] == ["A", "C"] and top_expenses([], 3) == [], "bằng nhau giữ thứ tự sổ; sổ rỗng"


def check_benchmark():
    rows = run_limited(lambda: benchmark((1000, 2000), number=3), 10, "đo hiệu năng quá 10 giây")
    assert [r[0] for r in rows] == [1000, 2000] and all(r[1] > 0 for r in rows), f"benchmark ra {rows}"
    assert rows[1][2] > rows[0][2] > 1000 * 8, "byte phải là sys.getsizeof của list sổ"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "GD001 | THU | 450.000đ | số dư 2.450.000đ", "GD006 | CHI | 75.000đ | số dư 3.150.000đ", "Đã ghi GD007. Số dư: 2.650.000đ",
        "GD007 | CHI | 500.000đ", "GD006 | CHI | 75.000đ", "Lỗi: Không đủ tiền trong quỹ: số dư 2.650.000đ",
        "Lỗi: Loại giao dịch phải là THU hoặc CHI", "Lỗi: Số tiền phải là số nguyên dương",
        "Tổng thu: 1.645.000đ | Tổng chi: 995.000đ | Số dư: 2.650.000đ", "1. GD007 | CHI | 500.000đ",
        "Lỗi: Số giao dịch phải là số nguyên dương", "Lựa chọn không hợp lệ.", "n | tính số dư (ms) | getsizeof list sổ (byte)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Chốt ca với số dư 2.650.000đ. Tạm biệt!",
    ])


CHECKS = [
    ("số dư cuối và số dư sau từng giao dịch", check_balance),
    ("số dư từng dòng của 40.000 giao dịch trong 1 giây", check_running_fast),
    ("ghi giao dịch và dữ liệu sai", check_add),
    ("tổng thu chi, top khoản chi", check_report),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '1',
    '2',
    'chi',
    '500000',
    '1',
    '2',
    '2',
    '2',
    'CHI',
    '99999999',
    '2',
    'rut',
    '100000',
    '2',
    'THU',
    '0',
    '3',
    '1',
    '3',
    '2',
    '1',
    '2',
    'abc',
    '3',
    '9',
    '4',
    '0',
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
