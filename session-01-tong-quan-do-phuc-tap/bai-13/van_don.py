"""Kiểm tra mã vận đơn trùng trước khi in nhãn giao hàng trên Shopee."""


def normalize_code(code):
    """Có sẵn: chuẩn hóa mã vận đơn (bỏ khoảng trắng hai đầu, chữ hoa)."""
    return code.strip().upper()


def has_duplicate_v1(codes):
    """Giải pháp thứ nhất của bạn. Trả về True nếu có hai mã trùng nhau sau khi chuẩn hóa (xem đề, mục 2.1)."""
    raise NotImplementedError


def has_duplicate_v2(codes):
    """Giải pháp thứ hai của bạn, khác cách làm với giải pháp thứ nhất. Trả về như mục 2.1."""
    raise NotImplementedError


def print_check_message(codes):
    """Trả về thông báo trước khi in, dùng giải pháp bạn chọn ở phần phân tích (xem đề, mục 2.2)."""
    raise NotImplementedError


if __name__ == "__main__":
    batch = ["SPX0001", "SPX0002", "SPX0003", "SPX0004", "SPX0005"]
    print("Lô 5 vận đơn:", has_duplicate_v1(batch), has_duplicate_v2(batch), "|", print_check_message(batch))
    typed = ["SPX0001", " spx0002", "SPX0003", "SPX0002 "]
    print("Lô nhập tay:", has_duplicate_v1(typed), has_duplicate_v2(typed), "|", print_check_message(typed))
    ends = ["SPX0009", "SPX0001", "SPX0002", "SPX0009"]
    print("Trùng ở hai đầu:", has_duplicate_v1(ends), has_duplicate_v2(ends))
    print("Lô sau khi kiểm tra:", ends)
    print("Lô 1 vận đơn:", print_check_message(["SPX0001"]))
    print("Lô rỗng:", print_check_message([]))
