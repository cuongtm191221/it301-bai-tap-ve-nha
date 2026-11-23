"""Mảng động có mở rộng và thu gọn cho bộ đệm cuốc xe của tài xế Grab."""


class ShrinkArray:
    """Mảng động: đầy thì gấp đôi; sau khi lấy ra, còn dùng không quá 1/4 số ô thì giảm một nửa số ô."""

    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._data = [None] * self._capacity
        self.copies = 0                        # số tham chiếu đã chép khi đổi vùng lưu trữ

    def size(self):
        """Số phần tử đang lưu."""
        raise NotImplementedError

    def capacity(self):
        """Số ô của vùng lưu trữ hiện tại."""
        raise NotImplementedError

    def get(self, i):
        """Phần tử tại chỉ số i (0 đến size() - 1, i âm tính từ cuối); sai báo IndexError("Chỉ số ngoài phạm vi phần tử")."""
        raise NotImplementedError

    def append(self, value):
        """Thêm vào cuối; đầy thì gấp đôi số ô."""
        raise NotImplementedError

    def pop(self):
        """Lấy và xóa phần tử cuối; rỗng báo IndexError("Mảng rỗng"). Sau khi lấy, nếu size <= capacity // 4 và capacity > 1 thì giảm còn một nửa số ô."""
        raise NotImplementedError

    def items(self):
        """List các phần tử theo thứ tự."""
        raise NotImplementedError


if __name__ == "__main__":
    buffer = ShrinkArray()
    for k in range(9):
        buffer.append(f"CX{k + 1}")
    print("Sau 9 lần thêm:", buffer.size(), "phần tử,", buffer.capacity(), "ô")
    for _ in range(7):
        buffer.pop()
    print("Sau 7 lần lấy:", buffer.items(), "|", buffer.capacity(), "ô")
    buffer.reset = buffer.copies
    for _ in range(1000):
        buffer.append("CX")
        buffer.pop()
    print("1.000 lần thêm rồi lấy ở ngưỡng, số tham chiếu chép thêm:", buffer.copies - buffer.reset)
    try:
        ShrinkArray().pop()
    except IndexError as error:
        print("Lấy từ mảng rỗng:", error)
