"""Phiên nghe có nút lùi và tiến: danh sách liên kết đôi, con trỏ current chỉ bài đang phát."""


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class ListeningSession:
    def __init__(self):
        self.head = None       # bài đầu tiên của phiên nghe
        self.tail = None       # bài cuối cùng còn giữ trong phiên nghe
        self.current = None    # bài đang phát
        self.size = 0          # số bài đang giữ

    def play(self, code, title):
        """Phát một bài mới ngay sau bài đang phát. Trả về thông báo (xem đề, mục 2.1)."""
        raise NotImplementedError

    def back(self):
        """Lùi về bài đã nghe trước đó. Trả về thông báo (xem đề, mục 2.2)."""
        raise NotImplementedError

    def forward(self):
        """Tiến tới bài đã nghe sau đó. Trả về thông báo (xem đề, mục 2.3)."""
        raise NotImplementedError

    def to_lines(self):
        """Trả về list các dòng của phiên nghe, bài đang phát có dấu ">" ở đầu (xem đề, mục 2.4)."""
        raise NotImplementedError


if __name__ == "__main__":
    session = ListeningSession()
    print(session.back())
    print(session.play("ZM001", "Bình minh trên phố"))
    print(session.play("  zm002 ", " Mưa đêm "))
    print(session.play("ZM003", "Đường về nhà"))
    print(session.play("zm003", "Đường về nhà"))
    print(session.forward())
    print(session.back())
    print(session.back())
    print(session.back())
    print(session.forward())
    for line in session.to_lines():
        print(line)
    print(session.play("ZM004", "Phố cũ"))
    print(session.forward())
    for line in session.to_lines():
        print(line)
    print("Số bài đang giữ:", session.size, "| bài cuối:", session.tail.value)
