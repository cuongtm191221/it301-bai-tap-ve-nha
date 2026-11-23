"""K2 - Cài lại: thêm ở đầu và ở cuối, có tail và size."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_first(self, value):
        """Thêm value vào đầu danh sách trong O(1). Cập nhật head, tail (khi rỗng) và size."""
        raise NotImplementedError

    def add_last(self, value):
        """Thêm value vào cuối danh sách trong O(1) nhờ tail. Cập nhật head (khi rỗng), tail và size."""
        raise NotImplementedError

    def to_text(self):
        """Cho sẵn, không sửa."""
        parts = []
        current = self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " -> ".join(parts + ["None"])
