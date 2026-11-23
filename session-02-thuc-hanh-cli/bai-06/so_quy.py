"""Nghiệp vụ sổ quỹ tiền mặt trong ca của cửa hàng tiện lợi Circle K Lê Lợi.

Mỗi giao dịch là một list: [mã giao dịch, loại "THU" hoặc "CHI", số tiền (đồng)]. Sổ xếp theo thời gian.
"""
import sys
import timeit

OPENING = 2000000          # tiền quỹ đầu ca
SAMPLE_BOOK = [
    ["GD001", "THU", 450000], ["GD002", "CHI", 120000], ["GD003", "THU", 980000],
    ["GD004", "CHI", 300000], ["GD005", "THU", 215000], ["GD006", "CHI", 75000],
]


def make_book():
    """Có sẵn. Trả về bản sao sổ quỹ mẫu."""
    return [tx[:] for tx in SAMPLE_BOOK]


def make_big_book(n):
    """Có sẵn. Sổ quỹ giả lập n giao dịch dùng để đo hiệu năng."""
    return [[f"GD{k + 1:03d}", "THU" if k % 3 else "CHI", 1000 + k % 7 * 500] for k in range(n)]


def money(amount):
    """Có sẵn. 3150000 -> "3.150.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def balance(book):
    """Số dư cuối = OPENING + tổng THU - tổng CHI."""
    raise NotImplementedError


def running_balances(book):
    """List số dư ngay sau từng giao dịch, theo thứ tự sổ. Phải làm trong một lượt duyệt (O(n)),
    không tính lại từ đầu cho mỗi dòng."""
    raise NotImplementedError


def next_code(book):
    """Mã giao dịch tiếp theo: "GD" + số thứ tự (ít nhất 3 chữ số), số thứ tự = số giao dịch hiện có + 1."""
    raise NotImplementedError


def add_tx(book, kind_text, amount_text):
    """Ghi giao dịch vào cuối sổ, trả về giao dịch mới. Lỗi (sổ giữ nguyên):
    "Loại giao dịch phải là THU hoặc CHI", "Số tiền phải là số nguyên dương",
    "Không đủ tiền trong quỹ: số dư <tiền>" (khi CHI lớn hơn số dư)."""
    raise NotImplementedError


def totals(book):
    """(tổng THU, tổng CHI, số dư cuối)."""
    raise NotImplementedError


def top_expenses(book, k):
    """k khoản CHI lớn nhất, lớn trước; bằng nhau giữ thứ tự trong sổ; không làm đổi book."""
    raise NotImplementedError


def benchmark(sizes, number=10):
    """Với từng n trong sizes, trên make_big_book(n): đo bằng timeit thời gian một lần balance (ms)
    và lấy sys.getsizeof của list sổ (byte). Trả về list bộ (n, ms, byte)."""
    raise NotImplementedError
