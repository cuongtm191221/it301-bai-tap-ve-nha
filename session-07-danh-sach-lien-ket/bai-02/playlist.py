"""Danh sách phát nhạc: danh sách liên kết đơn có head, tail, size."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Playlist:
    def __init__(self):
        self.head = None    # bài sẽ phát đầu tiên
        self.tail = None    # bài cuối danh sách
        self.size = 0       # số bài trong danh sách

    def add_first(self, code):
        # Chèn bài "phát tiếp theo" vào đầu danh sách
        node = Node(code, self.head)
        self.head = node

    def add_last(self, code):
        # Thêm bài vào cuối danh sách
        node = Node(code)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
        self.size += 1

    def to_text(self):
        parts = []
        current = self.head
        while current is not None:
            parts.append(current.value)
            current = current.next
        return " -> ".join(parts + ["None"])


if __name__ == "__main__":
    playlist = Playlist()
    # Người nghe thêm ba bài vào cuối danh sách
    playlist.add_last("ZM001")
    playlist.add_last("ZM002")
    playlist.add_last("ZM003")
    # Người nghe chọn "phát tiếp theo" cho bài ZM000
    playlist.add_first("ZM000")
    print("Danh sách phát:", playlist.to_text())
    print("Bài cuối danh sách:", playlist.tail.value)
    print("Số bài:", playlist.size)

    # Một danh sách mới: chọn "phát tiếp theo" trước, rồi mới thêm vào cuối
    morning = Playlist()
    morning.add_first("ZM010")
    morning.add_last("ZM011")
    print("Danh sách buổi sáng:", morning.to_text())
