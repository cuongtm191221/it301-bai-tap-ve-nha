"""Lộ trình nhiều điểm dừng của GrabCar, lưu bằng mảng động tự cài."""
class Route:
    # Lộ trình GrabCar nhiều điểm dừng, lưu bằng mảng động tự cài (Lesson 04).
    # moves đếm số tham chiếu đã dịch khi chèn; copies đếm số tham chiếu đã chép khi mở rộng.
    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._data = [None] * self._capacity
        self.moves = self.copies = 0

    def __len__(self):
        return self._size

    def stops(self):
        return [self._data[j] for j in range(self._size)]

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for j in range(self._size):
            new_data[j] = self._data[j]
            self.copies += 1
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        # Chèn điểm dừng value để nó có chỉ số index; index âm tính từ cuối,
        # index nhỏ hơn -len thì chèn đầu, lớn hơn len thì chèn cuối (giống list.insert).
        if index > self._size:
            index = self._size
        for j in range(index, self._size):
            self._data[j + 1] = self._data[j]
            self.moves += 1
        self._data[index] = value
        self._size += 1


if __name__ == "__main__":
    route = Route()
    for stop in ("Đón khách", "Bến Thành", "Sân bay"):
        route.append(stop)
    route.insert(1, "Chợ Lớn")
    print("Chèn Chợ Lớn vào chỉ số 1:", route.stops(), "| dịch:", route.moves)
    route.insert(-1, "Quận 3")
    print("Chèn Quận 3 trước điểm cuối:", route.stops())
    route.insert(0, "Đổ xăng")
    print("Chèn Đổ xăng vào đầu:", route.stops())
    route.insert(99, "Về nhà")
    print("Chèn cuối:", route.stops(), "| số điểm:", len(route))
