"""Hàng chờ của phòng nghe chung: danh sách liên kết đơn, yêu cầu của tài khoản VIP đứng trước yêu cầu thường."""


class Node:
    def __init__(self, value, vip=False):
        self.value = value    # chuỗi "MÃ_BÀI - TÊN_BÀI"
        self.vip = vip        # True nếu là yêu cầu của tài khoản VIP
        self.next = None


class RoomQueue:
    def __init__(self):
        self.head = None    # bài sẽ phát tiếp theo
        self.tail = None    # bài cuối hàng chờ
        self.size = 0       # số bài đang chờ

    def add_request(self, code, title, vip=False):
        """Nhận một yêu cầu phát bài. Trả về thông báo (xem đề, mục 2.1)."""
        raise NotImplementedError

    def play_next(self):
        """Lấy bài ở đầu hàng chờ ra để phát. Trả về thông báo (xem đề, mục 2.2)."""
        raise NotImplementedError

    def cancel(self, code):
        """Hủy yêu cầu phát bài có mã code. Trả về thông báo (xem đề, mục 2.3)."""
        raise NotImplementedError

    def to_lines(self):
        """Trả về list các dòng hiển thị hàng chờ (xem đề, mục 2.4)."""
        raise NotImplementedError


if __name__ == "__main__":
    room = RoomQueue()
    print(room.add_request("ZM001", "Bình minh trên phố"))
    print(room.add_request("  zm002 ", " Mưa đêm "))
    print(room.add_request("ZM003", "Đường về nhà", vip=True))
    print(room.add_request("ZM004", "Phố cũ", vip=True))
    print(room.add_request("zm001", "Bình minh trên phố", vip=True))
    print(room.add_request("ZM005", "Gió qua thềm"))
    for line in room.to_lines():
        print(line)
    print(room.cancel("ZM999"))
    print(room.cancel("zm004"))
    print(room.add_request("ZM006", "Ngày nắng", vip=True))
    for line in room.to_lines():
        print(line)
    print("Số bài đang chờ:", room.size, "| bài cuối:", room.tail.value)
    print(room.play_next())
    print(room.play_next())
    print(room.add_request("ZM008", "Sau cơn mưa", vip=True))
    print("Bài đầu:", room.head.value)
