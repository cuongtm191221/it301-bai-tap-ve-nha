"""Đối soát danh sách đơn giữa hệ thống Shopee và đơn vị vận chuyển."""


def normalize_code(code):
    """Có sẵn: chuẩn hóa mã đơn (bỏ khoảng trắng hai đầu, chữ hoa)."""
    return code.strip().upper()


def same_orders_v1(ours, carrier):
    """Giải pháp thứ nhất của bạn. Trả về True nếu hai list có cùng các mã đơn, mỗi mã cùng số lần, không kể thứ tự (xem đề, mục 2.1)."""
    raise NotImplementedError


def same_orders_v2(ours, carrier):
    """Giải pháp thứ hai của bạn, khác cách làm với giải pháp thứ nhất. Trả về như mục 2.1."""
    raise NotImplementedError


def reconcile_message(ours, carrier):
    """Trả về thông báo đối soát, dùng giải pháp bạn chọn (xem đề, mục 2.2)."""
    raise NotImplementedError


if __name__ == "__main__":
    ours = ["DH9001", "DH9002", "DH9003", "DH9004", "DH9005"]
    carrier = ["DH9003", " dh9001", "DH9005", "DH9002", "DH9004 "]
    print("Ngày 11/11:", same_orders_v1(ours, carrier), same_orders_v2(ours, carrier), "|", reconcile_message(ours, carrier))
    print("Thiếu một đơn:", reconcile_message(ours, carrier[:4]))
    twice = ["DH9001", "DH9001", "DH9002"]
    print("Trùng số lần khác nhau:", same_orders_v1(twice, ["DH9001", "DH9002", "DH9002"]), same_orders_v2(twice, ["DH9001", "DH9002", "DH9002"]))
    print("Sai một mã:", reconcile_message(ours, ["DH9003", "DH9001", "DH9005", "DH9002", "DH9006"]))
    print("Hai bên chưa có đơn:", reconcile_message([], []))
    print("List của đơn vị vận chuyển giữ nguyên:", carrier)
