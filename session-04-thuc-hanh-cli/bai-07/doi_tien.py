"""Nghiệp vụ quầy đổi tiền mới dịp Tết của Vietcombank chi nhánh Hoàn Kiếm.

Khách đổi một số tiền (bội của 10.000đ, tối đa 3.000.000đ) sang tiền mới các mệnh giá trong DENOMS.
"Một cách đổi" là một bộ số tờ của từng mệnh giá (không quan tâm thứ tự đưa tờ).
"""
import timeit

DENOMS = [500000, 200000, 100000, 50000, 20000, 10000]
MAX_AMOUNT = 3000000


def money(amount):
    """Có sẵn. 1500000 -> "1.500.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def parse_amount(text):
    """Có sẵn. Số tiền là số nguyên, bội của 10.000, từ 10.000 đến MAX_AMOUNT; sai báo ValueError."""
    text = text.strip()
    if not text.isdigit() or int(text) % 10000 or not 10000 <= int(text) <= MAX_AMOUNT:
        raise ValueError("Số tiền phải là bội của 10.000đ, từ 10.000đ đến 3.000.000đ")
    return int(text)


def count_ways_v1(amount, i=0):
    """Giải pháp 1. Số cách đổi amount bằng các mệnh giá DENOMS[i:]. Đệ quy."""
    raise NotImplementedError


def count_ways_v2(amount, i=0):
    """Giải pháp 2: cùng kết quả với giải pháp 1, cách làm khác và nhanh hơn rõ rệt; 3.000.000đ trong 1 giây."""
    raise NotImplementedError


def fewest_notes(amount, i=0):
    """Phương án ít tờ nhất: list bộ (mệnh giá, số tờ) theo mệnh giá giảm dần, bỏ mệnh giá 0 tờ.
    Lấy nhiều nhất có thể tờ mệnh giá lớn rồi đổi phần còn lại. Đệ quy trên các mệnh giá, không vòng lặp."""
    raise NotImplementedError


def benchmark(amounts, number=1):
    """Với từng số tiền: đo bằng timeit một lần count_ways_v1 và một lần count_ways_v2 (xóa cache trước nếu có).
    Trả về list bộ (số tiền, ms giải pháp 1, ms giải pháp 2)."""
    raise NotImplementedError
