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
import tien_dien
from tien_dien import TIERS, make_customers, bill, breakdown, total_bill, top_user, update_reading


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


def check_bill():
    got = [bill(k, TIERS) for k in (0, 40, 50, 51, 230, 400, 401)]
    assert got == [0, 75720, 94650, 96606, 505350, 1025250, 1028552], f"tiền điện 0, 40, 50, 51, 230, 400, 401 kWh ra {got}"
    assert bill(100000, TIERS) == 1025250 + 99600 * 3302, "bậc cuối không giới hạn"
    recursive_only(tien_dien.bill)


def check_breakdown():
    assert breakdown(230, TIERS) == [(1, 50, 94650), (2, 50, 97800), (3, 100, 227100), (4, 30, 85800)], f"chi tiết 230 kWh ra {breakdown(230, TIERS)}"
    assert breakdown(0, TIERS) == [] and breakdown(50, TIERS) == [(1, 50, 94650)]
    recursive_only(tien_dien.breakdown)


def check_total_top():
    cs = make_customers()
    assert total_bill(cs, TIERS) == 1606320, f"tổng cả tổ ra {total_bill(cs, TIERS)}"
    assert total_bill([], TIERS) == 0 and top_user([]) is None
    assert top_user(cs)[0] == "PE003", "hộ dùng nhiều nhất phải là PE003"
    tie = [["A", "x", 0, 10], ["B", "y", 0, 10]]
    assert top_user(tie)[0] == "A", "bằng nhau phải lấy hộ đứng trước"
    recursive_only(tien_dien.total_bill)
    recursive_only(tien_dien.top_user)
    assert cs == make_customers(), "các hàm tính toán làm đổi dữ liệu"


def check_update():
    cs = make_customers()
    assert update_reading(cs, " pe004 ", "350")[3] == 350, "ghi chỉ số sai"
    assert update_reading(cs, "PE002", "880")[3] == 880, "chỉ số mới bằng chỉ số cũ phải được"
    raises("Không có khách hàng PE009", lambda: update_reading(cs, "pe009", "10"))
    raises("Chỉ số phải là số nguyên không âm", lambda: update_reading(cs, "PE002", "1o0"))
    raises("Chỉ số phải là số nguyên không âm", lambda: update_reading(cs, "PE002", "-5"))
    raises("Chỉ số mới không được nhỏ hơn chỉ số cũ (880)", lambda: update_reading(cs, "PE002", "879"))
    assert cs[1][3] == 880


def check_many():
    cs = [[f"PE{k}", "Hộ", 0, 200 + k % 50] for k in range(400)]
    got = run_limited(lambda: (total_bill(cs, TIERS), top_user(cs)[0]), 2, "400 hộ quá 2 giây")
    assert got[1] == "PE49"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "PE001 | Nguyễn Văn Hòa | 230 kWh | 505.350đ", "PE004 | Đỗ Khánh Vy | 0 kWh | 0đ", "Tháng này không dùng điện.", "Bậc 4: 30 kWh = 85.800đ",
        "Đã ghi PE004: 50 kWh, 94.650đ.", "Lỗi: Chỉ số mới không được nhỏ hơn chỉ số cũ (880)",
        "Lỗi: Không có khách hàng PE009", "Lỗi: Chỉ số phải là số nguyên không âm", "Lỗi: Không có khách hàng PE009",
        "Lựa chọn không hợp lệ.", "Tổng tiền điện cả tổ: 1.700.970đ", "Dùng nhiều nhất: PE003 - Lê Minh Tâm (400 kWh)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã chốt sổ ghi điện. Tạm biệt!",
    ])


CHECKS = [
    ("tiền điện bậc thang (đệ quy)", check_bill),
    ("chi tiết từng bậc (đệ quy)", check_breakdown),
    ("tổng cả tổ, hộ dùng nhiều nhất (đệ quy)", check_total_top),
    ("ghi chỉ số mới và dữ liệu sai", check_update),
    ("400 hộ", check_many),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '1',
    '1',
    '2',
    'pe004',
    '1',
    '2',
    'pe001',
    '2',
    'pe004',
    '350',
    '2',
    'PE002',
    '870',
    '2',
    'PE009',
    '10',
    '2',
    'PE002',
    '1o0',
    '1',
    '2',
    'PE009',
    '1',
    '5',
    '3',
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
