"""Nghiệp vụ hành trình nhiều chặng của Vietnam Airlines: đảo chiều hành trình để tạo chuyến về.

Hành trình là danh sách liên kết đơn có head (sân bay đi), tail (sân bay đến cuối). Mỗi node giữ mã sân bay 3 chữ cái.
Không dùng list Python để lưu hành trình.
"""
import timeit


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Route:
    """Danh sách liên kết đơn có head, tail."""

    def __init__(self):
        self.head = None
        self.tail = None

    def add_last(self, value):
        """Có sẵn. Thêm value sau tail."""
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def to_text(self):
        """Có sẵn. Chuỗi dạng "HAN -> DAD -> None"."""
        parts, current = [], self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " -> ".join(parts + ["None"])


def make_route():
    """Có sẵn. Hành trình mẫu."""
    route = Route()
    for code in ["HAN", "DAD", "SGN", "PQC"]:
        route.add_last(code)
    return route


def make_big_route(n):
    """Có sẵn. Hành trình giả lập n điểm."""
    route = Route()
    for k in range(n):
        route.add_last(k)
    return route


def add_airport(route, text):
    """Thêm sân bay vào cuối: mã 3 chữ cái (viết hoa, bỏ khoảng trắng). Lỗi: "Mã sân bay phải gồm 3 chữ cái",
    "Sân bay trùng với điểm cuối hành trình". Trả về mã đã thêm."""
    raise NotImplementedError


def reverse_v1(route):
    """Giải pháp 1. Đảo chiều hành trình ngay trên route: không tạo node mới, không dùng list; head, tail đúng sau khi đảo."""
    raise NotImplementedError


def reverse_v2(route):
    """Giải pháp 2: cùng kết quả, cách làm khác, nhanh hơn rõ rệt; 200.000 điểm trong 1 giây. Cùng các ràng buộc."""
    raise NotImplementedError


def benchmark(sizes, number=1):
    """Với từng n: đo (ms) mỗi giải pháp trên một make_big_route(n) mới (thời gian tạo không tính). Trả về list bộ (n, ms 1, ms 2)."""
    raise NotImplementedError
