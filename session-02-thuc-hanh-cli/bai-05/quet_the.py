"""Nghiệp vụ nhật ký quẹt thẻ ra vào tòa nhà văn phòng Viettel Tower.

Mỗi lượt quẹt là một list: [mã thẻ, giờ quẹt tính bằng phút từ 00:00]. Nhật ký xếp theo thời gian, cũ trước mới sau.
"""
import timeit

SAMPLE_LOGS = [
    ["VT1024", 470], ["VT2048", 475], ["VT1024", 485], ["VT3001", 490],
    ["VT2048", 520], ["VT1024", 720], ["VT3001", 725], ["VT4096", 810],
]


def make_logs():
    """Có sẵn. Trả về bản sao nhật ký mẫu."""
    return [log[:] for log in SAMPLE_LOGS]


def make_big_logs(n):
    """Có sẵn. Nhật ký giả lập n lượt (xếp theo thời gian) dùng để đo hiệu năng."""
    return [[f"VT{1000 + k % 500}", k * 1440 // n] for k in range(n)]


def to_text(minute):
    """Có sẵn. 485 -> "08:05"."""
    return f"{minute // 60:02d}:{minute % 60:02d}"


def parse_time(text):
    """Đổi "HH:MM" thành số phút từ 00:00. Sai dạng hoặc ngoài 00:00-23:59 báo
    ValueError("Giờ quẹt phải có dạng HH:MM từ 00:00 đến 23:59")."""
    raise NotImplementedError


def latest(logs, k):
    """List k lượt gần nhất, mới nhất trước (ít hơn k thì trả tất cả); không làm đổi logs."""
    raise NotImplementedError


def add_swipe(logs, card, time_text):
    """Ghi lượt quẹt vào cuối nhật ký, trả về lượt mới. Lỗi (nhật ký giữ nguyên):
    "Mã thẻ phải gồm VT và 4 chữ số", thông báo của parse_time,
    "Giờ quẹt không được sớm hơn lượt trước (<HH:MM>)"."""
    raise NotImplementedError


def count_card(logs, card):
    """Số lượt quẹt của một thẻ (không phân biệt hoa thường)."""
    raise NotImplementedError


def busiest_hour(logs):
    """(giờ đông nhất 0-23, số lượt trong giờ đó); bằng nhau lấy giờ sớm hơn; nhật ký rỗng trả (None, 0).
    Dùng một list 24 bộ đếm: bộ nhớ phụ không tăng theo số lượt."""
    raise NotImplementedError


def benchmark(sizes, number=10):
    """Đo bằng timeit trên make_big_logs(n) với từng n trong sizes. Trả về list bộ
    (n, ms một lần count_card(logs, "VT1000"), ms một lần busiest_hour(logs))."""
    raise NotImplementedError
