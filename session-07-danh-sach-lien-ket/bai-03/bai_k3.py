"""K3 - Cài lại: xóa ở đầu và xóa theo giá trị, có tail và size."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_last(self, value):
        """Cho sẵn, không sửa."""
        node = Node(value)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def to_text(self):
        """Cho sẵn, không sửa."""
        parts = []
        current = self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " -> ".join(parts + ["None"])

    def remove_first(self):
        """Xóa node đầu và trả về giá trị của nó, trong O(1).

        Danh sách rỗng: báo IndexError("danh sách rỗng, không có phần tử để lấy").
        Xóa node duy nhất thì head và tail đều là None.
        """
        raise NotImplementedError

    def remove(self, value):
        """Xóa node đầu tiên có giá trị value. Trả True nếu xóa được, False nếu không có.

        Xóa node cuối thì tail lùi về node đứng trước. size giảm đúng 1 khi xóa được.
        """
        raise NotImplementedError
