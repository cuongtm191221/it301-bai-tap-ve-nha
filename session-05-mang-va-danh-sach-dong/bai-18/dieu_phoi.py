"""Bảng điều phối cuốc xe GrabCar của tổng đài: nhận lệnh dạng chữ."""


class DispatchQueue:
    """Hàng chờ cuốc xe: cuốc vào trước được giao trước. Lấy cuốc đầu hàng O(1) khấu hao, không dồn cả hàng mỗi lần."""

    def __init__(self):
        self._items = []

    def size(self):
        """Số cuốc đang chờ."""
        raise NotImplementedError

    def add(self, code):
        """Thêm cuốc vào cuối hàng; mã đã có trong hàng thì trả False, ngược lại True."""
        raise NotImplementedError

    def next(self):
        """Lấy cuốc đầu hàng; rỗng trả None."""
        raise NotImplementedError

    def cancel(self, code):
        """Hủy cuốc có mã code; trả True nếu hủy được."""
        raise NotImplementedError

    def view(self, k):
        """List tối đa k cuốc đầu hàng."""
        raise NotImplementedError


def handle(queue, line):
    """Xử lý một dòng lệnh của tổng đài viên, trả về dòng phản hồi."""
    raise NotImplementedError


if __name__ == "__main__":
    q = DispatchQueue()
    for line in ("ADD gc101", "add GC102", "ADD GC103", "ADD GC101", "  next  ", "VIEW 5", "CANCEL GC103",
                 "CANCEL GC999", "COUNT", "NEXT", "NEXT", "VIEW 0", "ADD", "PRINT", ""):
        print(f"{line!r:16} -> {handle(q, line)}")
    big = DispatchQueue()
    for k in range(200000):
        handle(big, f"ADD GC{k}")
        if big.size() > 50:
            handle(big, "NEXT")
    print(handle(big, "COUNT"), handle(big, "VIEW 2"))
