"""Nghiệp vụ danh sách đặt cọc trước điện thoại mới của CellphoneS.

Danh sách là danh sách liên kết đơn có head (khách đặt sớm nhất), tail (khách cuối). Mỗi node giữ mã khách "KH" + 3 chữ số.
Vị trí người dùng nhập đếm từ 1; chỉ số trong lớp đếm từ 0. Không dùng list Python để lưu danh sách.
"""

PAGE_SIZE = 3


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class PreorderList:
    """Danh sách liên kết đơn có head, tail."""

    def __init__(self):
        self.head = None
        self.tail = None

    def to_text(self):
        """Có sẵn. Chuỗi dạng "A -> B -> None"."""
        parts = []
        current = self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " -> ".join(parts + ["None"])

    def count(self):
        """Số node, đếm bằng cách duyệt từ head."""
        raise NotImplementedError

    def add_last(self, value):
        """Thêm value vào cuối (sau tail)."""
        raise NotImplementedError

    def get(self, index):
        """Giá trị của node thứ index (đếm từ 0); ngoài 0..count()-1 báo IndexError("Chỉ số ngoài phạm vi")."""
        raise NotImplementedError

    def insert_at(self, index, value):
        """Chèn value để nó đứng ở chỉ số index (0 là trước head, count() là sau tail); ngoài 0..count() báo IndexError("Chỉ số ngoài phạm vi")."""
        raise NotImplementedError

    def remove_at(self, index):
        """Xóa node ở chỉ số index, trả về giá trị; ngoài 0..count()-1 báo IndexError("Chỉ số ngoài phạm vi")."""
        raise NotImplementedError


def make_list():
    """Có sẵn. Danh sách mẫu KH101 đến KH105."""
    customers = PreorderList()
    for k in range(101, 106):
        customers.add_last("KH%d" % k)
    return customers


def check_code(customers, text):
    """Mã khách viết hoa, bỏ khoảng trắng; sai dạng báo ValueError("Mã khách phải có dạng KH và 3 chữ số"),
    đã có báo ValueError("Khách <mã> đã có trong danh sách")."""
    raise NotImplementedError


def parse_position(text, largest):
    """Vị trí (số nguyên 1..largest). Không phải số nguyên: ValueError("Vị trí phải là số nguyên");
    ngoài khoảng: ValueError("Vị trí phải từ 1 đến <largest>")."""
    raise NotImplementedError


def deposit(customers, text):
    """Khách đặt cọc: thêm vào cuối; trả về (mã, vị trí)."""
    raise NotImplementedError


def prioritize(customers, text, position_text):
    """Chèn khách ưu tiên vào vị trí 1..count()+1; trả về (mã, vị trí). Kiểm tra mã trước, vị trí sau."""
    raise NotImplementedError


def cancel_at(customers, position_text):
    """Hủy suất ở vị trí 1..count(); trả về (mã, vị trí). Danh sách rỗng báo ValueError("Danh sách đặt cọc đang trống")."""
    raise NotImplementedError


def page(customers, start_text):
    """Tối đa PAGE_SIZE khách từ vị trí start (1..count()): list các cặp (vị trí, mã)."""
    raise NotImplementedError
