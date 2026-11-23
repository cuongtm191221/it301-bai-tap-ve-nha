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

    def add_last(self, code):
        # Cho sẵn, đã đúng: thêm bài vào cuối danh sách
        node = Node(code)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def to_text(self):
        # Cho sẵn, đã đúng
        parts = []
        current = self.head
        while current is not None:
            parts.append(current.value)
            current = current.next
        return " -> ".join(parts + ["None"])

    def remove_first(self):
        # Phát xong bài đầu: lấy bài đầu ra khỏi danh sách và trả về mã bài
        code = self.head.value
        self.head = self.head.next
        return code

    def remove(self, code):
        # Người nghe bỏ một bài: xóa bài có mã code, trả True nếu xóa được
        prev = self.head
        while prev.next is not None:
            if prev.next.value == code:
                prev.next = prev.next.next
                self.size -= 1
                return True
            prev = prev.next
        return False


if __name__ == "__main__":
    playlist = Playlist()
    for code in ["ZM001", "ZM002", "ZM003"]:
        playlist.add_last(code)
    # Người nghe bỏ bài cuối, rồi thêm một bài mới
    print("Bỏ ZM003:", playlist.remove("ZM003"))
    playlist.add_last("ZM004")
    print("Danh sách phát:", playlist.to_text())
    # Người nghe bỏ bài đang đứng đầu
    print("Bỏ ZM001:", playlist.remove("ZM001"))
    print("Danh sách phát:", playlist.to_text())
    # Phát lần lượt cho tới hết danh sách
    print("Phát xong:", playlist.remove_first())
    print("Phát xong:", playlist.remove_first())
    print("Số bài còn lại:", playlist.size)
    print("Bài cuối danh sách:", playlist.tail)
    # Danh sách đã hết bài nhưng ứng dụng vẫn gọi phát tiếp
    playlist.remove_first()
