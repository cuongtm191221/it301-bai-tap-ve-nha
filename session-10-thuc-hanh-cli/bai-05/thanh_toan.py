"""Nghiệp vụ hàng đợi yêu cầu thanh toán của ví MoMo, kèm đo ba cách cài hàng đợi.

Yêu cầu là tuple (mã, số điện thoại, số tiền); gửi trước xử lý trước. Hàng đợi của hệ thống là collections.deque
(append ở cuối, popleft ở đầu). LinkedQueue (Session 09) có sẵn để so sánh.
"""
import sys
import timeit
from collections import deque


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedQueue:
    """Có sẵn. Hàng đợi liên kết của Session 09."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, value):
        """Có sẵn."""
        node = Node(value)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self._size += 1

    def dequeue(self):
        """Có sẵn. Rỗng báo IndexError("hàng đợi rỗng")."""
        if self.head is None:
            raise IndexError("hàng đợi rỗng")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        return value


class PaymentQueue:
    """Có sẵn. Hàng đợi yêu cầu (requests là deque) và số yêu cầu đã cấp mã."""

    def __init__(self):
        self.requests = deque()
        self.issued = 0


def money(value):
    """Có sẵn. 150000 -> "150.000đ"."""
    return f"{value:,}".replace(",", ".") + "đ"


def submit(queue, phone_text, amount_text):
    """Gửi yêu cầu: số điện thoại 10 chữ số bắt đầu bằng 0 (sai báo ValueError("Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0")),
    số tiền nguyên 1.000 đến 50.000.000 (sai báo ValueError("Số tiền phải là số nguyên từ 1.000 đến 50.000.000")).
    Mã "YC" + 5 chữ số. Thêm vào cuối hàng đợi, trả về yêu cầu."""
    raise NotImplementedError


def make_queue():
    """Có sẵn. Hàng đợi mẫu 4 yêu cầu."""
    queue = PaymentQueue()
    for phone, amount in [("0901112223", "150000"), ("0934556677", "2500000"), ("0987001122", "45000"), ("0909090909", "800000")]:
        submit(queue, phone, amount)
    return queue


def process(queue, k_text):
    """Xử lý tối đa k yêu cầu đầu hàng (k nguyên dương; sai báo ValueError("Số yêu cầu phải là số nguyên dương");
    hàng trống báo ValueError("Không có yêu cầu đang chờ")). Trả về list yêu cầu đã xử lý theo thứ tự."""
    raise NotImplementedError


def bench_drain(sizes):
    """Với từng n: dựng sẵn ba hàng đợi n phần tử (list, LinkedQueue, deque; không tính giờ) rồi đo (ms) lấy hết từ đầu bằng
    pop(0), dequeue, popleft. Trả về list bộ (n, ms list, ms LinkedQueue, ms deque)."""
    raise NotImplementedError


def memory_report(n):
    """Byte của chính cấu trúc khi chứa n số nguyên (không tính các số): (getsizeof(list n phần tử), getsizeof(deque n phần tử))."""
    raise NotImplementedError
