"""Chồng thùng hàng trên kệ kho Tiki, quản lý bằng ngăn xếp."""
class BoxStack:
    # Chồng thùng hàng ở một ô kệ kho Tiki: thùng đặt sau cùng nằm trên cùng, được lấy ra trước.
    # pop() lấy thùng trên cùng; peek() xem thùng trên cùng mà không lấy.
    # Chồng rỗng: pop() và peek() báo IndexError("ngăn xếp rỗng").
    def __init__(self):
        self._items = []

    def push(self, box):
        self._items.append(box)

    def pop(self):
        if self.is_empty():
            raise IndexError("ngăn xếp rỗng")
        return self._items.pop(0)

    def peek(self):
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


if __name__ == "__main__":
    shelf = BoxStack()
    for box in ("TH01", "TH02", "TH03"):
        shelf.push(box)
    print("Thùng trên cùng:", shelf.peek())
    print("Lấy ra:", shelf.pop(), "| còn", shelf.size(), "thùng, trên cùng:", shelf.peek())
    print("Lấy tiếp:", shelf.pop(), shelf.pop(), "| rỗng:", shelf.is_empty())
    try:
        shelf.peek()
    except IndexError as error:
        print("Xem chồng rỗng:", error)
