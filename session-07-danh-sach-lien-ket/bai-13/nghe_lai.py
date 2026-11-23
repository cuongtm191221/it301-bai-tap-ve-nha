"""Nghe lại bài cách đây k lượt: nhật ký nghe là danh sách liên kết đơn, chỉ có node đầu (bài nghe sớm nhất)."""


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def build_log(values):
    """Có sẵn: tạo nhật ký nghe từ một list chuỗi, trả về node đầu (None nếu list rỗng)."""
    head = None
    for value in reversed(values):
        head = Node(value, head)
    return head


def kth_from_end_v1(head, k):
    """Giải pháp thứ nhất của bạn. Trả về value của node thứ k tính từ cuối, hoặc None (xem đề, mục 2.1)."""
    raise NotImplementedError


def kth_from_end_v2(head, k):
    """Giải pháp thứ hai của bạn, khác cách làm với giải pháp thứ nhất. Trả về như mục 2.1."""
    raise NotImplementedError


def replay_message(head, k):
    """Trả về thông báo cho nút "Nghe lại" (xem đề, mục 2.2)."""
    raise NotImplementedError


if __name__ == "__main__":
    log = build_log([
        "ZM001 - Bình minh trên phố",
        "ZM002 - Mưa đêm",
        "ZM003 - Đường về nhà",
        "ZM002 - Mưa đêm",
        "ZM004 - Phố cũ",
    ])
    for k in [1, 2, 5, 6, 0]:
        print(replay_message(log, k))
    print(replay_message(None, 1))
    print("Giải pháp 1:", kth_from_end_v1(log, 3), "| Giải pháp 2:", kth_from_end_v2(log, 3))
