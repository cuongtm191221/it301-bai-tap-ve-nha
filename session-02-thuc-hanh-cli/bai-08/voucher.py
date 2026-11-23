"""Nghiệp vụ kiểm tra mã voucher phát trùng trong một đợt khuyến mãi của Lazada.

Mỗi voucher là một list: [mã voucher, giá trị (nghìn đồng)]. Voucher được phát từ nhiều máy chủ nên một mã có thể bị phát nhiều lần.
"""
import timeit

SAMPLE_VOUCHERS = [
    ["LZ8K2Q1A", 50], ["LZ3M9P0B", 20], ["LZ8K2Q1A", 50], ["LZ7T4R2C", 100],
    ["LZ3M9P0B", 20], ["LZ1X5W6D", 10], ["LZ8K2Q1A", 50],
]
VALUES = (10, 20, 50, 100)


def make_vouchers():
    """Có sẵn. Trả về bản sao lô voucher mẫu."""
    return [v[:] for v in SAMPLE_VOUCHERS]


def make_big_vouchers(n):
    """Có sẵn. Lô giả lập n voucher, khoảng 1% số mã bị phát trùng."""
    return [[f"LZ{(k * 7919) % (n - n // 100):06d}", 10] for k in range(n)]


def issue(vouchers, code_text, value_text):
    """Phát thêm một voucher vào cuối lô (mã trùng vẫn được phát), trả về voucher. Lỗi (lô giữ nguyên):
    "Mã voucher phải có 8 ký tự chữ hoặc số, bắt đầu bằng LZ", "Giá trị phải là 10, 20, 50 hoặc 100 (nghìn đồng)"."""
    raise NotImplementedError


def total_value(vouchers):
    """Tổng giá trị lô (nghìn đồng)."""
    raise NotImplementedError


def find_duplicates_v1(vouchers):
    """Giải pháp 1. List bộ (mã, số lần xuất hiện) của các mã xuất hiện từ 2 lần, xếp tăng dần theo mã;
    không làm đổi vouchers."""
    raise NotImplementedError


def find_duplicates_v2(vouchers):
    """Giải pháp 2: cùng đầu ra với giải pháp 1, cách làm khác và nhanh hơn rõ rệt khi lô lớn."""
    raise NotImplementedError


def benchmark(sizes, number=1):
    """Với từng n trong sizes, trên make_big_vouchers(n): đo bằng timeit một lần mỗi giải pháp (ms).
    Trả về list bộ (n, ms giải pháp 1, ms giải pháp 2)."""
    raise NotImplementedError
