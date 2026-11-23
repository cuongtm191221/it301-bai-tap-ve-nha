"""Chồng phiếu xuất kho Tiki, cài ngăn xếp bằng chuỗi nút."""
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class SlipStack:
    # Chồng phiếu xuất kho Tiki, cài bằng chuỗi nút: phiếu in sau cùng nằm trên cùng (head).
    # Rỗng: pop() và peek() báo IndexError("ngăn xếp rỗng").
    def __init__(self):
        self.head = None
        self._size = 0

    def push(self, slip):
        self.head = Node(slip, self.head)
        self._size += 1

    def pop(self):
        if self.head is None:
            raise IndexError("ngăn xếp rỗng")
        value = self.head.value
        return value

    def peek(self):
        if self.head is None:
            return None
        return self.head.value

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size


if __name__ == "__main__":
    slips = SlipStack()
    for code in ("PX01", "PX02", "PX03"):
        slips.push(code)
    print("Xử lý:", slips.pop(), slips.pop(), "| còn", slips.size(), "phiếu, trên cùng:", slips.peek())
    print("Xử lý:", slips.pop(), "| rỗng:", slips.is_empty(), "| còn", slips.size(), "phiếu")
    try:
        print("Xem chồng rỗng:", slips.peek())
    except IndexError as error:
        print("Xem chồng rỗng:", error)
