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
import don_thuoc
from don_thuoc import make_orders, add_order, cancel_order, compact, drop_cancelled, merge_duplicates, reverse_in_place


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def codes(rows):
    return [o[0] for o in rows]


def no_list_shifting(func):
    body = inspect.getsource(func).split('"""', 2)[-1]
    for banned in (".pop(", ".remove(", ".insert(", "reverse(", "[::-1]", "reversed("):
        assert banned not in body, f"{func.__name__} không được dùng {banned}"


def check_compact():
    orders = make_orders()
    same = orders
    kept, assigns = compact(orders)
    assert orders is same and len(orders) == 9, "compact phải sửa tại chỗ, không đổi độ dài"
    assert kept == 7 and codes(orders[:7]) == ["PC1001", "PC1003", "PC1003", "PC1005", "PC1005", "PC1005", "PC1006"], f"phần đơn MOI ra {codes(orders[:kept])}"
    assert sorted(codes(orders[7:])) == ["PC1002", "PC1004"], "hai đơn HUY phải ở cuối"
    assert compact([]) == (0, 0)
    no_list_shifting(don_thuoc.compact)


def check_drop():
    orders = make_orders()
    assert drop_cancelled(orders) == 2 and len(orders) == 7 and all(o[1] == "MOI" for o in orders)
    assert drop_cancelled(orders) == 0
    no_list_shifting(don_thuoc.drop_cancelled)


def check_merge():
    orders = make_orders()
    assert merge_duplicates(orders) == 3, "phải gộp 3 đơn trùng liền nhau"
    assert codes(orders) == ["PC1001", "PC1002", "PC1003", "PC1004", "PC1005", "PC1006"], f"sau khi gộp ra {codes(orders)}"
    gap = [["A", "MOI", 1], ["B", "MOI", 1], ["A", "MOI", 1]]
    assert merge_duplicates(gap) == 0 and codes(gap) == ["A", "B", "A"], "chỉ gộp đơn trùng LIỀN NHAU"
    assert merge_duplicates([]) == 0
    no_list_shifting(don_thuoc.merge_duplicates)


def check_reverse():
    orders = make_orders()
    first = orders[0]
    reverse_in_place(orders)
    assert codes(orders) == codes(make_orders())[::-1] and orders[-1] is first, "đảo ngược tại chỗ sai"
    one = [["A", "MOI", 1]]
    reverse_in_place(one)
    assert one == [["A", "MOI", 1]]
    no_list_shifting(don_thuoc.reverse_in_place)


def check_add_cancel():
    orders = make_orders()
    assert add_order(orders, " pc1007", "75000") == ["PC1007", "MOI", 75000]
    assert cancel_order(orders, "pc1005") == 3, "phải hủy cả 3 đơn PC1005 đang chờ"
    raises("Không có đơn PC1002 đang chờ", lambda: cancel_order(orders, "PC1002"))
    raises("Mã đơn phải có dạng PC và 4 chữ số", lambda: add_order(orders, "PC12", "1000"))
    raises("Số tiền phải là số nguyên dương", lambda: add_order(orders, "PC1008", "0"))


def check_big():
    def job():
        orders = [[f"PC{k % 10000:04d}", "HUY" if k % 2 else "MOI", 1000] for k in range(200000)]
        removed = drop_cancelled(orders)
        orders2 = [[f"PC{k // 3:04d}", "MOI", 1000] for k in range(30000)]
        return removed, len(orders), merge_duplicates(orders2)
    got = run_limited(job, 2, "200.000 đơn quá 2 giây: không được xóa từng phần tử trong vòng lặp")
    assert got == (100000, 100000, 20000), f"200.000 đơn ra {got}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Đã gộp 3 đơn trùng. Còn 6 đơn.", "Đã hủy 1 đơn.", "Đã bỏ 3 đơn hủy. Còn 3 đơn.", "3. PC1006 | MOI | 310.000đ",
        "Lỗi: Không có đơn PC1002 đang chờ", "Lỗi: Mã đơn phải có dạng PC và 4 chữ số", "Lỗi: Số tiền phải là số nguyên dương",
        "Đã đảo thứ tự danh sách.", "1. PC1006 | MOI | 310.000đ", "Lựa chọn không hợp lệ.",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã chốt danh sách đơn. Tạm biệt!",
    ])


CHECKS = [
    ("dồn đơn hủy về cuối, giữ thứ tự đơn còn hiệu lực", check_compact),
    ("bỏ đơn hủy tại chỗ", check_drop),
    ("gộp đơn trùng liền nhau", check_merge),
    ("đảo ngược bằng hai chỉ số", check_reverse),
    ("nhận, hủy đơn và dữ liệu sai", check_add_cancel),
    ("200.000 đơn", check_big),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '4',
    '2',
    '3',
    'pc1005',
    '4',
    '1',
    '1',
    '3',
    'PC1002',
    '2',
    'PC12',
    '1000',
    '2',
    'PC1007',
    '0',
    '4',
    '3',
    '1',
    '4',
    '9',
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
