"""Nghiệp vụ chia đơn chờ giao thành các chuyến xe của Sendo.

Đơn là tuple (mã, giá trị), giá trị là số nguyên đồng; giá trị 0 là đơn chưa thanh toán, không được giao.
Danh sách đơn chờ là list theo thứ tự đặt. Không dùng dict, set, deque.
"""
import timeit

SAMPLE = [
    ("SD01", 250000), ("SD02", 0), ("SD03", 480000), ("SD04", 120000),
    ("SD05", 0), ("SD06", 315000), ("SD07", 99000), ("SD08", 560000),
]
SIZE_ERROR = "Số đơn mỗi chuyến phải là số nguyên dương"


def make_orders():
    """Có sẵn. Trả về bản sao các đơn mẫu."""
    return SAMPLE[:]


def make_big_orders(n):
    """Có sẵn. n đơn giả lập, cứ 5 đơn có 1 đơn chưa thanh toán."""
    return [("SD%06d" % k, 0 if k % 5 == 0 else 10000 + k % 97 * 1000) for k in range(n)]


def money(value):
    """Có sẵn. 1165000 -> "1.165.000đ"."""
    return f"{value:,}".replace(",", ".") + "đ"


def batch_slow(orders, size):
    """Có sẵn. Bản cũ đang chạy, KHÔNG sửa. Lấy lần lượt các đơn đã thanh toán, gom đủ size đơn thành một chuyến;
    chuyến cuối có thể thiếu. Trả về list các chuyến, mỗi chuyến là (list mã đơn, tổng giá trị)."""
    if size < 1:
        raise ValueError(SIZE_ERROR)
    queue = orders[:]
    batches = []
    codes = []
    total = 0
    while len(queue) > 0:
        code, amount = queue[0]
        queue = queue[1:]
        if amount <= 0:
            continue
        codes = codes + [code]
        total = total + amount
        if len(codes) == size:
            batches = batches + [(codes, total)]
            codes = []
            total = 0
    if len(codes) > 0:
        batches = batches + [(codes, total)]
    return batches


def batch_fast(orders, size):
    """Cùng kết quả với batch_slow (kể cả lỗi); 200.000 đơn trong 1 giây.
    Không gọi batch_slow, không làm đổi orders."""
    raise NotImplementedError


def add_order(orders, code, amount_text):
    """Thêm đơn vào cuối, trả về mã đã chuẩn hóa. Mã bỏ khoảng trắng, viết hoa. Lỗi (danh sách giữ nguyên):
    "Mã đơn phải có dạng SD + số", "Mã đơn đã tồn tại", "Giá trị đơn phải là số nguyên không âm"."""
    raise NotImplementedError


def benchmark(sizes, size=50, number=1):
    """Với từng n trong sizes, trên make_big_orders(n), mỗi chuyến size đơn: đo bằng timeit batch_slow và batch_fast (ms).
    Trả về list bộ (n, ms bản cũ, ms bản mới)."""
    raise NotImplementedError
