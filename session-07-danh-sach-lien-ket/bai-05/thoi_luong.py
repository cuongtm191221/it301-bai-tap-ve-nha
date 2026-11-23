"""Thống kê thời lượng danh sách phát. Mỗi node giữ chuỗi "MÃ_BÀI - SỐ_GIÂY"."""


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


def total_seconds(playlist):
    # Tổng số giây của mọi bài trong danh sách phát
    total = 0
    current = playlist.head.next
    while current is not None:
        total += int(current.value.split(" - ")[1])
        current = current.next
    return total


def longest_song(playlist):
    # Bài có thời lượng dài nhất; bằng nhau thì lấy bài đứng trước; danh sách rỗng trả None
    best = playlist.head
    current = playlist.head.next
    while current is not None:
        if current.value.split(" - ")[1] > best.value.split(" - ")[1]:
            best = current
        current = current.next
    return best.value


def format_duration(seconds):
    # Đổi số giây thành chuỗi "phút:giây", phần giây luôn có hai chữ số
    minutes = seconds // 60
    rest = seconds % 60
    return str(minutes) + ":" + str(rest)


if __name__ == "__main__":
    playlist = Playlist()
    for song in ["ZM001 - 215", "ZM002 - 95", "ZM003 - 248", "ZM004 - 185"]:
        playlist.add_last(song)
    print("Tổng thời lượng:", format_duration(total_seconds(playlist)))
    print("Bài dài nhất:", longest_song(playlist))
    print("Thời lượng bài ZM004:", format_duration(185))

    # Danh sách mới tạo, chưa có bài nào
    empty = Playlist()
    print("Tổng thời lượng danh sách mới:", format_duration(total_seconds(empty)))
    print("Bài dài nhất của danh sách mới:", longest_song(empty))
