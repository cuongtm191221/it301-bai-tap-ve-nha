"""Các lớp danh sách liên kết của Session 07, chép đúng từ bài đọc Lesson 02, 03, 04.

Dùng lại trong mọi bài tập về nhà: from lien_ket import Node, LinkedList, DNode, DoublyLinkedList
Không sửa tệp này.
"""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def count(self):
        total = 0
        current = self.head
        while current is not None:
            total += 1
            current = current.next
        return total

    def find(self, value):
        position = 0
        current = self.head
        while current is not None:
            if current.value == value:
                return position
            current = current.next
            position += 1
        return None

    def to_text(self):
        parts = []
        current = self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " -> ".join(parts + ["None"])

    def add_first(self, value):
        node = Node(value, self.head)
        self.head = node
        if self.tail is None:
            self.tail = node

    def add_last(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def remove_first(self):
        if self.head is None:
            raise IndexError("danh sách rỗng, không có phần tử để lấy")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return value

    def remove(self, value):
        if self.head is None:
            return False
        if self.head.value == value:
            self.remove_first()
            return True
        prev = self.head
        while prev.next is not None:
            if prev.next.value == value:
                if prev.next is self.tail:
                    self.tail = prev
                prev.next = prev.next.next
                return True
            prev = prev.next
        return False


class DNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_first(self, value):
        node = DNode(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def add_last(self, value):
        node = DNode(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

    def remove_first(self):
        if self.head is None:
            raise IndexError("danh sách rỗng, không có phần tử để xóa")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        return node.value

    def remove_last(self):
        if self.tail is None:
            raise IndexError("danh sách rỗng, không có phần tử để xóa")
        node = self.tail
        self.tail = node.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        return node.value

    def to_text(self):
        parts, current = [], self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " -> ".join(parts + ["None"])

    def to_text_backward(self):
        parts, current = [], self.tail
        while current is not None:
            parts.append(str(current.value))
            current = current.prev
        return " -> ".join(parts + ["None"])


def make_list(values):
    """Tạo LinkedList từ list Python bằng add_last (dùng trong test)."""
    lst = LinkedList()
    for v in values:
        lst.add_last(v)
    return lst


def make_dlist(values):
    """Tạo DoublyLinkedList từ list Python bằng add_last (dùng trong test)."""
    dl = DoublyLinkedList()
    for v in values:
        dl.add_last(v)
    return dl
