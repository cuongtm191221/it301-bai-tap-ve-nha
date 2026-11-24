"""Nghiệp vụ lệnh chuyển tiền chờ xử lý tại Agribank.

Lệnh là tuple (mã lệnh, số tài khoản nhận, số tiền). Lệnh được xử lý theo thứ tự nhập: lấy ở head, nhập ở tail.
Danh sách lệnh là danh sách liên kết đơn có head, tail, size. Không dùng list Python để lưu danh sách lệnh.
"""
import sys
import timeit


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class OrderLine:
    """Danh sách liên kết đơn có head, tail, size; issued là số lệnh đã cấp mã."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.issued = 0

    def add_last(self, value):
        """Thêm value sau tail, tăng size."""
        raise NotImplementedError

    def remove_first(self):
        """Lấy và trả về giá trị ở head, giảm size; rỗng báo IndexError("danh sách rỗng, không có phần tử để lấy")."""
        raise NotImplementedError


def money(value):
    """Có sẵn. 2500000 -> "2.500.000đ"."""
    return f"{value:,}".replace(",", ".") + "đ"


def submit(line, account_text, amount_text):
    """Nhập lệnh: tài khoản đủ 13 chữ số, số tiền là số nguyên 10.000 đến 500.000.000. Mã lệnh "LC" + số lệnh đã cấp (4 chữ số).
    Lỗi: "Số tài khoản phải gồm 13 chữ số", "Số tiền phải là số nguyên từ 10.000 đến 500.000.000". Trả về lệnh vừa nhập."""
    raise NotImplementedError


def make_line():
    """Có sẵn. Danh sách mẫu 4 lệnh."""
    line = OrderLine()
    for account, amount in [("1500201234567", "2500000"), ("3100205551234", "15000000"),
                            ("1500209876543", "750000"), ("5400201112223", "120000000")]:
        submit(line, account, amount)
    return line


def pending_total(line):
    """Tổng số tiền các lệnh đang chờ, duyệt từ head."""
    raise NotImplementedError


def process(line, k_text):
    """Xử lý tối đa k lệnh (k nguyên dương) theo thứ tự, trả về list lệnh đã xử lý.
    Lỗi: "Số lệnh phải là số nguyên dương"; không còn lệnh: "Không có lệnh chờ xử lý"."""
    raise NotImplementedError


def bench_drain(sizes, number=1):
    """Với từng n: dựng sẵn list và OrderLine n phần tử (không tính giờ), đo (ms) lấy hết từ đầu bằng pop(0) và bằng remove_first.
    Trả về list bộ (n, ms list, ms danh sách liên kết)."""
    raise NotImplementedError


def memory_per_item():
    """Byte cho mỗi phần tử: list = (getsizeof([0] * 1000) - getsizeof([])) / 1000; node = getsizeof(Node(0)) + getsizeof(Node(0).__dict__).
    Không tính bộ nhớ của chính giá trị. Trả về (byte mỗi ô list, byte mỗi node)."""
    raise NotImplementedError
