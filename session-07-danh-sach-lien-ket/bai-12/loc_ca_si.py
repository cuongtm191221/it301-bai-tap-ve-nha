"""Bỏ mọi bài của một ca sĩ khỏi danh sách phát: danh sách liên kết đơn, mỗi node giữ chuỗi "MÃ_BÀI - TÊN_BÀI - CA_SĨ"."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class ArtistPlaylist:
    def __init__(self):
        self.head = None    # bài đầu danh sách phát
        self.tail = None    # bài cuối danh sách phát
        self.size = 0       # số bài

    def add_song(self, code, title, artist):
        """Thêm một bài vào cuối danh sách phát. Trả về thông báo (xem đề, mục 2.1)."""
        raise NotImplementedError

    def count_by_artist(self, artist):
        """Trả về số bài của ca sĩ artist trong danh sách phát (xem đề, mục 2.2)."""
        raise NotImplementedError

    def remove_by_artist(self, artist):
        """Bỏ mọi bài của ca sĩ artist. Trả về thông báo (xem đề, mục 2.3)."""
        raise NotImplementedError

    def to_lines(self):
        """Trả về list các dòng hiển thị danh sách phát (xem đề, mục 2.4)."""
        raise NotImplementedError


if __name__ == "__main__":
    playlist = ArtistPlaylist()
    print(playlist.add_song("ZM001", "Bình minh trên phố", "Hoàng Lan"))
    print(playlist.add_song("  zm002 ", " Mưa đêm ", "  hoàng lan "))
    print(playlist.add_song("ZM003", "Đường về nhà", "Minh Khôi"))
    print(playlist.add_song("ZM004", "Phố cũ", "Hoàng Lan"))
    print(playlist.add_song("ZM005", "Gió qua thềm", "Thu An"))
    print(playlist.add_song("ZM006", "Ngày nắng", "Thu An"))
    print("Số bài của Hoàng Lan:", playlist.count_by_artist(" HOÀNG LAN "))
    print(playlist.remove_by_artist("hoàng lan"))
    for line in playlist.to_lines():
        print(line)
    print(playlist.remove_by_artist("Hoàng Lan"))
    print(playlist.remove_by_artist("Thu An"))
    print("Số bài:", playlist.size, "| bài cuối:", playlist.tail.value)
    print(playlist.add_song("ZM007", "Đêm thành phố", "Minh Khôi"))
    print(playlist.remove_by_artist("minh khôi"))
    for line in playlist.to_lines():
        print(line)
