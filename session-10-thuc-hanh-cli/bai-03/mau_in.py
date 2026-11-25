"""Nghiệp vụ kiểm tra mẫu in hóa đơn trên Sapo.

Mẫu in chứa biến trong ngoặc như {ten_khach}, [ma_don], (tong_tien). Các cặp ngoặc (), [], {} phải mở, đóng đúng cặp,
đúng thứ tự. Phần nằm giữa hai dấu nháy kép "..." là văn bản in nguyên, ngoặc trong đó không tính.
Kiểm tra dùng LinkedStack (danh sách liên kết, đỉnh ở head); không dùng list Python làm ngăn xếp.
"""

PAIRS = {")": "(", "]": "[", "}": "{"}


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedStack:
    """Ngăn xếp cài bằng danh sách liên kết: đỉnh là head."""

    def __init__(self):
        self.head = None
        self._size = 0

    def push(self, value):
        """Đặt value lên đỉnh."""
        raise NotImplementedError

    def pop(self):
        """Lấy và trả về phần tử ở đỉnh; rỗng báo IndexError("ngăn xếp rỗng")."""
        raise NotImplementedError

    def peek(self):
        """Phần tử ở đỉnh, không lấy ra; rỗng báo IndexError("ngăn xếp rỗng")."""
        raise NotImplementedError

    def is_empty(self):
        """True nếu rỗng."""
        raise NotImplementedError

    def size(self):
        """Số phần tử, không duyệt."""
        raise NotImplementedError


def check_template(text):
    """Kiểm tra mẫu in (vị trí đếm từ 1 theo ký tự của text). Hợp lệ trả None; không thì trả về thông báo lỗi ĐẦU TIÊN gặp khi đọc
    từ trái sang phải:
      - "Vị trí <p>: dấu '<c>' không có dấu mở"
      - "Vị trí <p>: dấu '<c>' không khớp với '<o>' ở vị trí <q>"
      - hết chuỗi còn nháy kép mở: "Vị trí <q>: dấu nháy kép chưa được đóng"
      - hết chuỗi còn ngoặc mở: "Vị trí <q>: dấu '<o>' chưa được đóng" (ngoặc mở gần cuối nhất)."""
    raise NotImplementedError


def is_balanced(text):
    """True nếu check_template(text) không báo lỗi."""
    raise NotImplementedError


def clean(text):
    """Có sẵn. Bỏ khoảng trắng hai đầu; rỗng hoặc dài hơn 200 ký tự báo ValueError("Mẫu in phải có từ 1 đến 200 ký tự")."""
    text = text.strip()
    if not 1 <= len(text) <= 200:
        raise ValueError("Mẫu in phải có từ 1 đến 200 ký tự")
    return text


def add_template(templates, text):
    """Thêm mẫu hợp lệ vào list templates, trả về mẫu; mẫu lỗi báo ValueError(<thông báo của check_template>)."""
    raise NotImplementedError


def make_templates():
    """Có sẵn. Các mẫu đang dùng."""
    return ["Khách: {ten_khach} - Đơn [ma_don]", "Tổng tiền: (tong_tien) đồng", 'Ghi chú: "(không xuất hóa đơn đỏ" {ghi_chu}']
