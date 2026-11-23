"""Hàng đợi phiếu trả hàng của Tiki."""


class TwoStackQueue:
    # Hàng đợi phiếu trả hàng của Tiki, AI đề xuất cài bằng hai ngăn xếp (list):
    # _in nhận phiếu mới, _out để lấy phiếu ra.
    def __init__(self):
        self._in = []
        self._out = []

    def enqueue(self, ticket):
        self._in.append(ticket)

    def dequeue(self):
        # Đổ hết _in sang _out (đảo thứ tự) rồi lấy phiếu trên cùng của _out.
        while self._in:
            self._out.append(self._in.pop())
        if not self._out:
            raise IndexError("hàng đợi rỗng")
        return self._out.pop()

    def peek(self):
        if not self._out:
            raise IndexError("hàng đợi rỗng")
        return self._out[-1]

    def size(self):
        return len(self._in)


if __name__ == "__main__":
    q = TwoStackQueue()
    for t in ("TH01", "TH02", "TH03"):
        q.enqueue(t)
    print("Xử lý:", q.dequeue(), q.dequeue())
    print("Đầu hàng:", q.peek())
    print("Xử lý:", q.dequeue())
