"""Nghiệp vụ thẻ thành viên Highlands Coffee: lịch sử hóa đơn của một hội viên.

Lịch sử là list số tiền các hóa đơn (đồng), cũ trước mới sau. Các hàm tính toán viết bằng ĐỆ QUY, không dùng vòng lặp.
"""

SAMPLE_BILLS = [45000, 120000, 59000, 35000, 210000, 65000]


def make_bills():
    """Có sẵn. Trả về bản sao lịch sử mẫu."""
    return SAMPLE_BILLS[:]


def money(amount):
    """Có sẵn. 120000 -> "120.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def total_points(bills):
    """Tổng điểm: mỗi hóa đơn được (số tiền // 10000) điểm. Đệ quy, không vòng lặp."""
    raise NotImplementedError


def count_big(bills, threshold):
    """Số hóa đơn có số tiền >= threshold. Đệ quy, không vòng lặp."""
    raise NotImplementedError


def largest(bills):
    """Hóa đơn lớn nhất; lịch sử rỗng trả None. Đệ quy, không vòng lặp, không dùng max()."""
    raise NotImplementedError


def add_bill(bills, amount_text):
    """Thêm hóa đơn vào cuối lịch sử, trả về số tiền. Lỗi (lịch sử giữ nguyên):
    "Số tiền phải là số nguyên từ 1.000 đến 5.000.000"."""
    raise NotImplementedError


def tier(points):
    """Có sẵn. Hạng thẻ theo điểm: dưới 50 "Thành viên", từ 50 "Bạc", từ 100 "Vàng", từ 200 "Kim cương"."""
    if points >= 200:
        return "Kim cương"
    if points >= 100:
        return "Vàng"
    if points >= 50:
        return "Bạc"
    return "Thành viên"
