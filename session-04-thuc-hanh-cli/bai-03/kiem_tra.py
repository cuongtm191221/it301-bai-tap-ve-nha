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
import van_don
from van_don import clean, luhn_sum, check_digit, normalize, is_valid, invalid_codes, receive, make_parcels


def recursive_only(func):
    body = inspect.getsource(func).split('"""', 2)[-1]
    assert func.__name__ + "(" in body, f"{func.__name__} phải gọi lại chính nó (đệ quy)"
    assert "for " not in body and "while " not in body, f"{func.__name__} không được dùng vòng lặp"


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_clean():
    assert clean(" jt 8402-1937-52 ") == "JT8402193752" and clean("") == "" and clean(" - ") == "", "clean sai"
    recursive_only(van_don.clean)
    assert "replace(" not in inspect.getsource(van_don.clean).split('"""', 2)[-1], "clean không được dùng replace()"


def check_luhn():
    assert luhn_sum("8402193752", False) == 40 and luhn_sum("", True) == 0, f'luhn_sum("8402193752", False) ra {luhn_sum("8402193752", False)}'
    assert [check_digit(b) for b in ["840219375", "512006438", "999999999", "123456789"]] == [2, 0, 9, 7], "chữ số kiểm tra sai"
    recursive_only(van_don.luhn_sum)


def check_valid():
    assert is_valid("JT8402193752") and not is_valid("JT8402193753"), "kiểm tra mã sai"
    assert normalize("jt 2604 5590 19") == "JT2604559019"
    for bad in ["JT12345", "VN8402193752", "JT84021937520", "JT84O2193752", ""]:
        raises("Mã vận đơn phải gồm JT và 10 chữ số", lambda: normalize(bad))


def check_batch():
    codes = ["JT8402193752", " jt5120064380", "JT12345", " JT9999999990 "]
    assert invalid_codes(codes) == ["JT12345", "JT9999999990"], f"lô mã ra {invalid_codes(codes)}"
    assert invalid_codes([]) == []
    recursive_only(van_don.invalid_codes)


def check_receive():
    ps = make_parcels()
    assert receive(ps, "JT 2604 5590 19", " Phạm Minh Thư ") == ["JT2604559019", "Phạm Minh Thư"] and len(ps) == 4
    raises("Mã vận đơn sai chữ số kiểm tra", lambda: receive(ps, "JT8402193753", "A"))
    raises("Mã JT8402193752 đã được nhận", lambda: receive(ps, "jt8402193752", "A"))
    raises("Người nhận không được để trống", lambda: receive(ps, "JT1234567897", "  "))
    assert len(ps) == 4, "dữ liệu sai không được nhận"


def check_long():
    codes = ["JT8402193752"] * 300 + ["X"]
    got = run_limited(lambda: invalid_codes(codes), 2, "lô 301 mã quá 2 giây")
    assert got == ["X"]


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Mã JT8402193752 hợp lệ.", "Mã JT8402193753 sai chữ số kiểm tra.", "Mã đầy đủ: JT2604559019",
        "Đã nhận JT2604559019 cho Phạm Minh Thư. Có 4 đơn.", "Hợp lệ 2/4 mã.", "Mã sai: JT12345, JT9999999990",
        "Lỗi: Mã JT8402193752 đã được nhận", "Lỗi: Mã vận đơn phải gồm JT và 10 chữ số", "Lỗi: Cần đúng 9 chữ số",
        "Lựa chọn không hợp lệ.", "4. JT2604559019 | Phạm Minh Thư", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.",
        "Đã đóng ca nhận hàng. Tạm biệt!",
    ])


CHECKS = [
    ("làm sạch mã (đệ quy)", check_clean),
    ("tổng Luhn và chữ số kiểm tra (đệ quy)", check_luhn),
    ("kiểm tra dạng mã và chữ số kiểm tra", check_valid),
    ("lọc mã sai trong lô (đệ quy)", check_batch),
    ("nhận đơn và dữ liệu sai", check_receive),
    ("lô 301 mã", check_long),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '1',
    'jt 8402-1937-52',
    '1',
    '1',
    'JT8402193753',
    '1',
    '2',
    '260455901',
    '2',
    'JT 2604 5590 19',
    'Phạm Minh Thư',
    '3',
    'JT8402193752, jt5120064380,JT12345, JT9999999990',
    '2',
    'JT8402193752',
    'Ai Đó',
    '2',
    'JT84021937',
    'Ai Đó',
    '1',
    '2',
    '12345',
    '1',
    '3',
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
