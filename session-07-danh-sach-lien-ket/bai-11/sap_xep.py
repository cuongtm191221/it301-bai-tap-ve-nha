"""Chỉnh sửa thứ tự danh sách phát: danh sách liên kết đơn, mỗi node giữ chuỗi "MÃ_BÀI - TÊN_BÀI"."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class EditablePlaylist:
    def __init__(self):
        self.head = None    # bài đầu danh sách phát
        self.tail = None    # bài cuối danh sách phát
        self.size = 0       # số bài

    def add_song(self, code, title):
        """Thêm một bài vào cuối danh sách phát. Trả về thông báo (xem đề, mục 2.1)."""
        raise NotImplementedError

    def insert_after(self, after_code, code, title):
        """Chèn một bài mới ngay sau bài có mã after_code. Trả về thông báo (xem đề, mục 2.2)."""
        raise NotImplementedError

    def move_to_top(self, code):
        """Đưa bài có mã code lên đầu danh sách phát. Trả về thông báo (xem đề, mục 2.3)."""
        raise NotImplementedError

    def to_lines(self):
        """Trả về list các dòng hiển thị danh sách phát (xem đề, mục 2.4)."""
        raise NotImplementedError


if __name__ == "__main__":
    playlist = EditablePlaylist()
    print(playlist.add_song("ZM001", "Bình minh trên phố"))
    print(playlist.add_song("  zm002 ", " Mưa đêm "))
    print(playlist.add_song("ZM003", "Đường về nhà"))
    print(playlist.insert_after("zm001", "ZM004", "Phố cũ"))
    print(playlist.insert_after("ZM999", "ZM005", "Gió qua thềm"))
    print(playlist.insert_after("ZM002", "zm004", "Phố cũ"))
    print(playlist.insert_after("ZM003", "ZM005", "Gió qua thềm"))
    print(playlist.add_song("ZM006", "Ngày nắng"))
    for line in playlist.to_lines():
        print(line)
    print(playlist.move_to_top("ZM001"))
    print(playlist.move_to_top("ZM999"))
    print(playlist.move_to_top("zm006"))
    print(playlist.add_song("ZM007", "Đêm thành phố"))
    for line in playlist.to_lines():
        print(line)
    print("Số bài:", playlist.size, "| bài cuối:", playlist.tail.value)
