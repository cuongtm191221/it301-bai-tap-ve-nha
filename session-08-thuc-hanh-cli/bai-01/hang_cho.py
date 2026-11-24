"""Nghiệp vụ hàng chờ nhận hàng tại bưu cục Viettel Post.

Hàng chờ là danh sách liên kết đơn có head (khách được gọi tiếp theo) và tail (khách vừa lấy số).
Mỗi node giữ một số thứ tự dạng "VP001". Không dùng list Python để lưu hàng chờ.
"""

EMPTY_MESSAGE = "danh sách rỗng, không có phần tử để lấy"


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class WaitingLine:
    """Danh sách liên kết đơn có head, tail; issued là số lượt đã cấp số."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.issued = 0

    def to_text(self):
        """Có sẵn. Chuỗi dạng "VP001 -> VP002 -> None"."""
        parts = []
        current = self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " -> ".join(parts + ["None"])

    def add_last(self, value):
        """Thêm value vào cuối (sau tail); danh sách rỗng thì node mới vừa là head vừa là tail."""
        raise NotImplementedError

    def remove_first(self):
        """Lấy và trả về giá trị ở head; rỗng báo IndexError(EMPTY_MESSAGE). Lấy node cuối cùng thì tail cũng về None."""
        raise NotImplementedError

    def count(self):
        """Số node, đếm bằng cách duyệt từ head."""
        raise NotImplementedError

    def find(self, value):
        """Vị trí (đếm từ 0) của node đầu tiên có giá trị value, không có trả None."""
        raise NotImplementedError

    def remove(self, value):
        """Xóa node đầu tiên có giá trị value, trả True; không có trả False. Xóa trúng tail thì tail lùi về node trước."""
        raise NotImplementedError


def take_ticket(line):
    """Cấp số mới "VP" + số lượt đã cấp (đủ 3 chữ số), thêm vào cuối hàng; trả về số đó."""
    raise NotImplementedError


def make_line():
    """Có sẵn. Hàng chờ mẫu: đã cấp VP001 đến VP004."""
    line = WaitingLine()
    for _ in range(4):
        take_ticket(line)
    return line


def normalize(text):
    """Số thứ tự viết hoa, bỏ khoảng trắng; sai dạng báo ValueError("Số thứ tự phải có dạng VP và 3 chữ số")."""
    raise NotImplementedError


def call_next(line):
    """Gọi khách đầu hàng: trả về số thứ tự (hàng trống thì IndexError của remove_first)."""
    raise NotImplementedError


def position(line, text):
    """Vị trí (đếm từ 1) của số thứ tự text trong hàng; không có báo ValueError("Không có số <số> trong hàng chờ")."""
    raise NotImplementedError


def leave(line, text):
    """Khách bỏ về: xóa số thứ tự text khỏi hàng, trả về số đã chuẩn hóa; không có báo ValueError như position."""
    raise NotImplementedError
