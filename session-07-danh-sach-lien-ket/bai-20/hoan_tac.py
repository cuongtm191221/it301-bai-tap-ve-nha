"""Danh sách phát có nút Hoàn tác: danh sách liên kết đơn cho các bài, và một nhật ký thao tác do bạn tự thiết kế."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class UndoablePlaylist:
    def __init__(self, limit=3):
        self.head = None       # bài đầu danh sách phát
        self.tail = None       # bài cuối danh sách phát
        self.size = 0          # số bài
        self.limit = limit     # số thao tác gần nhất còn hoàn tác được
        # Thêm ở đây các thuộc tính cho nhật ký thao tác do bạn thiết kế

    def add_song(self, code, title):
        """Thêm một bài vào cuối danh sách phát. Trả về thông báo (xem đề, mục 2.1)."""
        raise NotImplementedError

    def remove_song(self, code):
        """Bỏ bài có mã code. Trả về thông báo (xem đề, mục 2.2)."""
        raise NotImplementedError

    def undo(self):
        """Hoàn tác thao tác gần nhất còn trong nhật ký. Trả về thông báo (xem đề, mục 2.3)."""
        raise NotImplementedError

    def to_lines(self):
        """Trả về list các dòng hiển thị danh sách phát (xem đề, mục 2.4)."""
        raise NotImplementedError


if __name__ == "__main__":
    playlist = UndoablePlaylist(limit=3)
    print(playlist.undo())
    print(playlist.add_song("ZM001", "Bình minh trên phố"))
    print(playlist.add_song("  zm002 ", " Mưa đêm "))
    print(playlist.add_song("ZM003", "Đường về nhà"))
    print(playlist.add_song("zm001", "Bình minh trên phố"))
    print(playlist.remove_song("ZM999"))
    print(playlist.remove_song("zm001"))
    print(playlist.undo())
    for line in playlist.to_lines():
        print(line)
    print(playlist.undo())
    print(playlist.add_song("ZM004", "Phố cũ"))
    print(playlist.remove_song("ZM004"))
    print(playlist.undo())
    print(playlist.undo())
    print(playlist.undo())
    print(playlist.undo())
    for line in playlist.to_lines():
        print(line)
    print("Số bài:", playlist.size, "| bài cuối:", playlist.tail.value)
