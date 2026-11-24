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


import sys
import inspect
import sao_ke
from sao_ke import make_txs, make_big_txs, statement_slow, add_tx, latest_first, capacity_steps, benchmark


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_latest():
    txs = make_txs()
    assert [t[0] for t in latest_first(txs, 3)] == ["MB005", "MB004", "MB003"], "3 giao dịch gần nhất sai"
    assert latest_first(txs, 10) == statement_slow(txs) and latest_first([], 3) == [], "k lớn hoặc lịch sử rỗng sai"
    assert txs == make_txs(), "latest_first làm đổi lịch sử"
    body = inspect.getsource(sao_ke.latest_first).split('"""', 2)[-1]
    for banned in (".insert(", "reverse(", "[::-1]", "reversed("):
        assert banned not in body, f"latest_first không được dùng {banned}"


def check_latest_fast():
    txs = make_big_txs(300000)
    got = run_limited(lambda: latest_first(txs, 300000), 1, "300.000 giao dịch quá 1 giây")
    assert got[0][0] == "MB300000" and got[-1][0] == "MB000001"


def check_add():
    txs = make_txs()
    assert add_tx(txs, " Trà sữa ", "-45000") == ["MB006", "Trà sữa", -45000]
    assert add_tx(txs, "Thưởng", "+500000")[2] == 500000
    raises("Nội dung không được để trống", lambda: add_tx(txs, "  ", "1000"))
    for bad in ["0", "-0", "abc", "1.5", "", "-"]:
        raises("Số tiền phải là số nguyên khác 0 (âm là tiền ra)", lambda: add_tx(txs, "X", bad))
    assert len(txs) == 7


def check_capacity():
    steps = capacity_steps(40)
    data, expected = [], [(0, sys.getsizeof([]))]
    for _ in range(40):
        data.append(0)
        if sys.getsizeof(data) != expected[-1][1]:
            expected.append((len(data), sys.getsizeof(data)))
    assert steps == expected, f"các mốc đổi dung lượng ra {steps}, trên máy này phải là {expected}"
    assert len(steps) >= 4, "40 lần thêm phải có ít nhất 3 lần đổi vùng nhớ"


def check_benchmark():
    rows = run_limited(lambda: benchmark((500, 1000), number=1), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [500, 1000] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "MB005 | Tiền nhà | -4.500.000đ", "MB003 | Chuyển khoản cho mẹ | -2.000.000đ", "Đã ghi MB006: -45.000đ.",
        "Lỗi: Nội dung không được để trống", "Lỗi: Số tiền phải là số nguyên khác 0 (âm là tiền ra)", "MB001 | Lương tháng 10 | +15.000.000đ",
        "số phần tử | getsizeof (byte)", "Lỗi: Số phần tử phải là số nguyên từ 1 đến 100", "n | insert(0) (ms) | đọc từ cuối (ms)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Cảm ơn quý khách đã sử dụng MB Bank!",
    ])


CHECKS = [
    ("k giao dịch gần nhất, đọc từ cuối", check_latest),
    ("sao kê 300.000 giao dịch", check_latest_fast),
    ("ghi giao dịch và dữ liệu sai", check_add),
    ("các mốc đổi dung lượng của list", check_capacity),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '2',
    'Trà sữa',
    '-45000',
    '2',
    '',
    '1000',
    '2',
    'Tiền thưởng',
    '0',
    '1',
    '10',
    '3',
    '20',
    '3',
    '0',
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
