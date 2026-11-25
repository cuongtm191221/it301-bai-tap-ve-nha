"""Nghiệp vụ hệ số giá cước theo nhu cầu của ứng dụng gọi xe Be.

counts là list số cuốc đặt trong từng phút, theo thời gian. Với cửa sổ k phút, "đỉnh" của phút i là số cuốc lớn nhất trong
các phút max(0, i-k+1) .. i (những phút đầu có cửa sổ ngắn hơn). Hệ số giá tính theo đỉnh.
"""
import timeit
from collections import deque


def check_window(k):
    """Có sẵn. k là số nguyên 1..1440, sai báo ValueError("Số phút phải từ 1 đến 1440")."""
    if type(k) is not int or not 1 <= k <= 1440:
        raise ValueError("Số phút phải từ 1 đến 1440")


def peaks_slow(counts, k):
    """Có sẵn. Bản cũ đang chạy, KHÔNG sửa. List đỉnh của từng phút với cửa sổ k."""
    check_window(k)
    peaks = []
    for i in range(len(counts)):
        peaks.append(max(counts[max(0, i - k + 1): i + 1]))
    return peaks


def peaks_fast(counts, k):
    """Cùng kết quả, cùng lỗi với peaks_slow; 200.000 phút, k = 1.000 trong 1 giây. Không gọi peaks_slow, không dùng max(),
    không cắt lát counts; không làm đổi counts."""
    raise NotImplementedError


def surge(peak):
    """Có sẵn. Hệ số giá: dưới 100 cuốc là 1.0, dưới 200 là 1.2, từ 200 là 1.5."""
    return 1.0 if peak < 100 else 1.2 if peak < 200 else 1.5


def make_counts():
    """Có sẵn. Số cuốc 15 phút mẫu."""
    return [40, 55, 120, 90, 60, 210, 180, 75, 70, 65, 130, 95, 100, 60, 50]


def make_big_counts(n):
    """Có sẵn. n phút giả lập."""
    return [(k * 7919) % 1000 for k in range(n)]


def record(counts, text):
    """Ghi số cuốc của phút mới vào cuối (số nguyên 0..10000, sai báo ValueError("Số cuốc phải là số nguyên từ 0 đến 10000")).
    Trả về số phút đã ghi."""
    raise NotImplementedError


def parse_window(text):
    """Đọc k từ chuỗi; không phải số nguyên hoặc ngoài khoảng báo ValueError("Số phút phải từ 1 đến 1440")."""
    raise NotImplementedError


def report(counts, k, last=10):
    """Tối đa last phút cuối: list (số thứ tự phút đếm từ 1, số cuốc, đỉnh, hệ số), tính bằng peaks_fast."""
    raise NotImplementedError


def benchmark(windows, n=20000):
    """Với từng k: đo (ms) peaks_slow và peaks_fast trên make_big_counts(n). Trả về list bộ (k, ms bản cũ, ms bản mới)."""
    raise NotImplementedError
