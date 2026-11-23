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
import doanh_so
from doanh_so import make_staff, find_staff, add_sales, remove_staff, ranking, best_and_worst, count_kpi, average_sales


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def codes(rows):
    return [s[0] for s in rows]


def check_find_update():
    staff = make_staff()
    assert find_staff(staff, " nv04 ")[1] == "Phạm Quỳnh" and find_staff(staff, "NV09") is None, "find_staff sai"
    assert add_sales(staff, "nv05", "25")[2] == 85, "NV05 60 triệu cộng 25 phải ra 85"
    raises("Không có nhân viên NV09", lambda: add_sales(staff, "nv09", "10"))
    for bad in ["0", "-5", "2.5", "x"]:
        raises("Doanh số phải là số nguyên dương", lambda: add_sales(staff, "NV01", bad))
    assert staff[0][2] == 120, "doanh số sai không được làm đổi bảng"


def check_remove():
    staff = make_staff()
    assert remove_staff(staff, "nv03")[0] == "NV03" and codes(staff) == ["NV01", "NV02", "NV04", "NV05"], "xóa NV03 sai"
    raises("Không có nhân viên NV03", lambda: remove_staff(staff, "NV03"))


def check_ranking():
    staff = make_staff()
    assert codes(ranking(staff)) == ["NV03", "NV01", "NV02", "NV04", "NV05"], f"xếp hạng ra {codes(ranking(staff))}"
    assert codes(staff) == ["NV01", "NV02", "NV03", "NV04", "NV05"], "xếp hạng làm đổi thứ tự bảng"


def check_best_worst():
    best, worst = best_and_worst(make_staff())
    assert (best[0], worst[0]) == ("NV03", "NV05"), f"cao nhất, thấp nhất ra {(best[0], worst[0])}"
    tie = [["A", "x", 5], ["B", "y", 9], ["C", "z", 9], ["D", "t", 5]]
    best, worst = best_and_worst(tie)
    assert (best[0], worst[0]) == ("B", "A"), f"bằng nhau phải lấy người đứng trước, ra {(best[0], worst[0])}"
    assert best_and_worst([]) == (None, None), "bảng rỗng phải trả (None, None)"


def check_one_pass():
    src = inspect.getsource(doanh_so.best_and_worst)
    assert "sort" not in src and "max(" not in src and "min(" not in src, "best_and_worst phải tự duyệt một lượt, không sắp xếp, không dùng max/min"
    big = [["X", "y", (k * 7919) % 100003] for k in range(200000)]
    best, worst = run_limited(lambda: best_and_worst(big), 2, "200.000 nhân viên quá 2 giây")
    assert best[2] == 100002 and worst[2] == 0


def check_stats():
    staff = make_staff()
    assert count_kpi(staff, "100") == 2 and count_kpi(staff, "95") == 4, "đếm KPI sai (doanh số bằng ngưỡng là đạt)"
    raises("Ngưỡng KPI phải là số nguyên dương", lambda: count_kpi(staff, "ba"))
    assert average_sales(staff) == 104.0 and average_sales([]) is None, "doanh số trung bình sai"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "1. NV03 | Lê Phong | 150 triệu", "3. NV02 | Trần Mai | 95 triệu", "4. NV04 | Phạm Quỳnh | 95 triệu",
        "Đạt KPI 100 triệu: 2/5 nhân viên.", "Đã cập nhật: NV05 | Đỗ Khoa | 85 triệu", "5. NV05 | Đỗ Khoa | 85 triệu",
        "Doanh số trung bình: 109,0 triệu.", "Lỗi: Không có nhân viên NV09", "Lỗi: Doanh số phải là số nguyên dương",
        "Đã xóa NV03 - Lê Phong. Còn 4 nhân viên.", "Cao nhất: NV01 | Nguyễn Hải | 120 triệu", "Thấp nhất: NV05 | Đỗ Khoa | 85 triệu",
        "Lỗi: Ngưỡng KPI phải là số nguyên dương", "Lựa chọn không hợp lệ.", "Đã xóa NV05 - Đỗ Khoa. Còn 0 nhân viên.", "Chưa có nhân viên nào.", "Chưa có nhân viên nào.",
        "Chưa có nhân viên nào.", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã chốt bảng doanh số. Tạm biệt!",
    ])


CHECKS = [
    ("tìm và cộng doanh số, dữ liệu sai", check_find_update),
    ("xóa nhân viên nghỉ việc", check_remove),
    ("xếp hạng không đổi thứ tự bảng", check_ranking),
    ("cao nhất và thấp nhất, bằng nhau, bảng rỗng", check_best_worst),
    ("cao nhất và thấp nhất trong một lượt với 200.000 nhân viên", check_one_pass),
    ("đếm đạt KPI và doanh số trung bình", check_stats),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    '3',
    '4',
    '1',
    '100',
    '2',
    '1',
    'nv05',
    '25',
    '1',
    '1',
    '4',
    '2',
    '2',
    '2',
    'NV09',
    '2',
    '1',
    'NV01',
    '-5',
    '2',
    '2',
    'nv03',
    '3',
    '4',
    '1',
    'ba',
    '4',
    '7',
    '2',
    '2',
    'NV01',
    '2',
    '2',
    'NV02',
    '2',
    '2',
    'NV04',
    '2',
    '2',
    'NV05',
    '3',
    '1',
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
