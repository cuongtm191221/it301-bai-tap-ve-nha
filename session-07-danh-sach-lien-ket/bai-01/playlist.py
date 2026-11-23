"""Danh sách phát nhạc: danh sách liên kết đơn có head, tail."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Playlist:
    def __init__(self):
        self.head = None    # bài sẽ phát đầu tiên
        self.tail = None    # bài cuối danh sách

    def add_last(self, code):
        # Cho sẵn, đã đúng: thêm bài vào cuối danh sách
        node = Node(code)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def count(self):
        # Đếm số bài trong danh sách
        total = 0
        current = self.head
        while current.next is not None:
            total += 1
            current = current.next
        return total

    def find(self, code):
        # Trả về vị trí (tính từ 0) của bài có mã code, không có thì trả None
        position = 0
        while self.head is not None:
            if self.head.value == code:
                return position
            self.head = self.head.next
            position += 1
        return position

    def to_text(self):
        # Cho sẵn, đã đúng
        parts = []
        current = self.head
        while current is not None:
            parts.append(current.value)
            current = current.next
        return " -> ".join(parts + ["None"])


if __name__ == "__main__":
    playlist = Playlist()
    for code in ["ZM001", "ZM002", "ZM003", "ZM004"]:
        playlist.add_last(code)
    print("Số bài:", playlist.count())
    print("Vị trí của ZM003:", playlist.find("ZM003"))
    print("Danh sách phát:", playlist.to_text())
    print("Vị trí của ZM999:", playlist.find("ZM999"))
    print("Danh sách phát:", playlist.to_text())

    # Danh sách mới tạo, chưa có bài nào
    empty = Playlist()
    print("Số bài của danh sách mới:", empty.count())
