"""Nghiệp vụ tính số cách xếp pallet lên dãy kệ của kho Vinamilk Bình Dương.

Một dãy kệ dài n mét (n >= 1) được lấp kín bằng pallet loại 1 mét và loại 2 mét, xếp nối nhau theo thứ tự.
Số cách xếp: ways(1) = 1, ways(2) = 2, ways(n) = ways(n - 1) + ways(n - 2)
(pallet đầu tiên dài 1 mét hoặc 2 mét, phần còn lại xếp tiếp).
"""
import timeit
from functools import lru_cache

CACHED_SAFE = 400


def ways_naive(n):
    """Số cách xếp, đệ quy trực tiếp theo công thức (không nhớ kết quả). Không vòng lặp."""
    raise NotImplementedError


def count_calls(n):
    """Số lần ways_naive được gọi (kể cả lời gọi đầu tiên) khi tính ways_naive(n). Đệ quy, không vòng lặp,
    không chạy ways_naive."""
    raise NotImplementedError


@lru_cache(maxsize=None)
def ways_cached(n):
    """Số cách xếp, đệ quy có lru_cache: mỗi n chỉ tính một lần."""
    raise NotImplementedError


def ways_loop(n):
    """Số cách xếp, viết bằng vòng lặp (dùng cho dãy kệ dài)."""
    raise NotImplementedError


def ways(n):
    """Dùng ways_cached khi n <= CACHED_SAFE, ngược lại dùng ways_loop. Trả về bộ (số cách, "lru_cache" hoặc "vòng lặp")."""
    raise NotImplementedError


def layouts(n):
    """List mọi cách xếp dạng chuỗi, ví dụ n = 3: ["1+1+1", "1+2", "2+1"] (cách bắt đầu bằng 1 trước). Đệ quy."""
    raise NotImplementedError


def parse_length(text, high):
    """Có sẵn. Chiều dài là số nguyên từ 1 đến high; sai báo ValueError."""
    text = text.strip()
    if not text.isdigit() or not 1 <= int(text) <= high:
        raise ValueError(f"Chiều dài phải là số nguyên từ 1 đến {high} mét")
    return int(text)


def benchmark(sizes, number=1):
    """Với từng n trong sizes: đo bằng timeit một lần ways_naive(n) và một lần ways_cached(n) (xóa cache trước mỗi lần đo).
    Trả về list bộ (n, ms không nhớ, ms lru_cache)."""
    raise NotImplementedError
