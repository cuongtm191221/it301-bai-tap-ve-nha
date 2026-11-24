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


from ghe_cgv import make_hall, make_sample_hall, parse_seat, book, cancel, free_count, find_block


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_make():
    hall = make_hall(3, 4)
    assert hall == [["."] * 4] * 3, "phòng 3 x 4 phải toàn ghế trống"
    hall[0][1] = "X"
    assert hall[1][1] == "." and hall[2][1] == ".", "đặt ghế hàng A làm đổi cả hàng khác: các hàng đang là cùng một list"
    assert hall[0] is not hall[1], "mỗi hàng phải là một list riêng"
    for bad in [(0, 5), (27, 5), (5, 0), (5, 31), (2.0, 5), ("5", 5)]:
        raises("Kích thước phòng không hợp lệ", lambda: make_hall(*bad))


def check_parse():
    hall = make_hall(5, 10)
    assert parse_seat(hall, " c5 ") == (2, 4) and parse_seat(hall, "A10") == (0, 9) and parse_seat(hall, "E1") == (4, 0)
    for bad in ["5B", "C", "CC5", "C-1", ""]:
        raises("Ghế không hợp lệ", lambda: parse_seat(hall, bad))
    for bad in ["F1", "A11", "A0"]:
        raises("Ghế ngoài phòng chiếu", lambda: parse_seat(hall, bad))


def check_book_cancel():
    hall = make_sample_hall()
    assert free_count(hall) == (44, 50), f"phòng mẫu ra {free_count(hall)}"
    assert book(hall, "a5") == "A5" and hall[0][4] == "X"
    raises("Ghế A5 đã có người đặt", lambda: book(hall, "A5"))
    assert cancel(hall, "c6") == "C6" and hall[2][5] == "."
    raises("Ghế C6 chưa được đặt", lambda: cancel(hall, "C6"))
    assert free_count(hall) == (44, 50)


def check_block():
    hall = make_sample_hall()
    assert find_block(hall, 2) == ("A1", "A2") and find_block(hall, 3) == ("A5", "A7"), "tìm khối ghế sai"
    assert find_block(hall, 10) == ("B1", "B10") and find_block(hall, 11) is None
    book(hall, "A6")
    assert find_block(hall, 4) == ("A7", "A10"), "khối 4 ghế phải là A7 đến A10"
    assert find_block(make_hall(1, 1), 1) == ("A1", "A1")


def check_big():
    hall = make_hall(26, 30)
    for r in range(26):
        for c in range(0, 30, 2):
            hall[r][c] = "X"
    got = run_limited(lambda: [find_block(hall, 2) for _ in range(2000)][-1], 2, "tìm khối ghế quá chậm")
    assert got is None


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "A  . . X X . . . . . .", "Còn trống 44/50 ghế", "Gợi ý: A5 đến A7", "Đã đặt ghế A5.", "Lỗi: Ghế A5 đã có người đặt",
        "Đã hủy ghế C6.", "Lỗi: Ghế C6 chưa được đặt", "Lỗi: Ghế ngoài phòng chiếu", "Lỗi: Ghế ngoài phòng chiếu", "Lỗi: Ghế không hợp lệ",
        "Gợi ý: B1 đến B10", "Lỗi: Số người phải là số nguyên từ 1 đến 10", "A  . . X X X . . . . .", "Còn trống 44/50 ghế",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Chúc quý khách xem phim vui vẻ!",
    ])


CHECKS = [
    ("tạo phòng: mỗi hàng một list riêng", check_make),
    ("đọc tên ghế", check_parse),
    ("đặt, hủy ghế và đếm ghế trống", check_book_cancel),
    ("tìm k ghế trống liền nhau", check_block),
    ("phòng 26 x 30", check_big),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '4',
    '3',
    '2',
    'a5',
    '2',
    'A5',
    '3',
    'c6',
    '3',
    'C6',
    '2',
    'F1',
    '2',
    'B11',
    '2',
    '5B',
    '4',
    '10',
    '4',
    '11',
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
