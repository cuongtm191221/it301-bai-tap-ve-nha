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
from lich_hen import make_appointments, make_big_appointments, book, cancel, clean_v1, clean_v2, benchmark, WAITING, CANCELLED


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def codes(apps):
    return [a[0] for a in apps]


def check_v1():
    apps = make_appointments()
    same = apps
    removed = clean_v1(apps)
    assert removed == 3 and codes(same) == ["VM001", "VM004", "VM006"], f"giải pháp 1: xóa {removed}, còn {codes(same)} (phải sửa ngay trên list)"


def check_v2():
    apps = make_appointments()
    same = apps
    removed = clean_v2(apps)
    assert removed == 3 and codes(same) == ["VM001", "VM004", "VM006"], f"giải pháp 2: xóa {removed}, còn {codes(same)} (phải sửa ngay trên list)"
    empty = []
    assert clean_v2(empty) == 0 and empty == []


def check_same():
    rng = random.Random(8)
    for _ in range(200):
        apps = [("VM%03d" % k, "X", rng.choice([WAITING, CANCELLED])) for k in range(rng.randint(0, 30))]
        a, b = apps[:], apps[:]
        assert (clean_v1(a), a) == (clean_v2(b), b), f"hai giải pháp khác kết quả với {[x[2] for x in apps]}"


def check_fast():
    apps = make_big_appointments(200000)
    removed = run_limited(lambda: clean_v2(apps), 1, "giải pháp 2 với 200.000 lịch quá 1 giây")
    assert removed == 66667 and len(apps) == 133333 and apps[0][0] == "VM000001", f"200.000 lịch: xóa {removed}, còn {len(apps)}"


def check_book_cancel():
    apps = make_appointments()
    assert book(apps, "  Đỗ Hà ") == "VM007" and apps[-1] == ("VM007", "Đỗ Hà", WAITING)
    raises("Tên bệnh nhân không được để trống", lambda: book(apps, "   "))
    assert book([], "A") == "VM001"
    clean_v2(apps)
    apps2 = [("VM004", "A", WAITING), ("VM002", "B", WAITING)]
    assert book(apps2, "C") == "VM005", "mã mới lấy số lớn nhất cộng 1"
    cancel(apps, " vm004 ")
    assert apps[1] == ("VM004", "Phạm Dũng", CANCELLED)
    raises("Lịch hẹn đã hủy trước đó", lambda: cancel(apps, "VM004"))
    raises("Không tìm thấy lịch hẹn", lambda: cancel(apps, "VM999"))


def check_benchmark():
    rows = run_limited(lambda: benchmark((200, 400)), 10, "đo quá 10 giây")
    assert [r[0] for r in rows] == [200, 400] and all(len(r) == 3 and r[1] > 0 and r[2] > 0 for r in rows), f"benchmark ra {rows}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "VM002 | Trần Bình | đã hủy", "VM003 | Lê Chi | đã hủy", "Đã dọn 3 lịch hủy. Còn 3 lịch hẹn.",
        "Đã đặt VM007 cho Đỗ Hà.", "Lỗi: Tên bệnh nhân không được để trống", "Đã hủy VM004.",
        "Lỗi: Lịch hẹn đã hủy trước đó", "Lỗi: Không tìm thấy lịch hẹn", "Lựa chọn không hợp lệ.",
        "Đã dọn 1 lịch hủy. Còn 3 lịch hẹn.", "VM007 | Đỗ Hà | chờ khám", "n | giải pháp 1 (ms) | giải pháp 2 (ms)",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 6.", "Đã đóng sổ lịch hẹn. Tạm biệt!",
    ])
    assert "VM004 | Phạm Dũng" not in out.split("Đã dọn 1 lịch hủy")[1], "VM004 đã hủy vẫn còn sau khi dọn"


CHECKS = [
    ("giải pháp 1 trên dữ liệu mẫu, sửa ngay trên list", check_v1),
    ("giải pháp 2 trên dữ liệu mẫu, sửa ngay trên list", check_v2),
    ("hai giải pháp cùng kết quả trên 200 bộ ngẫu nhiên", check_same),
    ("giải pháp 2 với 200.000 lịch", check_fast),
    ("đặt lịch, hủy lịch, dữ liệu sai", check_book_cancel),
    ("hàm benchmark", check_benchmark),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '4',
    '3',
    '1',
    '1',
    'Đỗ Hà',
    '1',
    '   ',
    '2',
    'vm004',
    '2',
    'VM004',
    '2',
    'VM999',
    '3',
    'x',
    '3',
    '2',
    '4',
    '5',
    'x',
    '6',
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
