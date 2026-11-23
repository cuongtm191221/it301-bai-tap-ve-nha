"""Phát hiện danh sách phát bị lặp vòng: danh sách liên kết đơn, hàm chỉ nhận node đầu."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def build(values, loop_to=None):
    """Có sẵn: tạo danh sách từ một list chuỗi, trả về node đầu. Nếu có loop_to, node cuối trỏ về node ở vị trí loop_to (tính từ 0)."""
    nodes = [Node(value) for value in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if nodes and loop_to is not None:
        nodes[-1].next = nodes[loop_to]
    return nodes[0] if nodes else None


def has_loop_v1(head):
    """Giải pháp thứ nhất của bạn. Trả về True nếu danh sách bị lặp vòng, ngược lại False (xem đề, mục 2.1)."""
    raise NotImplementedError


def has_loop_v2(head):
    """Giải pháp thứ hai của bạn, khác cách làm với giải pháp thứ nhất. Trả về như mục 2.1."""
    raise NotImplementedError


def count_message(head):
    """Trả về thông báo đếm số bài, an toàn với danh sách bị lặp vòng (xem đề, mục 2.2)."""
    raise NotImplementedError


if __name__ == "__main__":
    codes = ["ZM001", "ZM002", "ZM003", "ZM004", "ZM005"]
    normal = build(codes)
    broken = build(codes, loop_to=2)
    circle = build(codes, loop_to=0)
    repeat = build(["ZM001", "ZM002", "ZM001", "ZM002"])
    for name, head in [("Bình thường", normal), ("Cuối trỏ về giữa", broken), ("Cuối trỏ về đầu", circle), ("Có bài lặp lại", repeat), ("Trống", None)]:
        print(name, "|", has_loop_v1(head), "|", has_loop_v2(head), "|", count_message(head))
