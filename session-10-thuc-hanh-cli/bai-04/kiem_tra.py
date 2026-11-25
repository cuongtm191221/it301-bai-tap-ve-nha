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
from collections import deque
from doc_bao import Reader, visit, go_back, go_forward, history


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_visit():
    r = Reader()
    assert visit(r, " a201 ") == "A201" and visit(r, "A202") == "A202" and list(r.back) == ["A100", "A201"]
    raises("Bạn đang đọc bài A202", lambda: visit(r, "a202"))
    for bad in ["B12", "A12", "A1234", "", "Aabc"]:
        raises("Mã bài phải có dạng A và 3 chữ số", lambda: visit(r, bad))
    assert r.current == "A202" and len(r.back) == 2


def check_back_forward():
    r = Reader()
    raises("Không có bài để quay lại", lambda: go_back(r))
    raises("Không có bài để tiến tới", lambda: go_forward(r))
    visit(r, "A201"); visit(r, "A202")
    assert go_back(r) == "A201" and go_back(r) == "A100" and r.forward == ["A202", "A201"]
    raises("Không có bài để quay lại", lambda: go_back(r))
    assert go_forward(r) == "A201" and r.forward == ["A202"]
    visit(r, "A305")
    assert r.forward == [] and list(r.back) == ["A100", "A201"], "mở bài mới phải xóa forward"
    raises("Không có bài để tiến tới", lambda: go_forward(r))


def check_limit():
    r = Reader()
    for k in range(1, 9):
        visit(r, "A%03d" % (200 + k))
    assert type(r.back) is deque and r.back.maxlen == 5 and list(r.back) == ["A203", "A204", "A205", "A206", "A207"], f"back ra {list(r.back)}"
    for want in ["A207", "A206", "A205", "A204", "A203"]:
        assert go_back(r) == want
    raises("Không có bài để quay lại", lambda: go_back(r))
    assert r.current == "A203" and r.forward == ["A208", "A207", "A206", "A205", "A204"]


def check_history():
    r = Reader()
    for code in ["A201", "A202", "A203"]:
        visit(r, code)
    go_back(r); go_back(r)
    assert history(r, "back") == ["A100"] and history(r, "forward") == ["A202", "A203"]
    assert list(r.back) == ["A100"] and r.forward == ["A203", "A202"], "history không được làm đổi back, forward"
    assert history(Reader(), "back") == [] and history(Reader(), "forward") == []


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Lỗi: Không có bài để quay lại", "Đang đọc: A201", "Đang đọc: A202", "Lỗi: Bạn đang đọc bài A202",
        "Lỗi: Mã bài phải có dạng A và 3 chữ số", "Đang đọc: A201", "Đang đọc: A100", "A201, A202", "Đang đọc: A201",
        "Đang đọc: A305", "Lỗi: Không có bài để tiến tới", "A201, A100", "Đang đọc: A309", "A308, A307, A306, A305, A201",
        "(trống)", "Lựa chọn không hợp lệ.", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 6.", "Cảm ơn bạn đã đọc VnExpress!",
    ])


CHECKS = [
    ("mở bài, mở lại bài đang đọc, mã sai", check_visit),
    ("quay lại, tiến tới, mở bài mới xóa forward", check_back_forward),
    ("giới hạn 5 bài quay lại bằng deque(maxlen=5)", check_limit),
    ("xem lịch sử không làm đổi dữ liệu", check_history),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '3',
    '2',
    'a201',
    '2',
    'A202',
    '2',
    'A202',
    '2',
    'B12',
    '3',
    '3',
    '5',
    '2',
    '4',
    '2',
    'A305',
    '4',
    '5',
    '1',
    '2',
    'A306',
    '2',
    'A307',
    '2',
    'A308',
    '2',
    'A309',
    '5',
    '1',
    '5',
    '2',
    '5',
    'x',
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
