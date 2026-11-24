"""Nghiệp vụ theo dõi giá đóng cửa một mã cổ phiếu trên ứng dụng SSI iBoard (dùng để học phân tích dữ liệu, không phải khuyến nghị đầu tư).

Giá đóng cửa các phiên lưu trong list số nguyên (đồng), phiên cũ trước, phiên mới sau; phiên đánh số từ 1.
"""
import sys
import timeit

SAMPLE = [97500, 98200, 96800, 95400, 99100, 101300, 100200, 102800, 101900, 103500]


def make_prices():
    """Có sẵn. Trả về bản sao giá 10 phiên mẫu của mã FPT."""
    return SAMPLE[:]


def make_big_prices(n):
    """Có sẵn. Giá giả lập n phiên."""
    return [50000 + (k * 7919) % 30000 for k in range(n)]


def money(amount):
    """Có sẵn. 103500 -> "103.500đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def add_price(prices, text):
    """Thêm giá phiên mới vào cuối, trả về số phiên. Giá phải là số nguyên từ 1.000 đến 10.000.000, sai báo
    ValueError("Giá phải là số nguyên từ 1.000 đến 10.000.000")."""
    raise NotImplementedError


def recent_average(prices, k):
    """(list k giá gần nhất theo thứ tự phiên, giá trung bình làm tròn xuống); k lớn hơn số phiên thì lấy tất cả; rỗng trả ([], None)."""
    raise NotImplementedError


def best_trade(prices):
    """Mua một lần rồi bán ở một phiên SAU đó: bộ (phiên mua, phiên bán, lãi) với lãi lớn nhất (phiên đánh số từ 1).
    Nhiều cách cùng lãi thì chọn phiên bán sớm nhất, rồi phiên mua sớm nhất. Không có cách nào lãi (> 0) trả None.
    Một lượt duyệt, bộ nhớ phụ O(1)."""
    raise NotImplementedError


def benchmark(sizes, number=5):
    """Với từng n trong sizes, trên make_big_prices(n): đo bằng timeit một lần best_trade (ms) và lấy sys.getsizeof của list giá.
    Trả về list bộ (n, ms, byte)."""
    raise NotImplementedError
