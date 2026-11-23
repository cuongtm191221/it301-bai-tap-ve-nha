"""Tra cứu giao dịch theo mã cho tổng đài chăm sóc khách hàng ví MoMo."""


def normalize(code):
    """Có sẵn. Chuẩn hóa mã giao dịch: bỏ khoảng trắng hai đầu, đổi sang chữ in hoa."""
    return code.strip().upper()


def find_transaction(codes, target, index=0):
    """Vị trí (bắt đầu từ 0) của giao dịch đầu tiên, tính từ vị trí index, có mã bằng target sau khi chuẩn hóa; không có thì -1."""
    raise NotImplementedError


def count_matches(codes, target, index=0):
    """Số giao dịch, tính từ vị trí index, có mã bằng target sau khi chuẩn hóa."""
    raise NotImplementedError


def search_message(codes, target):
    """Thông báo cho nhân viên tổng đài."""
    raise NotImplementedError


if __name__ == "__main__":
    codes = ["MM2401", " mm2402", "MM2403 ", "MM2402", "MM2405"]
    print(search_message(codes, "MM2403"))
    print(search_message(codes, "mm2405 "))
    print(search_message(codes, "MM2402"))
    print(search_message(codes, "MM9999"))
    print(search_message([], "MM2401"))
    print(search_message(codes, "   "))
