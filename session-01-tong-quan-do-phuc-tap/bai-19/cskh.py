"""Công cụ tra cứu bằng dòng lệnh cho bộ phận chăm sóc khách hàng của Shopee."""


def find_order(orders, code):
    """Trả về (vị trí tính từ 1 của đơn có mã code, số đơn đã xét); không có thì (None, số đơn đã xét) (xem đề, mục 2.1)."""
    raise NotImplementedError


def count_status(orders, status):
    """Trả về số đơn có trạng thái status, không phân biệt hoa thường (xem đề, mục 2.1)."""
    raise NotImplementedError


def orders_of(orders, buyer):
    """Trả về list mã đơn của khách buyer, theo thứ tự trong orders (xem đề, mục 2.1)."""
    raise NotImplementedError


def duplicate_codes(orders):
    """Trả về list các mã đơn xuất hiện từ hai lần trở lên, xếp tăng dần, mỗi mã một lần (xem đề, mục 2.1)."""
    raise NotImplementedError


def handle(orders, line):
    """Xử lý một dòng lệnh, trả về thông báo (xem đề, mục 2.2 và 3)."""
    raise NotImplementedError


if __name__ == "__main__":
    orders = [
        {"code": "DH1001", "buyer": "an.nguyen", "status": "Đang giao"},
        {"code": "DH1002", "buyer": "binh.tran", "status": "Đã giao"},
        {"code": "DH1003", "buyer": "an.nguyen", "status": "Chờ lấy hàng"},
        {"code": "DH1004", "buyer": "chi.le", "status": "Đang giao"},
        {"code": "DH1002", "buyer": "binh.tran", "status": "Đã giao"},
        {"code": "DH1005", "buyer": "an.nguyen", "status": "Đã hủy"},
    ]
    for line in ["TIM dh1004", "TIM DH9999", "  dem   đang giao ", "KHACH An.Nguyen", "KHACH dung.pham",
                 "TRUNG", "TIM", "XOA DH1001", ""]:
        print(">", line)
        print(handle(orders, line))
