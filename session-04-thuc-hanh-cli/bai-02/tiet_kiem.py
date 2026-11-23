"""Nghiệp vụ tính tiết kiệm tích lũy (lãi nhập gốc hằng tháng) của Techcombank.

Tiền tính bằng đồng (số nguyên). Lãi suất lưu bằng "điểm cơ bản" một năm: 6,5%/năm là 650.
Lãi một tháng = số dư * lãi suất // 120000 (làm tròn xuống). Các hàm tính toán viết bằng ĐỆ QUY, không dùng vòng lặp.
"""

MAX_MONTHS = 600


def money(amount):
    """Có sẵn. 100500000 -> "100.500.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def parse_money(text):
    """Có sẵn. Số tiền gửi: số nguyên từ 1.000.000 đến 10.000.000.000; sai báo ValueError."""
    text = text.strip()
    if not text.isdigit() or not 1000000 <= int(text) <= 10000000000:
        raise ValueError("Số tiền phải là số nguyên từ 1.000.000 đến 10.000.000.000")
    return int(text)


def parse_rate(text):
    """Có sẵn. "6,5" hoặc "6.5" -> 650 (điểm cơ bản); từ 0 đến 20, tối đa 2 chữ số thập phân; sai báo ValueError."""
    message = "Lãi suất phải từ 0 đến 20 (%/năm), tối đa 2 chữ số thập phân"
    text = text.strip().replace(",", ".")
    whole, _, frac = text.partition(".")
    if not whole.isdigit() or len(frac) > 2 or (frac and not frac.isdigit()):
        raise ValueError(message)
    value = int(whole) * 100 + int((frac + "00")[:2])
    if value > 2000:
        raise ValueError(message)
    return value


def balance_after(principal, rate_bp, months):
    """Số dư sau months tháng, lãi nhập gốc mỗi tháng. Đệ quy, không vòng lặp."""
    raise NotImplementedError


def months_to_reach(principal, rate_bp, target, months=0):
    """Số tháng ít nhất để số dư >= target (0 nếu đã đạt). Đệ quy, không vòng lặp.
    Lãi một tháng bằng 0 (không bao giờ tăng) báo ValueError("Số dư không tăng, không bao giờ đạt mục tiêu");
    cần hơn MAX_MONTHS tháng báo ValueError("Cần hơn 600 tháng để đạt mục tiêu")."""
    raise NotImplementedError


def yearly_table(principal, rate_bp, years):
    """List số dư cuối mỗi năm trong years năm (năm 1 trước). Đệ quy, không vòng lặp."""
    raise NotImplementedError
