"""Nghiệp vụ bảng thông báo đơn hàng của ứng dụng Tiki.

Thông báo mới nhất đứng đầu. Bảng thông báo là danh sách liên kết đơn có head và size. Không dùng list Python để lưu bảng.
Các hàm đo so sánh với list Python bằng timeit.
"""
import timeit


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class NoticeFeed:
    """Danh sách liên kết đơn có head và size."""

    def __init__(self):
        self.head = None
        self.size = 0

    def add_first(self, value):
        """Thêm value trước head, tăng size."""
        raise NotImplementedError

    def get(self, index):
        """Giá trị ở chỉ số index (0 là head); ngoài 0..size-1 báo IndexError("Chỉ số ngoài phạm vi")."""
        raise NotImplementedError


def make_feed():
    """Có sẵn. Bảng mẫu: thêm lần lượt 5 thông báo, thông báo thêm sau cùng đứng đầu."""
    feed = NoticeFeed()
    for text in ["TK1001 đã xác nhận", "TK1001 đang giao", "TK1002 đã xác nhận", "TK1001 đã giao", "TK1003 đã xác nhận"]:
        feed.add_first(text)
    return feed


def push(feed, text):
    """Thêm thông báo mới (bỏ khoảng trắng hai đầu, 1 đến 60 ký tự, sai báo ValueError("Thông báo phải có từ 1 đến 60 ký tự")).
    Trả về nội dung đã thêm."""
    raise NotImplementedError


def parse_count(text, low, high, message):
    """Có sẵn. Số nguyên trong [low, high], sai báo ValueError(message)."""
    text = text.strip()
    if not text.isdigit() or not low <= int(text) <= high:
        raise ValueError(message)
    return int(text)


def latest(feed, k_text):
    """k thông báo mới nhất (k là số nguyên dương; k lớn hơn size thì lấy tất cả) dưới dạng list, duyệt một lần từ head.
    k sai báo ValueError("Số thông báo phải là số nguyên dương")."""
    raise NotImplementedError


def notice_at(feed, i_text):
    """Thông báo thứ i (đếm từ 1, mới nhất là 1); ngoài 1..size báo ValueError("Thứ tự phải từ 1 đến <size>")."""
    raise NotImplementedError


def bench_front(sizes, number=1):
    """Với từng n: thời gian (ms) thêm n thông báo vào đầu một list rỗng bằng insert(0, ...) và vào một NoticeFeed rỗng.
    Trả về list bộ (n, ms list, ms danh sách liên kết)."""
    raise NotImplementedError


def bench_index(sizes, probes=200, number=1):
    """Với từng n: dựng list và NoticeFeed n phần tử (không tính giờ), rồi đo (ms) đọc probes vị trí rải đều 0..n-1
    bằng items[i] và bằng feed.get(i). Trả về list bộ (n, ms list, ms danh sách liên kết)."""
    raise NotImplementedError
