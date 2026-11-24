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
import quay_thuoc
from quay_thuoc import DrugArray, make_shelf, receive, sell


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_append():
    a = DrugArray()
    caps = []
    for k in range(9):
        a.append(["LC%03d" % k, "Thuốc", 1])
        caps.append(a.capacity())
    assert caps == [1, 2, 4, 4, 8, 8, 8, 8, 16], f"capacity sau từng lần append ra {caps}"
    assert a.size() == 9 and a.copies == 15, f"9 lần append phải chép 15 lần, ra {a.copies}"
    assert a.items() == [["LC%03d" % k, "Thuốc", 1] for k in range(9)], "items sai"


def check_storage_rules():
    src = inspect.getsource(quay_thuoc.DrugArray)
    assert "_data.append" not in src and "_data.insert" not in src, "không dùng append, insert trên _data: vùng lưu trữ có số ô cố định"
    a = DrugArray()
    for k in range(5):
        a.append([k])
    assert len(a._data) == a.capacity() == 8, "vùng lưu trữ phải có đúng capacity ô"
    assert a.items() == [[0], [1], [2], [3], [4]], "items không được lấy ô trống"


def check_find():
    s = make_shelf()
    assert s.find("LC101") == 0 and s.checks == 1, "tìm mã đầu phải so sánh 1 lần"
    s.checks = 0
    assert s.find(" lc103 ") == 2 and s.checks == 3, "tìm mã cuối phải so sánh 3 lần"
    s.checks = 0
    assert s.find("LC999") is None and s.checks == 3, "mã không có phải trả None sau 3 lần so sánh"


def check_receive_sell():
    s = make_shelf()
    assert receive(s, "LC104", " Men vi sinh ", "30") == ("thêm", ["LC104", "Men vi sinh", 30]) and s.size() == 4
    assert receive(s, "lc102", "", "10") == ("cộng", ["LC102", "Berberin", 25]) and s.size() == 4, "mã đã có phải cộng dồn"
    assert sell(s, "LC101", "24")[2] == 0, "bán hết phải còn 0"
    raises("Không đủ hàng: còn 0 hộp", lambda: sell(s, "LC101", "1"))
    raises("Không có thuốc LC999", lambda: sell(s, "lc999", "1"))
    raises("Mã thuốc phải có dạng LC và 3 chữ số", lambda: receive(s, "LC10", "X", "5"))
    raises("Số hộp phải là số nguyên dương", lambda: receive(s, "LC105", "X", "0"))
    raises("Tên thuốc không được để trống", lambda: receive(s, "LC105", "  ", "5"))
    assert s.size() == 4


def check_many():
    def job():
        a = DrugArray()
        for k in range(100000):
            a.append([k])
        return a.copies, a.capacity()
    got = run_limited(job, 2, "100.000 lần append quá 2 giây")
    assert got == (131071, 131072), f"100.000 lần append ra copies, capacity = {got}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "3. LC103 | Vitamin C 500mg | 40 hộp", "Đang lưu 3/4 ô, đã chép 0 lần", "Đã thêm mới LC104: còn 30 hộp.",
        "Đã cộng thêm LC102: còn 25 hộp.", "Đang lưu 4/4 ô, đã chép 0 lần", "Vị trí 3: Vitamin C 500mg, còn 40 hộp (so sánh 3 mã).",
        "Không có thuốc này (so sánh 4 mã).", "Lỗi: Không đủ hàng: còn 24 hộp", "Lỗi: Số hộp phải là số nguyên dương",
        "Lỗi: Mã thuốc phải có dạng LC và 3 chữ số", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã đóng quầy. Chúc sức khỏe!",
    ])


CHECKS = [
    ("append gấp đôi capacity, đếm copies", check_append),
    ("vùng lưu trữ có số ô cố định", check_storage_rules),
    ("tìm theo mã, đếm checks", check_find),
    ("nhập, bán thuốc và dữ liệu sai", check_receive_sell),
    ("100.000 lần append", check_many),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    'LC104',
    'Men vi sinh Biolactyl',
    '30',
    '2',
    'lc102',
    '',
    '10',
    '1',
    '3',
    'lc103',
    '3',
    'LC999',
    '4',
    'LC101',
    '30',
    '4',
    'LC101',
    '0',
    '2',
    'LC10',
    'X',
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
