"""Trình phát nhạc: danh sách liên kết đôi và con trỏ current chỉ bài đang phát."""


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class Player:
    def __init__(self):
        self.head = None       # bài đầu danh sách phát
        self.tail = None       # bài cuối danh sách phát
        self.current = None    # bài đang phát, None khi chưa phát bài nào

    def add_last(self, code):
        # Cho sẵn, đã đúng: thêm bài vào cuối, nối đủ hai chiều
        node = Node(code)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

    def play_first(self):
        # Bắt đầu phát từ bài đầu danh sách
        self.current = self.head
        return "Đang phát: " + self.current.value

    def next_song(self):
        # Nút "Bài tiếp theo"
        self.current = self.current.next
        return "Đang phát: " + self.current.value

    def prev_song(self):
        # Nút "Bài trước"
        self.current = self.current.next
        return "Đang phát: " + self.current.value


if __name__ == "__main__":
    player = Player()
    for code in ["ZM001", "ZM002", "ZM003"]:
        player.add_last(code)
    print(player.play_first())
    print(player.next_song())
    print(player.prev_song())
    print(player.prev_song())
    print(player.next_song())
    print(player.next_song())
    print(player.next_song())
    print(player.next_song())
    print("Bài đang phát:", player.current.value)

    # Trình phát mới mở, chưa có bài và chưa phát bài nào
    new_player = Player()
    print(new_player.next_song())
    print(new_player.play_first())
