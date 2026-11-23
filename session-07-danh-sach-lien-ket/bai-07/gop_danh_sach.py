"""Tính năng "Thêm tất cả vào danh sách phát của tôi": gộp một danh sách phát vào danh sách khác."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Playlist:
    def __init__(self):
        self.head = None    # bài sẽ phát đầu tiên
        self.tail = None    # bài cuối danh sách
        self.size = 0       # số bài trong danh sách

    def add_first(self, value):
        # Cho sẵn, đã đúng
        node = Node(value, self.head)
        self.head = node
        if self.tail is None:
            self.tail = node
        self.size += 1

    def add_last(self, value):
        # Cho sẵn, đã đúng
        node = Node(value)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def find(self, value):
        # Cho sẵn, đã đúng: vị trí của value, không có thì None
        position = 0
        current = self.head
        while current is not None:
            if current.value == value:
                return position
            current = current.next
            position += 1
        return None

    def to_text(self):
        # Cho sẵn, đã đúng
        parts = []
        current = self.head
        while current is not None:
            parts.append(current.value)
            current = current.next
        return " -> ".join(parts + ["None"])


def append_all(target, source):
    # Chép các bài của source vào cuối target, bỏ qua bài target đã có. Trả về số bài đã thêm.
    target.tail.next = source.head
    target.size += source.size
    return source.size


if __name__ == "__main__":
    mine = Playlist()
    for code in ["ZM001", "ZM002", "ZM003"]:
        mine.add_last(code)
    shared = Playlist()
    for code in ["ZM003", "ZM004", "ZM005"]:
        shared.add_last(code)

    print("Số bài đã thêm:", append_all(mine, shared))
    print("Danh sách của tôi:", mine.to_text())
    print("Số bài:", mine.size, "| bài cuối:", mine.tail.value)

    # Bạn bè thêm một bài vào danh sách của họ: danh sách của tôi không được đổi theo
    shared.add_last("ZM006")
    print("Danh sách của bạn:", shared.to_text())
    print("Danh sách của tôi:", mine.to_text())

    # Danh sách mới tạo nhận bài từ danh sách của bạn
    new_list = Playlist()
    print("Số bài đã thêm vào danh sách mới:", append_all(new_list, shared))
    print("Danh sách mới:", new_list.to_text())
