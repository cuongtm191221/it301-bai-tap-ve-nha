"""Nghiệp vụ lịch sử xem của ứng dụng Galaxy Play.

Lịch sử là danh sách liên kết đôi: head là mục xem cũ nhất, tail là mục vừa xem. Giữ tối đa MAX_ITEMS mục.
Không dùng list Python để lưu lịch sử.
"""

MAX_ITEMS = 6
EMPTY_MESSAGE = "danh sách rỗng, không có phần tử để xóa"


class DNode:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next


class WatchHistory:
    """Danh sách liên kết đôi có head, tail và size (số node, cập nhật trong mọi phương thức thêm, xóa)."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def to_text(self):
        """Có sẵn. Duyệt xuôi từ head: "A -> B -> None"."""
        parts, current = [], self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " -> ".join(parts + ["None"])

    def to_text_backward(self):
        """Duyệt ngược từ tail theo prev, cùng dạng với to_text."""
        raise NotImplementedError

    def add_first(self, value):
        """Thêm value trước head."""
        raise NotImplementedError

    def add_last(self, value):
        """Thêm value sau tail."""
        raise NotImplementedError

    def remove_first(self):
        """Xóa node head, trả về giá trị; rỗng báo IndexError(EMPTY_MESSAGE). head mới có prev là None."""
        raise NotImplementedError

    def remove_last(self):
        """Xóa node tail, trả về giá trị; rỗng báo IndexError(EMPTY_MESSAGE). tail mới có next là None."""
        raise NotImplementedError


def make_history():
    """Có sẵn. Lịch sử mẫu, cũ nhất trước."""
    history = WatchHistory()
    for title in ["Hành trình biển xanh", "Bếp nhà mình tập 3", "Trận cầu đỉnh cao", "Hoạt hình Thỏ con"]:
        history.add_last(title)
    return history


def check_title(text):
    """Tên bỏ khoảng trắng hai đầu; rỗng hoặc dài hơn 40 ký tự báo ValueError("Tên phim phải có từ 1 đến 40 ký tự")."""
    raise NotImplementedError


def watch(history, text):
    """Ghi phim vừa xem vào cuối; vượt MAX_ITEMS thì bỏ mục cũ nhất. Trả về (tên, tên mục bị bỏ hoặc None)."""
    raise NotImplementedError


def undo_last(history):
    """Xóa mục vừa xem, trả về tên; lịch sử trống báo ValueError("Lịch sử xem đang trống")."""
    raise NotImplementedError


def import_old(history, text):
    """Nhập một mục cũ từ thiết bị khác vào đầu lịch sử, trả về tên; đã đủ MAX_ITEMS mục báo
    ValueError("Lịch sử đã đủ 6 mục, không nhập thêm mục cũ"). Kiểm tra tên trước."""
    raise NotImplementedError
