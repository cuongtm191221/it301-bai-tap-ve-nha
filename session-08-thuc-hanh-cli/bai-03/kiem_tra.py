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
from dat_coc import PreorderList, make_list, deposit, prioritize, cancel_at, page


def raises(kind, message, task):
    try:
        task()
    except kind as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo {kind.__name__}("{message}")')


def build(*values):
    customers = PreorderList()
    for v in values:
        customers.add_last(v)
    return customers


def check_get():
    customers = build("A", "B", "C")
    assert [customers.get(i) for i in range(3)] == ["A", "B", "C"] and customers.count() == 3
    for bad in (3, 10, -1):
        raises(IndexError, "Chỉ số ngoài phạm vi", lambda: customers.get(bad))
    raises(IndexError, "Chỉ số ngoài phạm vi", lambda: PreorderList().get(0))


def check_insert():
    customers = PreorderList()
    customers.insert_at(0, "B")
    assert customers.head is customers.tail and customers.to_text() == "B -> None", "chèn vào danh sách rỗng"
    customers.insert_at(0, "A"); customers.insert_at(2, "D"); customers.insert_at(2, "C")
    assert customers.to_text() == "A -> B -> C -> D -> None" and customers.tail.value == "D", "chèn ở đầu, cuối, giữa"
    customers.add_last("E")
    assert customers.to_text().endswith("D -> E -> None"), "chèn ở cuối phải cập nhật tail"
    for bad in (6, -1):
        raises(IndexError, "Chỉ số ngoài phạm vi", lambda: customers.insert_at(bad, "X"))
    assert customers.count() == 5


def check_remove():
    customers = build("A", "B", "C", "D")
    assert customers.remove_at(3) == "D" and customers.tail.value == "C", "xóa tail phải lùi tail"
    customers.add_last("E")
    assert customers.remove_at(1) == "B" and customers.remove_at(0) == "A" and customers.to_text() == "C -> E -> None"
    for bad in (2, -1):
        raises(IndexError, "Chỉ số ngoài phạm vi", lambda: customers.remove_at(bad))
    assert customers.remove_at(1) == "E" and customers.remove_at(0) == "C" and customers.head is None and customers.tail is None
    raises(IndexError, "Chỉ số ngoài phạm vi", lambda: customers.remove_at(0))


def check_business():
    customers = make_list()
    assert deposit(customers, " kh106 ") == ("KH106", 6)
    raises(ValueError, "Khách KH102 đã có trong danh sách", lambda: deposit(customers, "KH102"))
    for bad in ["K12", "KH12", "KH1234", "KHabc", ""]:
        raises(ValueError, "Mã khách phải có dạng KH và 3 chữ số", lambda: deposit(customers, bad))
    assert prioritize(customers, "KH200", "1") == ("KH200", 1) and prioritize(customers, "KH201", "8") == ("KH201", 8)
    assert customers.tail.value == "KH201"
    raises(ValueError, "Vị trí phải từ 1 đến 9", lambda: prioritize(customers, "KH202", "10"))
    raises(ValueError, "Vị trí phải là số nguyên", lambda: prioritize(customers, "KH203", "a"))
    raises(ValueError, "Khách KH101 đã có trong danh sách", lambda: prioritize(customers, "KH101", "a"))
    assert cancel_at(customers, "8") == ("KH201", 8) and customers.tail.value == "KH106"
    raises(ValueError, "Vị trí phải từ 1 đến 7", lambda: cancel_at(customers, "0"))
    raises(ValueError, "Vị trí phải là số nguyên", lambda: cancel_at(customers, "1.5"))
    assert page(customers, "6") == [(6, "KH105"), (7, "KH106")] and page(customers, "1") == [(1, "KH200"), (2, "KH101"), (3, "KH102")]
    raises(ValueError, "Danh sách đặt cọc đang trống", lambda: cancel_at(PreorderList(), "1"))


def check_no_list():
    for name in ("count", "add_last", "get", "insert_at", "remove_at"):
        body = inspect.getsource(getattr(PreorderList, name)).split('"""', 2)[-1]
        assert "[" not in body and "list(" not in body and ".append(" not in body, f"{name} không được dùng list Python"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "KH101 -> KH102 -> KH103 -> KH104 -> KH105 -> None", "Tổng: 5 khách", "4. KH104", "5. KH105", "Lựa chọn không hợp lệ.",
        "Đã nhận cọc của KH106, vị trí 6.", "Lỗi: Khách KH102 đã có trong danh sách", "Lỗi: Mã khách phải có dạng KH và 3 chữ số",
        "Đã chèn KH200 vào vị trí 1.", "Đã chèn KH201 vào vị trí 8.", "Lỗi: Vị trí phải từ 1 đến 9", "Lỗi: Vị trí phải là số nguyên",
        "Đã hủy suất của KH201 (vị trí 8).", "Đã nhận cọc của KH107, vị trí 8.", "Lỗi: Vị trí phải từ 1 đến 8",
        "KH200 -> KH101 -> KH102 -> KH103 -> KH104 -> KH105 -> KH106 -> KH107 -> None", "Tổng: 8 khách",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Đã lưu danh sách đặt cọc. Tạm biệt!",
    ])


CHECKS = [
    ("get theo chỉ số, chỉ số sai", check_get),
    ("insert_at ở đầu, giữa, cuối, danh sách rỗng", check_insert),
    ("remove_at ở đầu, giữa, tail, node duy nhất", check_remove),
    ("đặt cọc, chèn ưu tiên, hủy, xem trang, dữ liệu sai", check_business),
    ("không dùng list Python trong các phương thức", check_no_list),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '1',
    '1',
    '2',
    '4',
    '1',
    'x',
    '2',
    'kh106',
    '2',
    'KH102',
    '2',
    'K12',
    '3',
    'KH200',
    '1',
    '3',
    'KH201',
    '8',
    '3',
    'KH202',
    '10',
    '3',
    'KH203',
    'a',
    '4',
    '8',
    '2',
    'KH107',
    '4',
    '0',
    '1',
    '1',
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
