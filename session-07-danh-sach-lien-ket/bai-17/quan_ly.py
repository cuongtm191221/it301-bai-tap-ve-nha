"""Trình quản lý danh sách phát bằng dòng lệnh: danh sách liên kết đơn, mỗi node giữ chuỗi "MÃ_BÀI - TÊN_BÀI"."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Playlist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def find(self, code):
        """Trả về vị trí (tính từ 1) của bài có mã code, hoặc 0 nếu không có."""
        raise NotImplementedError

    def value_at(self, position):
        """Trả về chuỗi của bài ở vị trí position (tính từ 1), hoặc None nếu không có."""
        raise NotImplementedError

    def add_first(self, code, title):
        """Thêm bài vào đầu danh sách phát."""
        raise NotImplementedError

    def add_last(self, code, title):
        """Thêm bài vào cuối danh sách phát."""
        raise NotImplementedError

    def remove(self, code):
        """Bỏ bài có mã code. Trả về chuỗi của bài đã bỏ, hoặc None nếu không có."""
        raise NotImplementedError

    def to_lines(self):
        """Trả về list các dòng "1. MÃ - TÊN" theo thứ tự phát (list rỗng nếu chưa có bài)."""
        raise NotImplementedError



def handle(playlist, line):
    """Xử lý một dòng lệnh của người dùng trên playlist. Trả về thông báo (xem đề, mục 2 và 3)."""
    raise NotImplementedError


def main():
    """Có sẵn: vòng lặp nhận lệnh từ bàn phím. Gõ THOAT để kết thúc."""
    playlist = Playlist()
    print("Trình quản lý danh sách phát. Các lệnh: THEM, DAU, BO, TIM, XEM, DEM, THOAT")
    while True:
        line = input("> ")
        if line.strip().upper() == "THOAT":
            print("Tạm biệt.")
            break
        print(handle(playlist, line))


def demo():
    """Có sẵn: chạy kịch bản mẫu của đề, không cần nhập tay."""
    playlist = Playlist()
    script = [
        "THEM ZM001 | Bình minh trên phố",
        "  them   zm002 |  Mưa đêm  ",
        "DAU ZM003 | Đường về nhà",
        "THEM ZM001 | Bình minh trên phố",
        "THEM ZM004",
        "THEM M4 | Phố cũ",
        "PHAT ZM001",
        "",
        "TIM zm002",
        "BO ZM002",
        "THEM ZM004 | Phố cũ",
        "XEM",
        "DEM",
    ]
    for line in script:
        print(">", line)
        print(handle(playlist, line))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        main()
