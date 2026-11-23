"""Hàng chờ yêu cầu đặt xe GrabCar tại sân bay."""
class RideQueue:
    # Hàng chờ yêu cầu đặt xe: ai đặt trước được phục vụ trước.
    # serve() trả mã yêu cầu được phục vụ, hàng rỗng trả None.
    # position(code) là số thứ tự trong hàng, đếm từ 1; không có trả None.
    # cancel(code) trả True nếu hủy được, False nếu không có mã đó.
    def __init__(self):
        self._items = []

    def join(self, code):
        self._items.append(code)

    def serve(self):
        return self._items.pop()

    def position(self, code):
        return self._items.index(code)

    def cancel(self, code):
        self._items.remove(code)
        return True

    def size(self):
        return len(self._items)


if __name__ == "__main__":
    q = RideQueue()
    for code in ("YC01", "YC02", "YC03", "YC04"):
        q.join(code)
    print("Phục vụ:", q.serve(), q.serve())
    print("Vị trí của YC04:", q.position("YC04"))
    print("Vị trí của YC09:", q.position("YC09"))
    print("Hủy YC03:", q.cancel("YC03"), "| hủy YC09:", q.cancel("YC09"))
    print("Phục vụ:", q.serve(), "| tiếp:", q.serve(), "| còn lại:", q.size())
