"""Nút Quay lại và Tiến tới khi xem sản phẩm trên ứng dụng Tiki."""
class ProductBrowser:
    # Nút Quay lại / Tiến tới khi khách xem sản phẩm trên ứng dụng Tiki.
    # current() là trang đang xem. back(), forward() trả trang đang xem sau khi bấm;
    # không còn trang để quay lại / tiến tới thì giữ nguyên trang đang xem.
    def __init__(self, home):
        self._back = []
        self._forward = []
        self._current = home

    def current(self):
        return self._current

    def visit(self, page):
        self._back.append(self._current)
        self._current = page

    def back(self):
        self._forward.append(self._current)
        self._current = self._back.pop()
        return self._current

    def forward(self):
        if self._forward:
            self._current = self._forward.pop()
        return self._current


if __name__ == "__main__":
    b = ProductBrowser("Trang chủ")
    for page in ("Điện thoại", "iPhone 15", "Ốp lưng"):
        b.visit(page)
    print("Quay lại 2 lần:", b.back(), "->", b.back())
    print("Tiến tới:", b.forward())
    print("Quay lại:", b.back())
    b.visit("Sạc dự phòng")
    print("Mở trang mới rồi tiến tới:", b.forward())
    for _ in range(4):
        b.back()
    print("Quay lại 4 lần:", b.current())
