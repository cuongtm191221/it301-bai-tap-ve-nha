"""Nghiệp vụ danh sách đơn giao trong ngày của bưu cục Giao Hàng Tiết Kiệm (GHTK).

Mỗi đơn là một list: [mã đơn, người nhận, quận, tiền thu hộ (đồng)].
"""

SAMPLE_ORDERS = [
    ["GH1001", "Nguyễn Văn An", "Cầu Giấy", 350000],
    ["GH1002", "Trần Thị Bình", "Đống Đa", 0],
    ["GH1003", "Lê Minh Châu", "Hà Đông", 1250000],
    ["GH1004", "Phạm Thu Dung", "Cầu Giấy", 89000],
    ["GH1005", "Hoàng Văn Em", "Thanh Xuân", 460000],
]


def make_orders():
    """Có sẵn. Trả về bản sao danh sách đơn mẫu (sửa bản sao không làm đổi SAMPLE_ORDERS)."""
    return [order[:] for order in SAMPLE_ORDERS]


def money(amount):
    """Có sẵn. 1250000 -> "1.250.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def format_order(order):
    """Có sẵn. Một dòng mô tả đơn: "GH1001 | Nguyễn Văn An | Cầu Giấy | 350.000đ"."""
    return f"{order[0]} | {order[1]} | {order[2]} | {money(order[3])}"


def total_cod(orders):
    """Trả về bộ (số đơn, tổng tiền thu hộ)."""
    raise NotImplementedError


def find_order(orders, code):
    """Tìm đơn theo mã (không phân biệt hoa thường, bỏ khoảng trắng hai đầu).
    Trả về bộ (đơn tìm thấy hoặc None, số lần so sánh mã)."""
    raise NotImplementedError


def add_order(orders, code, name, district, cod_text):
    """Thêm đơn vào cuối danh sách và trả về đơn mới. Dữ liệu sai báo ValueError (danh sách giữ nguyên):
    "Mã đơn không được để trống", "Mã đơn <MÃ> đã tồn tại", "Người nhận không được để trống",
    "Quận không được để trống", "Tiền thu hộ phải là số nguyên không âm"."""
    raise NotImplementedError


def count_by_district(orders, district):
    """Số đơn của một quận (không phân biệt hoa thường, bỏ khoảng trắng hai đầu)."""
    raise NotImplementedError
