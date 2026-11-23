"""Lịch sử nghe nhạc: danh sách liên kết đôi, bài nghe cũ nhất ở head, mới nhất ở tail."""


class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class History:
    def __init__(self):
        self.head = None    # bài nghe cũ nhất
        self.tail = None    # bài nghe mới nhất
        self.size = 0       # số bài trong lịch sử

    def add_last(self, code):
        # Ghi bài vừa nghe vào cuối lịch sử
        node = Node(code)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def remove_first(self):
        # Bỏ bài nghe cũ nhất, trả về mã bài
        code = self.head.value
        self.head = self.head.next
        self.size -= 1
        return code

    def to_text(self):
        # Cho sẵn, đã đúng: từ cũ đến mới
        parts = []
        current = self.head
        while current is not None:
            parts.append(current.value)
            current = current.next
        return " -> ".join(parts + ["None"])

    def to_text_backward(self):
        # Cho sẵn, đã đúng: từ mới về cũ, đi theo prev
        parts = []
        current = self.tail
        while current is not None:
            parts.append(current.value)
            current = current.prev
        return " -> ".join(parts + ["None"])


if __name__ == "__main__":
    history = History()
    for code in ["ZM001", "ZM002", "ZM003", "ZM004"]:
        history.add_last(code)
    print("Từ cũ đến mới:", history.to_text())
    print("Từ mới về cũ:", history.to_text_backward())
    # Lịch sử chỉ giữ 3 bài gần nhất: bỏ bài cũ nhất
    print("Bỏ bài cũ nhất:", history.remove_first())
    print("Từ mới về cũ:", history.to_text_backward())
    print("Bài đứng trước bài cũ nhất:", history.head.prev)

    # Lịch sử chỉ có một bài rồi bị xóa hết
    single = History()
    single.add_last("ZM010")
    single.remove_first()
    print("Bài mới nhất sau khi xóa hết:", single.tail)
