"""Hàng chờ phát nhạc: danh sách liên kết đơn, mỗi node giữ một chuỗi "MÃ_BÀI - TÊN_BÀI"."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class PlayQueue:
    def __init__(self):
        self.head = None    # bài sẽ phát tiếp theo
        self.tail = None    # bài cuối hàng chờ
        self.size = 0       # số bài đang chờ

    def add_song(self, code, title):
        """Thêm một bài vào cuối hàng chờ. Trả về thông báo (xem đề, mục 2.1)."""
        raise NotImplementedError

    def play_next(self):
        """Lấy bài ở đầu hàng chờ ra để phát. Trả về thông báo (xem đề, mục 2.2)."""
        raise NotImplementedError

    def remove_song(self, code):
        """Bỏ bài có mã code khỏi hàng chờ. Trả về thông báo (xem đề, mục 2.3)."""
        raise NotImplementedError

    def to_lines(self):
        """Trả về list các dòng hiển thị hàng chờ (xem đề, mục 2.4)."""
        raise NotImplementedError


if __name__ == "__main__":
    queue = PlayQueue()
    print(queue.add_song("ZM001", "Bình minh trên phố"))
    print(queue.add_song("  zm002 ", " Mưa đêm "))
    print(queue.add_song("ZM003", "Đường về nhà"))
    print(queue.add_song("zm001", "Bình minh trên phố"))
    print(queue.remove_song("ZM999"))
    print(queue.remove_song("zm003"))
    print(queue.add_song("ZM004", "Phố cũ"))
    for line in queue.to_lines():
        print(line)
    print("Số bài đang chờ:", queue.size)
    print(queue.play_next())
    print(queue.play_next())
    print(queue.play_next())
    print(queue.play_next())
    for line in queue.to_lines():
        print(line)
