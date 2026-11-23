"""Tính năng "Phát ngay": chuyển một bài lên đầu danh sách phát."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Playlist:
    def __init__(self):
        self.head = None    # bài sẽ phát đầu tiên
        self.tail = None    # bài cuối danh sách
        self.size = 0       # số bài trong danh sách

    def add_first(self, value):
        # Cho sẵn, đã đúng
        node = Node(value, self.head)
        self.head = node
        if self.tail is None:
            self.tail = node
        self.size += 1

    def add_last(self, value):
        # Cho sẵn, đã đúng
        node = Node(value)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def find(self, value):
        # Cho sẵn, đã đúng: vị trí của value, không có thì None
        position = 0
        current = self.head
        while current is not None:
            if current.value == value:
                return position
            current = current.next
            position += 1
        return None

    def to_text(self):
        # Cho sẵn, đã đúng
        parts = []
        current = self.head
        while current is not None:
            parts.append(current.value)
            current = current.next
        return " -> ".join(parts + ["None"])


def play_now(playlist, code):
    # Chuyển bài có mã code lên đầu danh sách phát. Trả True nếu bài có trong danh sách, False nếu không.
    prev = playlist.head
    while prev.next is not None:
        if prev.next.value == code:
            prev.next = prev.next.next
            break
        prev = prev.next
    playlist.add_first(code)
    return True


if __name__ == "__main__":
    playlist = Playlist()
    for code in ["ZM001", "ZM002", "ZM003", "ZM004"]:
        playlist.add_last(code)
    print("Phát ngay ZM003:", play_now(playlist, "ZM003"))
    print("Danh sách phát:", playlist.to_text(), "| số bài:", playlist.size)
    print("Phát ngay ZM004:", play_now(playlist, "ZM004"))
    print("Danh sách phát:", playlist.to_text(), "| bài cuối:", playlist.tail.value)
    print("Phát ngay ZM004 lần nữa:", play_now(playlist, "ZM004"))
    print("Phát ngay ZM999:", play_now(playlist, "ZM999"))
    playlist.add_last("ZM005")
    print("Danh sách phát:", playlist.to_text(), "| số bài:", playlist.size)

    # Danh sách mới tạo, chưa có bài nào
    empty = Playlist()
    print("Phát ngay trên danh sách mới:", play_now(empty, "ZM001"))
