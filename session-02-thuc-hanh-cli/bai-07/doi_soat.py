"""Nghiệp vụ đối soát giao dịch cuối ngày giữa hệ thống cổng thanh toán VNPAY và sao kê ngân hàng.

Mỗi giao dịch là một list: [mã giao dịch, số tiền (đồng)]. Trong mỗi sổ, mã không trùng nhau;
thứ tự trong sổ là thứ tự ghi nhận, không xếp theo mã.
"""
import timeit

SAMPLE_SYSTEM = [["VP1001", 150000], ["VP1002", 2300000], ["VP1003", 89000], ["VP1005", 560000], ["VP1006", 1200000]]
SAMPLE_BANK = [["VP1006", 1200000], ["VP1001", 150000], ["VP1003", 98000], ["VP1004", 45000], ["VP1002", 2300000]]


def make_books():
    """Có sẵn. Trả về (bản sao sổ hệ thống, bản sao sao kê ngân hàng)."""
    return [tx[:] for tx in SAMPLE_SYSTEM], [tx[:] for tx in SAMPLE_BANK]


def make_big_books(n):
    """Có sẵn. Hai sổ giả lập khoảng n giao dịch, có vài giao dịch thiếu và lệch tiền, thứ tự xáo trộn."""
    system = [[f"VP{(k * 7919) % (n + 17):07d}", 10000 + k] for k in range(n)]
    bank = [[code, amount + (1 if k % 97 == 0 else 0)] for k, (code, amount) in enumerate(system) if k % 50]
    bank.reverse()
    return system, bank


def money(amount):
    """Có sẵn. 2300000 -> "2.300.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def add_tx(book, code_text, amount_text):
    """Thêm giao dịch vào cuối sổ, trả về giao dịch. Lỗi (sổ giữ nguyên):
    "Mã giao dịch phải gồm VP và 4 chữ số trở lên", "Mã <MÃ> đã có trong sổ", "Số tiền phải là số nguyên dương"."""
    raise NotImplementedError


def summary(book):
    """(số giao dịch, tổng tiền)."""
    raise NotImplementedError


def reconcile_v1(system, bank):
    """Giải pháp 1. Trả về bộ (mã chỉ có ở hệ thống, mã chỉ có ở ngân hàng, list bộ (mã, tiền hệ thống, tiền ngân hàng)
    của các giao dịch lệch tiền); ba list đều xếp tăng dần theo mã; không làm đổi system, bank."""
    raise NotImplementedError


def reconcile_v2(system, bank):
    """Giải pháp 2: cùng đầu ra với reconcile_v1, cách làm khác và nhanh hơn rõ rệt khi sổ lớn."""
    raise NotImplementedError


def benchmark(sizes, number=1):
    """Với từng n trong sizes, trên make_big_books(n): đo bằng timeit thời gian một lần reconcile_v1 và reconcile_v2 (ms).
    Trả về list bộ (n, ms giải pháp 1, ms giải pháp 2)."""
    raise NotImplementedError
