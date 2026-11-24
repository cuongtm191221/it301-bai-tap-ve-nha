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
from xem_tiep import ContinueList, make_list, watch, finish, next_show


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def build(*values):
    shows = ContinueList()
    for v in values:
        shows.add_last(v)
    return shows


def check_add():
    shows = ContinueList()
    shows.add_first("B")
    assert shows.head is shows.tail and shows.to_text() == "B -> None", "add_first vào danh sách rỗng phải đặt cả tail"
    shows.add_first("A"); shows.add_last("C")
    assert shows.to_text() == "A -> B -> C -> None" and shows.tail.value == "C" and shows.tail.next is None
    assert shows.count() == 3 and shows.find("B") == 1 and shows.find("X") is None and ContinueList().count() == 0


def check_remove():
    shows = build("A", "B", "C")
    assert shows.remove("X") is False and ContinueList().remove("A") is False
    assert shows.remove("C") and shows.tail.value == "B", "xóa tail thì tail lùi về node trước"
    shows.add_last("D")
    assert shows.to_text() == "A -> B -> D -> None"
    assert shows.remove("A") and shows.remove("D") and shows.head is shows.tail and shows.head.value == "B"
    assert shows.remove("B") and shows.head is None and shows.tail is None, "xóa node duy nhất"
    shows.add_last("E")
    assert shows.to_text() == "E -> None"


def check_watch():
    shows = make_list()
    assert watch(shows, " Thời sự 19h ") is None and shows.to_text() == "Thời sự 19h -> Cà phê sáng -> V-League vòng 5 -> Phim tối thứ Bảy -> None"
    assert watch(shows, "Thời sự 19h") is None and shows.count() == 4, "mở lại chương trình đang ở đầu không tạo bản trùng"
    assert watch(shows, "Phim tối thứ Bảy") is None and shows.tail.value == "V-League vòng 5", "chuyển chương trình ở tail lên đầu phải cập nhật tail"
    assert watch(shows, "A") is None and watch(shows, "B") == "V-League vòng 5" and shows.count() == 5
    assert shows.to_text() == "B -> A -> Phim tối thứ Bảy -> Thời sự 19h -> Cà phê sáng -> None" and shows.tail.value == "Cà phê sáng"


def check_finish_errors():
    shows = make_list()
    assert finish(shows, "Phim tối thứ Bảy") == "Phim tối thứ Bảy" and shows.tail.value == "Thời sự 19h"
    raises("Không có Ca nhạc trong danh sách xem tiếp", lambda: finish(shows, "Ca nhạc"))
    for bad in ["", "   ", "x" * 41]:
        raises("Tên chương trình phải có từ 1 đến 40 ký tự", lambda: watch(shows, bad))
    assert next_show(shows) == "Cà phê sáng" and next_show(ContinueList()) is None


def check_no_list():
    for name in ("add_first", "add_last", "count", "find", "remove"):
        body = inspect.getsource(getattr(ContinueList, name)).split('"""', 2)[-1]
        assert "[" not in body and "list(" not in body and ".append(" not in body, f"{name} không được dùng list Python"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Cà phê sáng -> V-League vòng 5 -> Thời sự 19h -> Phim tối thứ Bảy -> None", "Có 4 chương trình", "Đang xem: Thời sự 19h.",
        "Đang xem: Đố vui cuối tuần.", "Đang xem: Hoạt hình cho bé.", "Đã bỏ chương trình cũ nhất: Phim tối thứ Bảy.",
        "Hoạt hình cho bé -> Đố vui cuối tuần -> Thời sự 19h -> Cà phê sáng -> V-League vòng 5 -> None", "Có 5 chương trình",
        "Đang xem: V-League vòng 5.", "Đã xem xong Cà phê sáng.", "Lỗi: Không có Ca nhạc trong danh sách xem tiếp",
        "Lỗi: Tên chương trình phải có từ 1 đến 40 ký tự", "V-League vòng 5 -> Hoạt hình cho bé -> Đố vui cuối tuần -> Thời sự 19h -> None",
        "Tiếp tục xem: V-League vòng 5", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Hẹn gặp lại trên FPT Play!",
    ])


CHECKS = [
    ("add_first, add_last, count, find", check_add),
    ("remove trúng head, tail, node duy nhất, rồi thêm lại", check_remove),
    ("mở chương trình: đưa lên đầu, không trùng, giới hạn 5", check_watch),
    ("xem xong, xem tiếp, dữ liệu sai", check_finish_errors),
    ("không dùng list Python trong các phương thức", check_no_list),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    'Thời sự 19h',
    '2',
    'Đố vui cuối tuần',
    '2',
    'Hoạt hình cho bé',
    '1',
    '2',
    'V-League vòng 5',
    '4',
    'Cà phê sáng',
    '4',
    'Ca nhạc',
    '2',
    '   ',
    '1',
    '3',
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
