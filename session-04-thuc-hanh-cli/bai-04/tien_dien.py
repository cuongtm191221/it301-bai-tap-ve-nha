"""Nghiệp vụ tính tiền điện bậc thang cho một tổ dân phố, Điện lực EVN Hà Nội.

Mỗi hộ là một list: [mã khách hàng, tên chủ hộ, chỉ số cũ, chỉ số mới] (kWh). Điện tiêu thụ = chỉ số mới - chỉ số cũ.
Bảng giá bậc thang (minh họa, chưa gồm VAT) là list các bộ (số kWh của bậc, đơn giá đồng/kWh); bậc cuối có số kWh None (không giới hạn).
Các hàm tính toán viết bằng ĐỆ QUY, không dùng vòng lặp.
"""

TIERS = [(50, 1893), (50, 1956), (100, 2271), (100, 2860), (100, 3197), (None, 3302)]
SAMPLE_CUSTOMERS = [
    ["PE001", "Nguyễn Văn Hòa", 1200, 1430],
    ["PE002", "Trần Thị Lan", 880, 920],
    ["PE003", "Lê Minh Tâm", 5040, 5440],
    ["PE004", "Đỗ Khánh Vy", 300, 300],
]


def make_customers():
    """Có sẵn. Trả về bản sao danh sách hộ mẫu."""
    return [c[:] for c in SAMPLE_CUSTOMERS]


def money(amount):
    """Có sẵn. 505350 -> "505.350đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def usage(customer):
    """Có sẵn. Số kWh tiêu thụ của một hộ."""
    return customer[3] - customer[2]


def bill(kwh, tiers):
    """Tiền điện (đồng) của kwh kWh theo bảng tiers. Đệ quy trên các bậc, không vòng lặp."""
    raise NotImplementedError


def breakdown(kwh, tiers, level=1):
    """List bộ (bậc, số kWh, tiền) cho các bậc có dùng điện, bậc 1 trước. Đệ quy, không vòng lặp."""
    raise NotImplementedError


def total_bill(customers, tiers):
    """Tổng tiền điện của mọi hộ. Đệ quy trên list hộ, không vòng lặp."""
    raise NotImplementedError


def top_user(customers):
    """Hộ dùng nhiều kWh nhất; bằng nhau lấy hộ đứng trước; rỗng trả None. Đệ quy, không vòng lặp, không max()."""
    raise NotImplementedError


def update_reading(customers, code, reading_text):
    """Ghi chỉ số mới cho hộ có mã code, trả về hộ đó. Lỗi (dữ liệu giữ nguyên): "Không có khách hàng <MÃ>",
    "Chỉ số phải là số nguyên không âm", "Chỉ số mới không được nhỏ hơn chỉ số cũ (<cũ>)"."""
    raise NotImplementedError
