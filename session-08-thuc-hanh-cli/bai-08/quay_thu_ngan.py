"""Nghiệp vụ gộp hàng chờ khi đóng quầy thu ngân ở siêu thị Co.opmart.

Khách lấy số thứ tự đến (số nguyên tăng dần) rồi vào quầy 1 hoặc 2; mỗi quầy là danh sách liên kết đơn có head, tail,
khách đứng theo số tăng dần. Đóng quầy 2 thì chuyển khách sang quầy 1, giữ thứ tự theo số.
Không dùng list Python để lưu hàng chờ.
"""
import timeit


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Lane:
    """Danh sách liên kết đơn có head, tail."""

    def __init__(self):
        self.head = None
        self.tail = None

    def add_last(self, value):
        """Có sẵn. Thêm value sau tail."""
        node = Node(value)
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node

    def remove_first(self):
        """Có sẵn. Lấy giá trị ở head; rỗng báo IndexError("danh sách rỗng, không có phần tử để lấy")."""
        if self.head is None:
            raise IndexError("danh sách rỗng, không có phần tử để lấy")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return value

    def to_text(self):
        """Có sẵn. Chuỗi dạng "101 -> 104 -> None"."""
        parts, current = [], self.head
        while current is not None:
            parts.append(str(current.value))
            current = current.next
        return " -> ".join(parts + ["None"])


class Store:
    """Có sẵn. Hai quầy và số thứ tự sẽ cấp tiếp theo."""

    def __init__(self):
        self.lanes = (Lane(), Lane())
        self.next_number = 101


def make_store():
    """Có sẵn. Siêu thị mẫu: số 101 đến 110 đã vào hai quầy."""
    store = Store()
    for number, lane in [(101, 0), (102, 1), (103, 1), (104, 0), (105, 0), (106, 1), (107, 1), (108, 1), (109, 0), (110, 1)]:
        store.lanes[lane].add_last(number)
    store.next_number = 111
    store.lanes[1].remove_first()                # khách 102 đã được phục vụ trước đó
    return store


def make_big_lanes(n):
    """Có sẵn. Hai quầy giả lập, mỗi quầy n khách: quầy 1 số chẵn, quầy 2 số lẻ."""
    a, b = Lane(), Lane()
    for k in range(n):
        a.add_last(2 * k)
        b.add_last(2 * k + 1)
    return a, b


def lane_index(text):
    """Có sẵn. "1" -> 0, "2" -> 1; sai báo ValueError("Quầy phải là 1 hoặc 2")."""
    text = text.strip()
    if text not in ("1", "2"):
        raise ValueError("Quầy phải là 1 hoặc 2")
    return int(text) - 1


def join(store, lane_text):
    """Cấp số tiếp theo cho khách vào quầy lane_text, trả về số đó."""
    raise NotImplementedError


def serve(store, lane_text):
    """Quầy lane_text phục vụ khách đầu hàng, trả về số; quầy trống báo ValueError("Quầy <k> không có khách")."""
    raise NotImplementedError


def merge_v1(a, b):
    """Giải pháp 1. Chuyển mọi node của b sang a để a tăng dần theo số; b thành rỗng; không tạo node mới, không dùng list;
    head, tail của cả hai đúng. Trả về số khách đã chuyển."""
    raise NotImplementedError


def merge_v2(a, b):
    """Giải pháp 2: cùng kết quả, cách làm khác, nhanh hơn rõ rệt; hai quầy 100.000 khách mỗi quầy trong 1 giây."""
    raise NotImplementedError


def benchmark(sizes, number=1):
    """Với từng n: đo (ms) mỗi giải pháp trên một cặp make_big_lanes(n) mới (thời gian tạo không tính). Trả về list bộ (n, ms 1, ms 2)."""
    raise NotImplementedError
