"""Lọc bài trùng trong danh sách phát: danh sách liên kết đơn có head, tail, size; mỗi node giữ một mã bài."""


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


def remove_duplicates(playlist):
    """Bỏ các bài trùng mã, giữ lại lần xuất hiện đầu tiên. Trả về số bài đã bỏ."""
    removed = 0
    current = playlist.head
    while current is not None:
        runner = current
        while runner.next is not None:
            if runner.next.value == current.value:
                runner.next = runner.next.next
                removed += 1
            runner = runner.next
        current = current.next
    return removed


def remove_duplicates_fast(playlist):
    """Giải pháp thứ hai do bạn đề xuất: cùng kết quả với remove_duplicates nhưng nhanh hơn khi danh sách dài."""
    raise NotImplementedError


if __name__ == "__main__":
    # Đoạn chạy thử: đổi dãy mã bài dưới đây để thử các bộ dữ liệu của bạn
    codes = ["ZM001", "ZM002", "ZM001", "ZM003"]
    playlist = Playlist()
    for code in codes:
        playlist.add_last(code)
    print("Trước khi lọc:", playlist.to_text())
    print("Số bài đã bỏ:", remove_duplicates(playlist))
    print("Sau khi lọc:", playlist.to_text())
