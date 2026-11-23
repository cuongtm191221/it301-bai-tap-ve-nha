"""Nghiệp vụ sổ đơn trong ca và báo cáo cuối ca của cửa hàng The Coffee House Hồ Con Rùa.

Mỗi đơn là một list: [mã đơn, tên món, số ly]. Sổ xếp theo thời gian, cũ trước mới sau.
"""
import timeit

DRINKS = ["Cà phê sữa đá", "Trà đào cam sả", "Bạc xỉu", "Trà sữa oolong", "Cold brew"]
SAMPLE_ORDERS = [
    ["TCH0001", "Bạc xỉu", 2], ["TCH0002", "Trà đào cam sả", 1], ["TCH0003", "Cà phê sữa đá", 3],
    ["TCH0004", "Bạc xỉu", 1], ["TCH0005", "Trà đào cam sả", 3], ["TCH0006", "Cold brew", 1],
]


def make_orders():
    """Có sẵn. Trả về bản sao sổ đơn mẫu."""
    return [o[:] for o in SAMPLE_ORDERS]


def make_big_orders(n):
    """Có sẵn. Sổ giả lập n đơn với 30 món khác nhau."""
    return [[f"TCH{k + 1:04d}", f"Món {(k * 7) % 30}", 1 + k % 4] for k in range(n)]


def report_slow(orders, top):
    """Có sẵn. Bản cũ đang chạy, KHÔNG sửa. Trả về bộ (tổng số ly, số món khác nhau, món bán nhiều ly nhất
    (bằng nhau lấy món xuất hiện trước trong sổ; sổ rỗng là None), số ly của món đó, list mã của top đơn gần nhất, mới nhất trước)."""
    drinks = []
    for order in orders:
        if order[1] not in drinks:
            drinks = drinks + [order[1]]
    best, best_cups = None, 0
    for drink in drinks:
        cups = 0
        for order in orders:
            if order[1] == drink:
                cups += order[2]
        if cups > best_cups:
            best, best_cups = drink, cups
    total = 0
    for order in orders:
        total += order[2]
    recent = []
    for order in orders:
        recent.insert(0, order[0])
    while len(recent) > top:
        recent.pop()
    return total, len(drinks), best, best_cups, recent


def report_fast(orders, top):
    """Cùng kết quả với report_slow cho mọi sổ và mọi top >= 0; 200.000 đơn trong 2 giây; không sửa orders.
    Không gọi report_slow; không dùng insert(0, ...), pop(0), nối list bằng + trong vòng lặp; không dùng dict, set."""
    raise NotImplementedError


def next_code(orders):
    """Mã đơn tiếp theo: "TCH" + số thứ tự 4 chữ số, số thứ tự = số đơn hiện có + 1."""
    raise NotImplementedError


def add_order(orders, drink_text, cups_text):
    """Ghi đơn mới vào cuối sổ, trả về đơn. drink_text là số thứ tự món trong DRINKS (1-5).
    Lỗi (sổ giữ nguyên): "Món phải là số từ 1 đến 5", "Số ly phải là số nguyên từ 1 đến 20"."""
    raise NotImplementedError


def find_order(orders, code):
    """Đơn có mã code (không phân biệt hoa thường) hoặc None."""
    raise NotImplementedError


def benchmark(sizes, number=1):
    """Với từng n trong sizes, trên make_big_orders(n) và top = 3: đo bằng timeit một lần report_slow và report_fast (ms).
    Trả về list bộ (n, ms bản cũ, ms bản mới)."""
    raise NotImplementedError
