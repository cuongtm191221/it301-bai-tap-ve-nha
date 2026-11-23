"""Mục "Sản phẩm đã xem gần đây" trên ứng dụng Tiki, dùng deque có giới hạn."""


from collections import deque


class RecentlyViewed:
    """Giữ tối đa limit sản phẩm đã xem gần nhất, mới nhất trước; xem lại sản phẩm đã có thì đưa nó lên đầu."""

    def __init__(self, limit):
        if type(limit) is not int or limit < 1:
            raise ValueError("Giới hạn phải là số nguyên dương")
        self._items = deque(maxlen=limit)          # mới nhất ở bên trái

    def view(self, product):
        """Ghi nhận khách vừa xem product (mã đã bỏ khoảng trắng hai đầu và đổi sang chữ in hoa)."""
        raise NotImplementedError

    def items(self):
        """List mã sản phẩm, mới nhất trước."""
        raise NotImplementedError

    def set_limit(self, limit):
        """Đổi giới hạn; giới hạn nhỏ hơn thì chỉ giữ các sản phẩm mới nhất."""
        raise NotImplementedError

    def clear(self):
        """Xóa toàn bộ lịch sử xem."""
        raise NotImplementedError


if __name__ == "__main__":
    history = RecentlyViewed(3)
    for product in ("SP01", "sp02", " SP03 ", "SP04", "SP02", "   "):
        history.view(product)
        print(f"Xem {product!r:9} -> {history.items()}")
    history.set_limit(2)
    print("Giới hạn 2:", history.items())
    history.set_limit(5)
    history.view("SP09")
    print("Giới hạn 5, xem SP09:", history.items())
