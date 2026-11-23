"""Giỏ món GrabFood, lưu bằng mảng động tự cài."""
class Basket:
    # Giỏ món GrabFood, lưu bằng mảng động tự cài (Lesson 04). moves đếm tham chiếu đã dịch, checks đếm lượt so sánh.
    def __init__(self, items=()):
        self._capacity = max(1, len(items))
        self._size = 0
        self._data = [None] * self._capacity
        self.moves = self.checks = 0
        for item in items:
            self._data[self._size] = item
            self._size += 1

    def __len__(self):
        return self._size

    def items(self):
        return [self._data[j] for j in range(self._size)]

    def _normalize_index(self, index):
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("Chỉ số ngoài phạm vi phần tử")
        return index

    def pop(self, index=-1):
        # Lấy và xóa món tại index (mặc định món cuối), trả về món đó.
        index = self._normalize_index(index)
        value = self._data[index]
        for j in range(index, self._size - 1):
            self._data[j] = self._data[j + 1]
            self.moves += 1
        return value

    def remove(self, value):
        # Xóa lần xuất hiện đầu tiên của value; không có thì báo ValueError("không tìm thấy món").
        for j in range(self._size):
            self.checks += 1
            if self._data[j] == value:
                self.pop(j)


if __name__ == "__main__":
    basket = Basket(["Phở bò", "Trà đá", "Bánh mì", "Trà đá", "Chè"])
    print("Lấy món cuối:", basket.pop(), "| giỏ:", basket.items())
    print("Lấy món đầu:", basket.pop(0), "| giỏ:", basket.items())
    basket.remove("Trà đá")
    print("Bỏ một Trà đá:", basket.items(), "| số món:", len(basket))
    try:
        basket.remove("Cơm tấm")
    except ValueError as error:
        print("Bỏ Cơm tấm:", error)
