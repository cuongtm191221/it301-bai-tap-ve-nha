"""Nghiệp vụ kho sách của nhà sách Fahasa chi nhánh Nguyễn Huệ.

Mỗi đầu sách là một list: [mã sách, tên sách, số cuốn tồn, giá bán (đồng)].
"""

SAMPLE_BOOKS = [
    ["FB001", "Đắc Nhân Tâm", 12, 86000],
    ["FB002", "Nhà Giả Kim", 25, 79000],
    ["FB003", "Tuổi Trẻ Đáng Giá Bao Nhiêu", 8, 90000],
    ["FB004", "Cây Cam Ngọt Của Tôi", 25, 108000],
    ["FB005", "Mắt Biếc", 4, 110000],
]


def make_books():
    """Có sẵn. Trả về bản sao kho sách mẫu."""
    return [book[:] for book in SAMPLE_BOOKS]


def money(amount):
    """Có sẵn. 1250000 -> "1.250.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def format_book(book):
    """Có sẵn. "FB001 | Đắc Nhân Tâm | tồn 12 | 86.000đ"."""
    return f"{book[0]} | {book[1]} | tồn {book[2]} | {money(book[3])}"


def parse_positive(text, message):
    """Có sẵn. Đổi chuỗi thành số nguyên dương; sai (rỗng, chữ, số thực, 0, âm) báo ValueError(message)."""
    text = text.strip()
    if not text.isdigit() or int(text) == 0:
        raise ValueError(message)
    return int(text)


def stock_summary(books):
    """Trả về bộ (số đầu sách, tổng số cuốn tồn, tổng giá trị tồn = tổng số cuốn × giá của từng đầu sách)."""
    raise NotImplementedError


def find_book(books, code):
    """Đầu sách có mã code (không phân biệt hoa thường, bỏ khoảng trắng hai đầu) hoặc None."""
    raise NotImplementedError


def add_stock(book, qty_text):
    """Cộng thêm số cuốn vào đầu sách đã có, trả về số tồn mới.
    Số lượng sai báo ValueError("Số lượng phải là số nguyên dương")."""
    raise NotImplementedError


def add_book(books, code, title, price_text, qty_text):
    """Thêm đầu sách mới vào cuối kho, trả về đầu sách mới. Lỗi (kho giữ nguyên):
    "Mã sách không được để trống", "Mã sách <MÃ> đã có trong kho", "Tên sách không được để trống",
    "Giá bán phải là số nguyên dương", "Số lượng phải là số nguyên dương"."""
    raise NotImplementedError


def sell_book(books, code, qty_text):
    """Bán qty cuốn, trả về đầu sách sau khi bán. Lỗi (kho giữ nguyên): "Mã sách <MÃ> không có trong kho",
    "Số lượng phải là số nguyên dương", "Không đủ sách: còn <n> cuốn"."""
    raise NotImplementedError


def top_stock(books, k):
    """List k đầu sách tồn nhiều nhất, nhiều trước; bằng nhau thì giữ thứ tự trong kho; không làm đổi thứ tự của books."""
    raise NotImplementedError
