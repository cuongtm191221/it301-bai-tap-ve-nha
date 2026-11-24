"""Nghiệp vụ danh sách "Xem tiếp" của ứng dụng FPT Play.

Danh sách là danh sách liên kết đơn có head (chương trình xem gần nhất) và tail (chương trình lâu nhất chưa xem lại).
Giữ tối đa MAX_SHOWS chương trình. Không dùng list Python để lưu danh sách.
"""

MAX_SHOWS = 5


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class ContinueList:
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

    def add_first(self, value):
        """Thêm value vào đầu (trước head); danh sách rỗng thì node mới cũng là tail."""
        raise NotImplementedError

    def add_last(self, value):
        """Thêm value vào cuối (sau tail)."""
        raise NotImplementedError

    def count(self):
        """Số node, đếm bằng cách duyệt từ head."""
        raise NotImplementedError

    def find(self, value):
        """Vị trí (đếm từ 0) của node đầu tiên có giá trị value, không có trả None."""
        raise NotImplementedError

    def remove(self, value):
        """Xóa node đầu tiên có giá trị value, trả True; không có trả False. Giữ đúng head, tail ở mọi trường hợp."""
        raise NotImplementedError


def make_list():
    """Có sẵn. Danh sách mẫu, chương trình xem gần nhất đứng đầu."""
    shows = ContinueList()
    for title in ["Cà phê sáng", "V-League vòng 5", "Thời sự 19h", "Phim tối thứ Bảy"]:
        shows.add_last(title)
    return shows


def check_title(text):
    """Tên bỏ khoảng trắng hai đầu; rỗng hoặc dài hơn 40 ký tự báo ValueError("Tên chương trình phải có từ 1 đến 40 ký tự")."""
    raise NotImplementedError


def watch(shows, text):
    """Người dùng mở chương trình text: đưa lên đầu (đã có thì chuyển lên, không lặp). Vượt MAX_SHOWS thì bỏ chương trình ở tail.
    Trả về tên chương trình bị bỏ, hoặc None."""
    raise NotImplementedError


def finish(shows, text):
    """Xem xong: xóa chương trình text, trả về tên; không có báo ValueError("Không có <tên> trong danh sách xem tiếp")."""
    raise NotImplementedError


def next_show(shows):
    """Chương trình ở head, danh sách rỗng trả None."""
    raise NotImplementedError
