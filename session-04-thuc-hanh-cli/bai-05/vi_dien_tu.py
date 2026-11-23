"""Nghiệp vụ lịch sử giao dịch ví ZaloPay của một người dùng.

Mỗi giao dịch là một list: [mã giao dịch, loại "NAP" hoặc "CHI", số tiền (đồng)]. Lịch sử xếp theo thời gian.
Số dư = tổng NAP - tổng CHI. Có hai cách cài: ĐỆ QUY (theo chỉ số, không cắt list) và VÒNG LẶP.
"""
import timeit

RECURSION_SAFE = 500           # lịch sử dài hơn mức này thì không dùng bản đệ quy
SAMPLE_TXS = [
    ["ZP001", "NAP", 500000], ["ZP002", "CHI", 45000], ["ZP003", "CHI", 120000],
    ["ZP004", "NAP", 200000], ["ZP005", "CHI", 89000], ["ZP006", "CHI", 35000],
]


def make_txs():
    """Có sẵn. Trả về bản sao lịch sử mẫu."""
    return [t[:] for t in SAMPLE_TXS]


def make_big_txs(n):
    """Có sẵn. Lịch sử giả lập n giao dịch."""
    return [[f"ZP{k}", "NAP" if k % 3 == 0 else "CHI", 1000 + k % 9 * 1000] for k in range(n)]


def money(amount):
    """Có sẵn. 411000 -> "411.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def net_rec(txs, i=0):
    """Số dư của txs[i:]. Đệ quy theo chỉ số i (không cắt list), không vòng lặp."""
    raise NotImplementedError


def net_loop(txs):
    """Số dư, viết bằng vòng lặp."""
    raise NotImplementedError


def balance(txs):
    """Trả về bộ (số dư, "đệ quy" hoặc "vòng lặp"): dùng net_rec khi len(txs) <= RECURSION_SAFE, ngược lại dùng net_loop."""
    raise NotImplementedError


def largest_spend(txs, i=0):
    """Khoản CHI lớn nhất trong txs[i:] (giao dịch, list) hoặc None; bằng nhau lấy khoản đứng trước.
    Đệ quy theo chỉ số, không vòng lặp, không max()."""
    raise NotImplementedError


def add_tx(txs, kind_text, amount_text):
    """Ghi giao dịch vào cuối lịch sử, mã "ZP" + số thứ tự 3 chữ số; trả về giao dịch. Lỗi (lịch sử giữ nguyên):
    "Loại phải là NAP hoặc CHI", "Số tiền phải là số nguyên dương", "Số dư không đủ: còn <tiền>"."""
    raise NotImplementedError


def benchmark(sizes, number=20):
    """Với từng n trong sizes, trên make_big_txs(n): đo bằng timeit một lần net_rec và net_loop (ms).
    Trả về list bộ (n, ms đệ quy, ms vòng lặp)."""
    raise NotImplementedError


def recursion_fails(n):
    """True nếu net_rec trên make_big_txs(n) gặp RecursionError, False nếu chạy được."""
    raise NotImplementedError
