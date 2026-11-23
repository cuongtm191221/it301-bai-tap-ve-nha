"""Phát đảo ngược danh sách phát: danh sách liên kết đơn có head, tail, size; mỗi node giữ một mã bài."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Playlist:
    """Danh sách liên kết đơn có head, tail, size. Lớp này đã đúng, không cần sửa."""

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_last(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1

    def to_text(self):
        parts = []
        current = self.head
        while current is not None:
            parts.append(current.value)
            current = current.next
        return " -> ".join(parts + ["None"])


def reversed_copy(playlist):
    """Trả về một Playlist mới có thứ tự ngược lại, danh sách gốc giữ nguyên (xem đề, mục 2.1)."""
    raise NotImplementedError


def reverse_in_place(playlist):
    """Đảo thứ tự ngay trên danh sách đang có, không tạo node mới, không trả về gì (xem đề, mục 2.2)."""
    raise NotImplementedError


if __name__ == "__main__":
    playlist = Playlist()
    for code in ["ZM001", "ZM002", "ZM003", "ZM004"]:
        playlist.add_last(code)

    copy = reversed_copy(playlist)
    print("Bản đảo:", copy.to_text())
    print("Danh sách gốc:", playlist.to_text())
    copy.add_last("ZM005")
    print("Bản đảo sau khi thêm ZM005:", copy.to_text(), "| số bài:", copy.size)
    print("Danh sách gốc:", playlist.to_text(), "| số bài:", playlist.size)

    reverse_in_place(playlist)
    print("Đảo tại chỗ:", playlist.to_text())
    print("Bài đầu:", playlist.head.value, "| bài cuối:", playlist.tail.value)
    playlist.add_last("ZM006")
    print("Sau khi thêm ZM006:", playlist.to_text(), "| số bài:", playlist.size)

    empty = Playlist()
    reverse_in_place(empty)
    print("Danh sách trống:", empty.to_text(), "|", reversed_copy(empty).to_text())
