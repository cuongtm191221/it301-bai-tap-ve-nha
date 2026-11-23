"""Nghiệp vụ thưởng chuỗi ngày mua hàng của khách thân thiết Bách Hóa Xanh.

Lịch sử là list các ngày mua (số nguyên: số thứ tự ngày, date.toordinal()), tăng dần, không trùng.
Một "chuỗi" là các ngày mua liên tiếp nhau (ngày sau = ngày trước + 1). Mỗi ngày mua được điểm bằng độ dài chuỗi
tính đến ngày đó, tối đa 7 điểm.
"""
import timeit
from datetime import date

SAMPLE_DAYS = [date(2026, 11, d).toordinal() for d in (1, 2, 3, 5, 6, 10, 11, 12, 13)]


def make_days():
    """Có sẵn. Trả về bản sao lịch sử mẫu."""
    return SAMPLE_DAYS[:]


def make_big_days(n):
    """Có sẵn. Lịch sử giả lập n ngày mua."""
    start = date(2020, 1, 1).toordinal()
    return [start + k + k // 9 for k in range(n)]


def to_text(day):
    """Có sẵn. Số thứ tự ngày -> "2026-11-13"."""
    return date.fromordinal(day).isoformat()


def report_slow(days):
    """Có sẵn. Bản cũ đang chạy, KHÔNG sửa. Trả về (chuỗi dài nhất, chuỗi hiện tại kết thúc ở ngày cuối, tổng điểm);
    lịch sử rỗng trả (0, 0, 0)."""
    if not days:
        return 0, 0, 0
    longest, _, points = report_slow(days[:-1])
    current = _streak_end(days)
    return max(longest, current), current, points + min(current, 7)


def report_fast(days):
    """Cùng kết quả với report_slow; một lượt duyệt; 100.000 ngày trong 1 giây, không RecursionError.
    Không gọi report_slow, không đổi giới hạn đệ quy, không làm đổi days."""
    raise NotImplementedError


def add_day(days, text):
    """Ghi ngày mua "YYYY-MM-DD" vào cuối lịch sử, trả về số thứ tự ngày. Lỗi (lịch sử giữ nguyên):
    "Ngày phải có dạng YYYY-MM-DD", "Ngày mua phải sau ngày mua gần nhất (<YYYY-MM-DD>)"."""
    raise NotImplementedError


def benchmark(sizes, number=3):
    """Với từng n trong sizes, trên make_big_days(n): đo bằng timeit một lần report_slow và report_fast (ms).
    Trả về list bộ (n, ms bản cũ, ms bản mới)."""
    raise NotImplementedError


def slow_fails(n):
    """True nếu report_slow trên make_big_days(n) gặp RecursionError."""
    raise NotImplementedError
