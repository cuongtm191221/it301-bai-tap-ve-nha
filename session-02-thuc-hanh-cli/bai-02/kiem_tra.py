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


from kho_sach import make_books, stock_summary, find_book, add_stock, add_book, sell_book, top_stock


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def check_summary():
    got = stock_summary(make_books())
    assert got == (5, 74, 6867000), f"kho mẫu ra {got}"
    assert stock_summary([]) == (0, 0, 0), f"kho rỗng ra {stock_summary([])}"


def check_find():
    books = make_books()
    assert find_book(books, " fb003 ")[1] == "Tuổi Trẻ Đáng Giá Bao Nhiêu", 'tìm " fb003 " sai'
    assert find_book(books, "FB999") is None, "mã không có phải trả None"


def check_add_stock():
    books = make_books()
    assert add_stock(books[4], "6") == 10 and books[4][2] == 10, "Mắt Biếc tồn 4, nhập thêm 6 phải ra 10"
    for bad in ["0", "-2", "2.5", "abc", ""]:
        raises("Số lượng phải là số nguyên dương", lambda: add_stock(books[4], bad))
    assert books[4][2] == 10, "số lượng sai không được làm đổi tồn kho"


def check_add_book():
    books = make_books()
    book = add_book(books, " fb006", "Hai Số Phận", "135000", "20")
    assert book == ["FB006", "Hai Số Phận", 20, 135000] and books[-1] is book, f"sách mới là {book}"
    cases = [(("", "A", "1", "1"), "Mã sách không được để trống"), (("fb001", "A", "1", "1"), "Mã sách FB001 đã có trong kho"),
             (("FB007", "  ", "1", "1"), "Tên sách không được để trống"), (("FB007", "A", "-99000", "1"), "Giá bán phải là số nguyên dương"),
             (("FB007", "A", "99000", "0"), "Số lượng phải là số nguyên dương")]
    for args, message in cases:
        books = make_books()
        raises(message, lambda: add_book(books, *args))
        assert books == make_books(), f"{args}: kho bị thay đổi dù dữ liệu sai"


def check_sell():
    books = make_books()
    assert sell_book(books, "fb002", "3")[2] == 22, "Nhà Giả Kim tồn 25, bán 3 phải còn 22"
    raises("Mã sách FB999 không có trong kho", lambda: sell_book(books, "fb999", "1"))
    raises("Không đủ sách: còn 12 cuốn", lambda: sell_book(books, "FB001", "13"))
    raises("Số lượng phải là số nguyên dương", lambda: sell_book(books, "FB001", "0"))
    assert books[0][2] == 12, "bán lỗi không được làm đổi tồn kho"
    assert sell_book(books, "FB005", "4")[2] == 0, "bán hết 4 cuốn Mắt Biếc phải còn 0"


def check_top():
    books = make_books()
    got = [b[0] for b in top_stock(books, 3)]
    assert got == ["FB002", "FB004", "FB001"], f"top 3 ra {got} (bằng nhau giữ thứ tự trong kho)"
    assert [b[0] for b in books] == ["FB001", "FB002", "FB003", "FB004", "FB005"], "top_stock làm đổi thứ tự kho"
    assert len(top_stock(books[:2], 3)) == 2 and top_stock([], 3) == [], "kho ít hơn 3 đầu sách"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "Top 3 sách tồn nhiều nhất:", "1. FB002 | Nhà Giả Kim | tồn 25 | 79.000đ", "3. FB001 | Đắc Nhân Tâm | tồn 12 | 86.000đ",
        "Mã đã có: Mắt Biếc (tồn 4).", "Đã cộng thêm sách. Tồn mới: 10.",
        "Đã thêm sách mới FB006. Kho có 6 đầu sách.", "Đã bán. Nhà Giả Kim còn 22 cuốn.",
        "Lỗi: Mã sách FB999 không có trong kho", "Lỗi: Không đủ sách: còn 12 cuốn", "Lỗi: Số lượng phải là số nguyên dương",
        "Lỗi: Tên sách không được để trống", "Lỗi: Giá bán phải là số nguyên dương",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.",
        "Tổng: 6 đầu sách, 97 cuốn, trị giá 9.990.000đ", "Đã đóng sổ kho. Hẹn gặp lại!",
    ])


CHECKS = [
    ("tổng đầu sách, số cuốn, giá trị tồn", check_summary),
    ("tìm sách theo mã", check_find),
    ("nhập thêm cho sách đã có", check_add_stock),
    ("thêm đầu sách mới và dữ liệu sai", check_add_book),
    ("bán sách và các lỗi khi bán", check_sell),
    ("top sách tồn nhiều nhất, không đổi thứ tự kho", check_top),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '4',
    '2',
    'fb005',
    '6',
    '2',
    'FB006',
    'Hai Số Phận',
    '135000',
    '20',
    '3',
    'FB002',
    '3',
    '3',
    'FB999',
    '1',
    '3',
    'FB001',
    '13',
    '3',
    'FB001',
    '0',
    '2',
    'FB007',
    '',
    '99000',
    '5',
    '2',
    'FB007',
    'Rừng Na Uy',
    '-99000',
    '5',
    'x',
    '1',
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
