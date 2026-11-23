"""Bộ đệm điểm GPS của tài xế Grab, lưu bằng mảng động tự cài."""
class DynamicArray:
    # Mảng động tự cài (Lesson 04): _data là vùng lưu trữ có _capacity ô, chỉ _size ô đầu là phần tử thật.
    # copies đếm số tham chiếu đã chép khi mở rộng.
    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._data = [None] * self._capacity
        self.copies = 0

    def __len__(self):
        return self._capacity

    def _normalize_index(self, index):
        if index < 0:
            index += self._size
        if not 0 <= index < self._capacity:
            raise IndexError("Chỉ số ngoài phạm vi phần tử")
        return index

    def __getitem__(self, index):
        return self._data[self._normalize_index(index)]

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for j in range(self._size):
            new_data[j] = self._data[j]
            self.copies += 1
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        if self._size == self._capacity:
            self._resize(self._capacity + 2)
        self._data[self._size] = value
        self._size += 1


if __name__ == "__main__":
    points = DynamicArray()
    for k in range(6):
        points.append(f"GPS{k + 1}")
    print("Số điểm GPS:", len(points))
    print("Điểm cuối:", points[-1])
    try:
        print("Điểm thứ 7:", points[6])
    except IndexError as error:
        print("Điểm thứ 7:", error)
    track = DynamicArray()
    for k in range(10000):
        track.append(k)
    print("10.000 điểm, số tham chiếu đã chép:", track.copies)
