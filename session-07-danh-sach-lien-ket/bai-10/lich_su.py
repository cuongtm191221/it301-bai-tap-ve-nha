"""Lịch sử nghe gần đây: danh sách liên kết đôi, bài vừa nghe nằm ở đầu. Mỗi node giữ chuỗi "MÃ_BÀI - TÊN_BÀI"."""


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class RecentHistory:
    def __init__(self, limit=4):
        self.head = None      # bài vừa nghe gần nhất
        self.tail = None      # bài nghe lâu nhất
        self.size = 0         # số bài trong lịch sử
        self.limit = limit    # số bài tối đa được giữ

    def record(self, code, title):
        """Ghi nhận một lượt nghe. Trả về thông báo (xem đề, mục 2.1)."""
        raise NotImplementedError

    def remove_song(self, code):
        """Xóa một bài khỏi lịch sử. Trả về thông báo (xem đề, mục 2.2)."""
        raise NotImplementedError

    def to_lines(self):
        """Trả về list các dòng, bài vừa nghe gần nhất đứng trước (xem đề, mục 2.3)."""
        raise NotImplementedError

    def to_lines_oldest_first(self):
        """Trả về list các dòng, bài nghe lâu nhất đứng trước, đi từ tail theo prev (xem đề, mục 2.4)."""
        raise NotImplementedError


if __name__ == "__main__":
    history = RecentHistory(limit=4)
    print(history.record("ZM001", "Bình minh trên phố"))
    print(history.record("  zm002 ", " Mưa đêm "))
    print(history.record("ZM003", "Đường về nhà"))
    print(history.record("zm001", "Bình minh trên phố"))
    print(history.record("ZM001", "Bình minh trên phố"))
    print(history.record("ZM004", "Phố cũ"))
    print(history.record("ZM005", "Gió qua thềm"))
    for line in history.to_lines():
        print(line)
    print("Từ cũ đến mới:")
    for line in history.to_lines_oldest_first():
        print(line)
    print("Số bài trong lịch sử:", history.size)
    print(history.remove_song("ZM999"))
    print(history.remove_song("zm003"))
    print(history.remove_song("ZM005"))
    for line in history.to_lines():
        print(line)
    print("Bài cũ nhất:", history.tail.value)
