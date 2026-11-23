"""K1 - Cài lại: duyệt danh sách liên kết đơn."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def count(self):
        """Trả về số node. Danh sách rỗng trả 0."""
        raise NotImplementedError

    def find(self, value):
        """Trả về vị trí (tính từ 0) của node đầu tiên có giá trị value; không có thì trả None."""
        raise NotImplementedError

    def get(self, position):
        """Trả về giá trị ở vị trí position (tính từ 0).

        position âm hoặc từ số node trở lên: báo IndexError("vị trí ngoài phạm vi").
        """
        raise NotImplementedError

    def to_text(self):
        """Trả về chuỗi dạng "KH1 -> KH2 -> None"; danh sách rỗng trả "None"."""
        raise NotImplementedError
