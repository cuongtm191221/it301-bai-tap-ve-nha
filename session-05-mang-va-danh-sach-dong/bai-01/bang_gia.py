"""Bảng giá cước GrabBike theo từng km."""
class FareTable:
    # Bảng giá cước GrabBike theo từng km: get(i) là giá của km thứ i + 1 (chỉ số từ 0).
    # Đặc tả: get, set với i ngoài 0 đến size() - 1 báo IndexError("Chỉ số ngoài phạm vi bảng giá");
    # set chỉ thay giá, không đổi số mức.
    def __init__(self, fares):
        self._data = list(fares)

    def _check(self, i):
        if i < 0 or i > self.size():
            raise IndexError("Chỉ số ngoài phạm vi bảng giá")

    def get(self, i):
        self._check(i)
        return self._data[i]

    def set(self, i, value):
        self._check(i)
        self._data.insert(i, value)

    def size(self):
        return len(self._data)

    def last(self):
        return self.get(self.size())


if __name__ == "__main__":
    table = FareTable([12000, 10000, 9000, 8000])
    print("Giá km đầu:", table.get(0))
    print("Số mức giá:", table.size())
    print("Giá mức cuối:", table.last())
    table.set(1, 11000)
    print("Sau khi sửa giá km thứ hai:", [table.get(i) for i in range(table.size())], "| số mức:", table.size())
    try:
        table.get(4)
    except IndexError as error:
        print("Đọc mức thứ năm:", error)
