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
import mau_in
from mau_in import LinkedStack, check_template, is_balanced, add_template, make_templates


def raises(kind, message, task):
    try:
        task()
    except kind as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo {kind.__name__}("{message}")')


def check_stack():
    s = LinkedStack()
    raises(IndexError, "ngăn xếp rỗng", s.pop)
    raises(IndexError, "ngăn xếp rỗng", s.peek)
    for v in "ABC":
        s.push(v)
    assert s.size() == 3 and s.peek() == "C" and s.pop() == "C" and s.pop() == "B" and s.size() == 1
    assert s.pop() == "A" and s.is_empty() and s.head is None
    for name in ("push", "pop", "peek", "is_empty", "size"):
        body = inspect.getsource(getattr(LinkedStack, name)).split('"""', 2)[-1]
        assert "while" not in body and "for " not in body and "[" not in body, f"{name} không được duyệt, không dùng list"


def check_messages():
    cases = {
        "Khách: {ten_khach} - Đơn [ma_don]": None,
        "Tổng: {tong_tien": "Vị trí 7: dấu '{' chưa được đóng",
        "Giảm (10%]": "Vị trí 10: dấu ']' không khớp với '(' ở vị trí 6",
        "Phí ship)": "Vị trí 9: dấu ')' không có dấu mở",
        '"(in nguyên văn" [ma_km]': None,
        'Lời cảm ơn "hẹn gặp lại': "Vị trí 12: dấu nháy kép chưa được đóng",
        "{a} (b": "Vị trí 5: dấu '(' chưa được đóng",
        "([)]": "Vị trí 3: dấu ')' không khớp với '[' ở vị trí 2",
        "{[(": "Vị trí 3: dấu '(' chưa được đóng",
        "a)(": "Vị trí 2: dấu ')' không có dấu mở",
        '"{" "}"': None,
        "": None,
    }
    for text, want in cases.items():
        got = check_template(text)
        assert got == want, f"check_template({text!r}) ra {got!r}, cần {want!r}"
        assert is_balanced(text) == (want is None)


def check_no_list_stack():
    body = inspect.getsource(mau_in.check_template).split('"""', 2)[-1]
    assert "LinkedStack()" in body and "append(" not in body and "= []" not in body, "check_template phải dùng LinkedStack, không dùng list làm ngăn xếp"


def check_add():
    templates = make_templates()
    assert add_template(templates, "  Mã: {ma_don} (ngày [ngay_dat])  ") == "Mã: {ma_don} (ngày [ngay_dat])" and len(templates) == 4
    raises(ValueError, "Vị trí 6: dấu '{' chưa được đóng", lambda: add_template(templates, "Hạn: {han"))
    for bad in ["", "   ", "x" * 201]:
        raises(ValueError, "Mẫu in phải có từ 1 đến 200 ký tự", lambda: add_template(templates, bad))
    assert len(templates) == 4


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "1. Khách: {ten_khach} - Đơn [ma_don]", "3. Ghi chú: \"(không xuất hóa đơn đỏ\" {ghi_chu}", "Vị trí 7: dấu '{' chưa được đóng",
        "Vị trí 10: dấu ']' không khớp với '(' ở vị trí 6", "Không hợp lệ", "Hợp lệ", "Vị trí 12: dấu nháy kép chưa được đóng",
        "Lựa chọn không hợp lệ.", "Đã thêm mẫu 4.", "Lỗi: Vị trí 6: dấu '{' chưa được đóng", "Lỗi: Mẫu in phải có từ 1 đến 200 ký tự",
        "4. Mã: {ma_don} (ngày [ngay_dat])", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 4.", "Đã lưu các mẫu in. Tạm biệt!",
    ])


CHECKS = [
    ("LinkedStack: push, pop, peek, rỗng; không duyệt", check_stack),
    ("thông báo lỗi đầu tiên, vị trí, nháy kép, is_balanced", check_messages),
    ("check_template dùng LinkedStack, không dùng list làm ngăn xếp", check_no_list_stack),
    ("thêm mẫu, mẫu lỗi, dữ liệu sai", check_add),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '2',
    'Tổng: {tong_tien',
    '3',
    '2',
    'Giảm (10%]',
    '3',
    '1',
    'Phí ship)',
    '3',
    '2',
    '"(in nguyên văn" [ma_km]',
    '3',
    '2',
    'Lời cảm ơn "hẹn gặp lại',
    '3',
    'x',
    '2',
    'Mã: {ma_don} (ngày [ngay_dat])',
    '2',
    'Hạn: {han',
    '2',
    '   ',
    '1',
    'x',
    '4',
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
