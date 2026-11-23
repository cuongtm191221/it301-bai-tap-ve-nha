"""Hàng chờ đóng gói ở kho Tiki, cài hàng đợi bằng chuỗi nút."""
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class PackingQueue:
    # Hàng chờ đóng gói ở kho Tiki, cài bằng chuỗi nút: đơn vào ở tail, ra ở head.
    # Rỗng: dequeue() và peek() báo IndexError("hàng đợi rỗng").
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, order):
        node = Node(order)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
        self._size += 1

    def dequeue(self):
        if self.head is None:
            raise IndexError("hàng đợi rỗng")
        value = self.head.value
        self.head = self.head.next
        self._size -= 1
        return value

    def peek(self):
        if self.head is None:
            raise IndexError("hàng đợi rỗng")
        return self.tail.value

    def size(self):
        return self._size


if __name__ == "__main__":
    q = PackingQueue()
    for code in ("TK101", "TK102", "TK103"):
        q.enqueue(code)
    print("Đầu hàng:", q.peek(), "| số đơn:", q.size())
    print("Đóng gói:", q.dequeue(), q.dequeue(), q.dequeue())
    q.enqueue("TK104")
    q.enqueue("TK105")
    print("Sau khi hàng rỗng, thêm 2 đơn:", q.dequeue(), q.dequeue(), "| còn:", q.size())
