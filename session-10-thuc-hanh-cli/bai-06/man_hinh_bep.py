"""Nghiệp vụ màn hình bếp của nhà hàng Jollibee: chỉ hiện N đơn gần nhất.

Màn hình giữ đơn trong deque(maxlen=SCREEN_SIZE): thêm đơn mới khi đã đủ thì đơn cũ nhất tự rời màn hình.
Đơn là tuple (mã, món). Hàm đo so sánh ba cách giữ N phần tử gần nhất.
"""
import timeit
from collections import deque

SCREEN_SIZE = 6


class Board:
    """Có sẵn. Màn hình bếp: orders là deque(maxlen=SCREEN_SIZE), issued là số đơn đã cấp mã."""

    def __init__(self):
        self.orders = deque(maxlen=SCREEN_SIZE)
        self.issued = 0


def add_order(board, text):
    """Thêm đơn mới (món 1 đến 40 ký tự, bỏ khoảng trắng hai đầu; sai báo ValueError("Tên món phải có từ 1 đến 40 ký tự")).
    Mã "JB" + 3 chữ số. Trả về (đơn mới, đơn bị đẩy khỏi màn hình hoặc None)."""
    raise NotImplementedError


def make_board():
    """Có sẵn. Màn hình mẫu 5 đơn."""
    board = Board()
    for item in ["Gà giòn 2 miếng", "Mì Ý sốt bò", "Burger tôm", "Gà giòn 1 miếng", "Kem sundae"]:
        add_order(board, item)
    return board


def finish(board, text):
    """Bếp làm xong đơn có mã text (viết hoa, bỏ khoảng trắng): bỏ khỏi màn hình, trả về đơn.
    Không có trên màn hình báo ValueError("Đơn <mã> không có trên màn hình")."""
    raise NotImplementedError


def keep_last_del(n, m):
    """Có sẵn. Giữ n phần tử gần nhất trong list: thêm m số, đủ n thì del items[0]."""
    items = []
    for k in range(m):
        if len(items) == n:
            del items[0]
        items.append(k)
    return items


def keep_last_slice(n, m):
    """Có sẵn. Giữ n phần tử gần nhất trong list: thêm m số, mỗi lần cắt lấy n phần tử cuối."""
    items = []
    for k in range(m):
        items.append(k)
        items = items[-n:]
    return items


def keep_last_deque(n, m):
    """Giữ n phần tử gần nhất bằng deque(maxlen=n): thêm m số. Trả về deque."""
    raise NotImplementedError


def bench_window(sizes, m=20000):
    """Với từng n: đo (ms) ba hàm keep_last_* với cùng n, m. Trả về list bộ (n, ms del, ms cắt lát, ms deque)."""
    raise NotImplementedError
