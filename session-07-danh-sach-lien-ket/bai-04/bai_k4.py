"""K4 - Cài lại: danh sách liên kết đôi, thêm và xóa ở hai đầu, duyệt ngược."""


class DNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def to_text(self):
        """Cho sẵn, không sửa."""
        parts, current = [], self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " -> ".join(parts + ["None"])

    def add_first(self, value):
        """Thêm value vào đầu trong O(1); nối đủ cả next và prev; cập nhật size."""
        raise NotImplementedError

    def add_last(self, value):
        """Thêm value vào cuối trong O(1); nối đủ cả next và prev; cập nhật size."""
        raise NotImplementedError

    def remove_first(self):
        """Xóa node đầu, trả về giá trị. Rỗng: IndexError("danh sách rỗng, không có phần tử để xóa")."""
        raise NotImplementedError

    def remove_last(self):
        """Xóa node cuối trong O(1), trả về giá trị. Rỗng: IndexError("danh sách rỗng, không có phần tử để xóa")."""
        raise NotImplementedError

    def to_text_backward(self):
        """Trả về chuỗi các giá trị từ tail về head theo prev, dạng "V3 -> V2 -> V1 -> None"."""
        raise NotImplementedError
