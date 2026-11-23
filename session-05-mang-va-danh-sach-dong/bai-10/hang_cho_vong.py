"""Hàng chờ đơn GrabFood tại bếp trung tâm, cố định số chỗ."""


class KitchenQueue:
    """Hàng chờ đơn có tối đa capacity đơn; đơn vào trước được nấu trước."""

    def __init__(self, capacity):
        if type(capacity) is not int or capacity < 1:
            raise ValueError("Sức chứa phải là số nguyên dương")
        self._data = [None] * capacity        # vùng lưu trữ cố định, không thêm bớt ô

    def size(self):
        """Số đơn đang chờ."""
        raise NotImplementedError

    def is_full(self):
        """True nếu đã đủ capacity đơn."""
        raise NotImplementedError

    def enqueue(self, code):
        """Thêm đơn vào cuối hàng; trả True, hoặc False nếu hàng đã đầy."""
        raise NotImplementedError

    def dequeue(self):
        """Lấy và xóa đơn đứng đầu; hàng rỗng trả None. O(1), không dịch phần tử."""
        raise NotImplementedError

    def peek(self):
        """Đơn đứng đầu mà không xóa; rỗng trả None."""
        raise NotImplementedError

    def to_list(self):
        """List các đơn từ đầu hàng tới cuối hàng."""
        raise NotImplementedError


if __name__ == "__main__":
    q = KitchenQueue(3)
    print("Thêm 4 đơn:", [q.enqueue(c) for c in ("GF1", "GF2", "GF3", "GF4")])
    print("Nấu:", q.dequeue(), "| đầu hàng:", q.peek(), "| hàng:", q.to_list())
    print("Thêm GF5:", q.enqueue("GF5"), "| hàng:", q.to_list(), "| đầy:", q.is_full())
    print("Nấu hết:", [q.dequeue() for _ in range(4)], "| còn:", q.size())
    big = KitchenQueue(50)
    served = 0
    for k in range(200000):
        big.enqueue(f"GF{k}")
        if big.size() > 40:
            big.dequeue()
            served += 1
    print("200.000 đơn, đã nấu:", served, "| đang chờ:", big.size(), "| đầu hàng:", big.peek())
