"""Băng chuyền đóng gói ở kho Tiki: hàng đợi cài bằng list đổi đầu cuối."""
class PackingLine:
    # Băng chuyền đóng gói ở kho Tiki: đơn vào trước được đóng gói trước.
    # Bản cài bằng list: thêm đơn ở đầu list, lấy đơn ở cuối list.
    # peek() là đơn sẽ được đóng gói tiếp theo; take_batch(k) lấy tối đa k đơn theo thứ tự;
    # rỗng thì peek() trả None, take_batch trả list rỗng.
    def __init__(self):
        self._items = []

    def enqueue(self, order):
        self._items.insert(0, order)

    def dequeue(self):
        if not self._items:
            return None
        return self._items.pop()

    def peek(self):
        if not self._items:
            return None
        return self._items[0]

    def take_batch(self, k):
        batch = []
        for _ in range(k):
            batch.append(self._items.pop())
        return batch

    def size(self):
        return len(self._items)


if __name__ == "__main__":
    line = PackingLine()
    for code in ("TK201", "TK202", "TK203", "TK204"):
        line.enqueue(code)
    print("Đơn tiếp theo:", line.peek())
    print("Lô 3 đơn:", line.take_batch(3))
    print("Lô 3 đơn tiếp:", line.take_batch(3), "| còn:", line.size())
    big = PackingLine()
    for k in range(200000):
        big.enqueue(f"TK{k}")
    print("200.000 đơn, đơn tiếp theo:", big.peek(), "| lô 2 đơn:", big.take_batch(2))
