"""Nghiệp vụ chốt ca bán hàng của cửa hàng dùng KiotViet.

Mặt hàng là tuple (mã, tên, tồn đầu ca); mã hàng là số nguyên 0..9999 (in đủ 4 chữ số), không trùng.
Giao dịch bán là tuple (mã, số lượng), theo thứ tự thời gian. Không dùng dict, set.
"""
import timeit

MAX_CODE = 9999
CATALOG = [
    (1001, "Mì Hảo Hảo", 50), (1002, "Sữa TH 180ml", 24), (2005, "Nước mắm Nam Ngư", 10),
    (3010, "Gạo ST25 5kg", 5), (4500, "Dầu ăn Neptune 1L", 8),
]
SALES = [(1001, 3), (2005, 10), (3010, 6), (9999, 1), (2005, 1), (1002, 24), (3010, 5)]


def make_catalog():
    """Có sẵn. Trả về bản sao danh mục mẫu."""
    return CATALOG[:]


def make_sales():
    """Có sẵn. Trả về bản sao các giao dịch mẫu."""
    return SALES[:]


def make_big_catalog(n):
    """Có sẵn. n mặt hàng (n <= 10000), mã rải khắp 0..9999, tồn 50."""
    return [(k * 7 % 10000, "Hàng %d" % k, 50) for k in range(n)]


def make_big_sales(m):
    """Có sẵn. m giao dịch giả lập."""
    return [(k * 13 % 10000, 1 + k % 5) for k in range(m)]


def close_slow(catalog, sales):
    """Có sẵn. Bản cũ đang chạy, KHÔNG sửa. Áp lần lượt các giao dịch: mã không có trong danh mục, hoặc số lượng
    lớn hơn tồn hiện tại, thì từ chối (tồn giữ nguyên). Trả về (list tồn cuối ca theo thứ tự danh mục,
    list số thứ tự giao dịch bị từ chối, đánh số từ 1)."""
    stocks = []
    for item in catalog:
        stocks = stocks + [item[2]]
    rejected = []
    for k in range(len(sales)):
        code, quantity = sales[k]
        position = -1
        for i in range(len(catalog)):
            if catalog[i][0] == code:
                position = i
        if position == -1 or quantity > stocks[position]:
            rejected = rejected + [k + 1]
        else:
            stocks[position] = stocks[position] - quantity
    return stocks, rejected


def close_fast(catalog, sales):
    """Cùng kết quả với close_slow; danh mục 10.000 mặt hàng và 200.000 giao dịch trong 1 giây.
    Không gọi close_slow, không dùng dict, set, không làm đổi catalog, sales."""
    raise NotImplementedError


def add_sale(sales, code_text, quantity_text):
    """Ghi giao dịch vào cuối, trả về (mã, số lượng). Lỗi (danh sách giữ nguyên):
    "Mã hàng phải gồm 4 chữ số", "Số lượng phải là số nguyên dương"."""
    raise NotImplementedError


def benchmark(sizes, number=1):
    """Với từng n trong sizes, trên make_big_catalog(n) và make_big_sales(n): đo bằng timeit close_slow và close_fast (ms).
    Trả về list bộ (n, ms bản cũ, ms bản mới)."""
    raise NotImplementedError
