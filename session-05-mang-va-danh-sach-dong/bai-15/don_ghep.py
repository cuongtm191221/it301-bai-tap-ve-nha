"""Danh sách đơn của tài xế giao ghép GrabFood, lưu bằng mảng động tự cài."""


class OrderArray:
    # Mảng động tự cài (Lesson 04) lưu mã đơn GrabFood của một tài xế giao ghép.
    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._data = [None] * self._capacity
        self.moves = 0

    def __len__(self):
        return self._size

    def items(self):
        return [self._data[j] for j in range(self._size)]

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for j in range(self._size):
            new_data[j] = self._data[j]
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = value
        self._size += 1

    def pop(self, index):
        value = self._data[index]
        for j in range(index, self._size - 1):
            self._data[j] = self._data[j + 1]
            self.moves += 1
        self._size -= 1
        self._data[self._size] = None
        return value

    # ===== Phần do trợ lý AI viết thêm =====

    def extend(self, values):
        # Thêm mọi phần tử của values vào cuối.
        if self._size + len(values) > self._capacity:
            self._resize(2 * self._capacity)
        for value in values:
            self._data[self._size] = value
            self._size += 1

    def index_of(self, value):
        # Chỉ số của lần xuất hiện đầu tiên; không có thì báo ValueError.
        for j in range(self._size):
            if self._data[j] == value:
                return j
        return -1

    def remove_all(self, value):
        # Xóa mọi lần xuất hiện của value, trả về số phần tử đã xóa.
        removed = 0
        j = 0
        while j < self._size:
            if self._data[j] == value:
                self.pop(j)
                removed += 1
            j += 1
        return removed


if __name__ == "__main__":
    bag = OrderArray()
    bag.extend(["GF01", "GF02"])
    bag.append("GF03")
    print("Đơn đang giao:", bag.items())
    print("Vị trí GF02:", bag.index_of("GF02"))
    bag.append("GF02")
    print("Xóa GF02:", bag.remove_all("GF02"), "| còn:", bag.items())
