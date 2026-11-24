"""Nghiệp vụ lọc người chơi minigame "Lắc xu" của Shopee.

Mỗi lượt tham gia ghi mã người dùng là số nguyên từ 0 đến MAX_ID (người dùng có thể lắc nhiều lần).
Danh sách lượt tham gia là list số nguyên theo thứ tự thời gian. Không dùng dict, set.
"""
import timeit

MAX_ID = 999999
SAMPLE = [100245, 532001, 100245, 777777, 532001, 100245, 3, 888120]


def make_turns():
    """Có sẵn. Trả về bản sao các lượt mẫu."""
    return SAMPLE[:]


def make_big_turns(n):
    """Có sẵn. n lượt giả lập, khoảng một nửa là người chơi lặp lại."""
    return [(k * 7919) % (n // 2 + 1) * 37 % (MAX_ID + 1) for k in range(n)]


def add_turn(turns, text):
    """Ghi một lượt; mã là số nguyên 0..MAX_ID (gõ đủ 6 chữ số hoặc ít hơn), sai báo ValueError("Mã người dùng phải là số từ 0 đến 999999")."""
    raise NotImplementedError


def unique_v1(turns):
    """Giải pháp 1. List mã người chơi, mỗi người một lần, theo thứ tự lượt đầu tiên của họ; không làm đổi turns."""
    raise NotImplementedError


def unique_v2(turns):
    """Giải pháp 2: cùng kết quả với giải pháp 1, cách làm khác, nhanh hơn rõ rệt; 300.000 lượt trong 1 giây. Không dùng dict, set."""
    raise NotImplementedError


def count_turns(turns, user):
    """Số lượt của một mã."""
    raise NotImplementedError


def benchmark(sizes, number=1):
    """Với từng n trong sizes, trên make_big_turns(n): đo bằng timeit một lần mỗi giải pháp (ms). Trả về list bộ (n, ms 1, ms 2)."""
    raise NotImplementedError
