"""Nghiệp vụ sao kê tài khoản trên ứng dụng MB Bank.

Lịch sử giao dịch là list, cũ trước mới sau; mỗi giao dịch là [mã, nội dung, số tiền] (số tiền âm là tiền ra).
Sao kê hiển thị mới nhất trước.
"""
import sys
import timeit

SAMPLE = [
    ["MB001", "Lương tháng 10", 15000000], ["MB002", "Tiền điện", -650000], ["MB003", "Chuyển khoản cho mẹ", -2000000],
    ["MB004", "Hoàn tiền Shopee", 120000], ["MB005", "Tiền nhà", -4500000],
]


def make_txs():
    """Có sẵn. Trả về bản sao lịch sử mẫu."""
    return [t[:] for t in SAMPLE]


def make_big_txs(n):
    """Có sẵn. Lịch sử giả lập n giao dịch."""
    return [[f"MB{k + 1:06d}", "Giao dịch", (k % 7 - 3) * 10000] for k in range(n)]


def money(amount):
    """Có sẵn. -650000 -> "-650.000đ", 120000 -> "+120.000đ"."""
    return ("+" if amount > 0 else "-") + f"{abs(amount):,}".replace(",", ".") + "đ"


def statement_slow(txs):
    """Có sẵn. Bản cũ: list mọi giao dịch, mới nhất trước, dựng bằng insert(0, ...)."""
    result = []
    for tx in txs:
        result.insert(0, tx)
    return result


def add_tx(txs, content, amount_text):
    """Ghi giao dịch vào cuối, mã "MB" + số thứ tự 3 chữ số (ít nhất). Lỗi (lịch sử giữ nguyên):
    "Nội dung không được để trống", "Số tiền phải là số nguyên khác 0 (âm là tiền ra)"."""
    raise NotImplementedError


def latest_first(txs, k):
    """List k giao dịch gần nhất, mới nhất trước (k lớn hơn số giao dịch thì trả tất cả). Đọc theo chỉ số từ cuối, dùng append;
    không dùng insert, reverse, [::-1], reversed. Không làm đổi txs."""
    raise NotImplementedError


def capacity_steps(n):
    """Thêm lần lượt n phần tử (số 0) vào một list rỗng; trả về list bộ (số phần tử, sys.getsizeof) tại lúc bắt đầu
    và mỗi khi getsizeof thay đổi (tức là list vừa chuyển sang vùng nhớ lớn hơn)."""
    raise NotImplementedError


def benchmark(sizes, number=3):
    """Với từng n trong sizes, trên make_big_txs(n): đo bằng timeit một lần statement_slow và một lần latest_first(txs, n) (ms).
    Trả về list bộ (n, ms bản cũ, ms bản mới)."""
    raise NotImplementedError
