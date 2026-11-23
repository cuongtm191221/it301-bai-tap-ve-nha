"""Bảng giá cước GrabCar theo vùng, viết theo đặc tả ADT."""


def money(amount):
    """Có sẵn. Số tiền có dấu chấm ngăn cách hàng nghìn, ví dụ 12000 thành "12.000"."""
    return f"{amount:,}".replace(",", ".")


class ZoneFares:
    """Bảng giá theo vùng: vùng có chỉ số i (từ 0) có giá get(i)."""

    def __init__(self, fares):
        for value in fares:
            if not _valid_fare(value):
                raise ValueError("Giá phải là số nguyên dương")
        self._data = list(fares)              # bản sao: list của người gọi đổi sau đó không ảnh hưởng

    def size(self):
        """Số vùng đang có giá."""
        raise NotImplementedError

    def get(self, i):
        """Giá của vùng i; i âm tính từ cuối."""
        raise NotImplementedError

    def set(self, i, value):
        """Thay giá vùng i bằng value; số vùng giữ nguyên."""
        raise NotImplementedError

    def surge(self, percent):
        """Bảng giá MỚI sau khi tăng percent phần trăm, làm tròn xuống tới 1.000đ; bảng hiện tại giữ nguyên."""
        raise NotImplementedError


def report(board):
    """Một dòng mô tả bảng giá, chỉ dùng size() và get()."""
    raise NotImplementedError


if __name__ == "__main__":
    board = ZoneFares([25000, 32000, 41000])
    print(report(board))
    print("Vùng cuối:", board.get(-1))
    board.set(1, 33000)
    print("Giờ cao điểm +15%:", report(board.surge(15)))
    print("Bảng gốc giữ nguyên:", report(board))
    for bad in (3, "1", True):
        try:
            board.get(bad)
        except (IndexError, TypeError) as error:
            print(f"get({bad!r}):", type(error).__name__, "-", error)
    try:
        board.set(0, 0)
    except ValueError as error:
        print("set(0, 0):", error)
    print(report(ZoneFares([])))
