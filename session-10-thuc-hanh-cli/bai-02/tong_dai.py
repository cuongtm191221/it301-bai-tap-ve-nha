"""Nghiệp vụ hàng chờ cuộc gọi tổng đài chăm sóc khách hàng Mobifone.

Cuộc gọi là tuple (mã, số điện thoại); gọi trước được nghe trước. Hàng chờ là LinkedQueue: danh sách liên kết đơn
có head (cuộc gọi được nhận tiếp theo), tail (cuộc gọi vừa đến) và _size. Không dùng list Python để lưu hàng chờ.
"""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedQueue:
    """Hàng đợi: thêm ở tail, lấy ở head."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0
        self.issued = 0

    def enqueue(self, value):
        """Thêm value vào cuối hàng."""
        raise NotImplementedError

    def dequeue(self):
        """Lấy và trả về phần tử đầu hàng; rỗng báo IndexError("hàng đợi rỗng"). Lấy phần tử cuối cùng thì tail về None."""
        raise NotImplementedError

    def peek(self):
        """Trả về phần tử đầu hàng, không lấy ra; rỗng báo IndexError("hàng đợi rỗng")."""
        raise NotImplementedError

    def is_empty(self):
        """True nếu hàng đợi rỗng."""
        raise NotImplementedError

    def size(self):
        """Số phần tử, không duyệt."""
        raise NotImplementedError


def incoming(queue, phone_text):
    """Cuộc gọi đến từ số phone_text (bỏ khoảng trắng hai đầu; 10 chữ số, bắt đầu bằng 0; sai báo
    ValueError("Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0")). Số đang chờ thì báo ValueError("Số <số> đang trong hàng chờ").
    Mã "CG" + số lượt đã cấp (3 chữ số). Trả về cuộc gọi."""
    raise NotImplementedError


def answer(queue):
    """Tổng đài viên nhận cuộc gọi đầu hàng; hàng trống báo ValueError("Không có cuộc gọi đang chờ"). Trả về cuộc gọi."""
    raise NotImplementedError


def make_queue():
    """Có sẵn. Hàng chờ mẫu 3 cuộc gọi."""
    queue = LinkedQueue()
    for phone in ["0901234567", "0912000111", "0388765432"]:
        incoming(queue, phone)
    return queue


def waiting(queue):
    """Có sẵn. List các cuộc gọi đang chờ, đầu hàng trước (chỉ để in)."""
    result, current = [], queue.head
    while current is not None:
        result.append(current.value)
        current = current.next
    return result
