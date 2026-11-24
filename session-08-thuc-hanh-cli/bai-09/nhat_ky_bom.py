"""Nghiệp vụ báo cáo ca của trụ bơm xăng Petrolimex.

Nhật ký bơm là danh sách liên kết đơn có head, tail; mỗi node giữ một lần bơm (mã, loại nhiên liệu, số decilít).
Số lít lưu bằng số nguyên decilít (12,5 lít = 125) để không sai số thập phân. Không dùng list Python để lưu nhật ký.
"""
import timeit

FUELS = ("RON95", "E5", "DO")


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class PumpLog:
    """Có sẵn. Danh sách liên kết đơn có head, tail; issued là số lần bơm đã cấp mã."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.issued = 0

    def add_last(self, value):
        """Có sẵn. Thêm value sau tail."""
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def count(self):
        """Có sẵn. Số node."""
        total, current = 0, self.head
        while current is not None:
            total += 1
            current = current.next
        return total

    def get(self, index):
        """Có sẵn. Giá trị ở chỉ số index (đếm từ 0)."""
        current = self.head
        for _ in range(index):
            current = current.next
        return current.value


def liters_text(dl):
    """Có sẵn. 125 -> "12.5"."""
    return f"{dl // 10}.{dl % 10}"


def parse_liters(text):
    """Có sẵn. "12.5" hoặc "12,5" hoặc "12" -> số decilít; ngoài 0,1..200 lít hoặc quá 1 chữ số thập phân báo
    ValueError("Số lít phải từ 0.1 đến 200, tối đa 1 chữ số thập phân")."""
    text = text.strip().replace(",", ".")
    whole, _, part = text.partition(".")
    if not whole.isdigit() or len(part) > 1 or (part and not part.isdigit()) or (_ and not part):
        raise ValueError("Số lít phải từ 0.1 đến 200, tối đa 1 chữ số thập phân")
    dl = int(whole) * 10 + (int(part) if part else 0)
    if not 1 <= dl <= 2000:
        raise ValueError("Số lít phải từ 0.1 đến 200, tối đa 1 chữ số thập phân")
    return dl


def record(log, fuel_text, liters):
    """Ghi lần bơm: loại nhiên liệu là một trong FUELS (không phân biệt hoa thường, sai báo
    ValueError("Nhiên liệu phải là RON95, E5 hoặc DO")), số lít theo parse_liters. Mã "B" + 5 chữ số. Trả về lần bơm."""
    raise NotImplementedError


def make_log():
    """Có sẵn. Nhật ký mẫu 6 lần bơm."""
    log = PumpLog()
    for fuel, liters in [("RON95", "35.5"), ("DO", "120"), ("E5", "18.2"), ("RON95", "50"), ("DO", "120.0"), ("E5", "7.5")]:
        record(log, fuel, liters)
    return log


def make_big_log(n):
    """Có sẵn. Nhật ký giả lập n lần bơm."""
    log = PumpLog()
    for k in range(n):
        log.add_last(("B%05d" % k, FUELS[k % 3], 1 + k * 37 % 2000))
    return log


def report_slow(log, threshold):
    """Có sẵn. Bản cũ đang chạy, KHÔNG sửa. threshold là số decilít. Trả về (tổng decilít theo thứ tự FUELS dưới dạng tuple,
    mã lần bơm nhiều nhất (bằng nhau lấy lần đầu; nhật ký rỗng là None), list mã các lần bơm từ threshold trở lên)."""
    totals = (0, 0, 0)
    largest = None
    largest_dl = 0
    over = []
    for i in range(log.count()):
        code, fuel, dl = log.get(i)
        k = FUELS.index(fuel)
        totals = totals[:k] + (totals[k] + dl,) + totals[k + 1:]
        if dl > largest_dl:
            largest, largest_dl = code, dl
        if dl >= threshold:
            over = over + [code]
    return totals, largest, over


def report_fast(log, threshold):
    """Cùng kết quả với report_slow; 200.000 lần bơm trong 1 giây. Không gọi report_slow, không gọi get, count; không làm đổi nhật ký."""
    raise NotImplementedError


def benchmark(sizes, number=1):
    """Với từng n trên make_big_log(n), ngưỡng 1000 decilít: đo (ms) report_slow và report_fast. Trả về list bộ (n, ms bản cũ, ms bản mới)."""
    raise NotImplementedError
