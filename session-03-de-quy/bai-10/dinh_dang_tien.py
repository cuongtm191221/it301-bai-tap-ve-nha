"""Định dạng số tiền hiển thị trên biên lai chuyển tiền ví MoMo."""


def format_money(amount):
    """Chuỗi số tiền nguyên amount có dấu chấm ngăn cách hàng nghìn, ví dụ 1234567 thành "1.234.567"; số âm có dấu "-" ở đầu."""
    raise NotImplementedError


def receipt_line(name, amount):
    """Dòng biên lai: tên người nhận đã bỏ khoảng trắng thừa và số tiền kèm "đ"; tên trống ghi "Không rõ người nhận"."""
    raise NotImplementedError


if __name__ == "__main__":
    for amount in (0, 950, 1000, 1005, 45000, 1234567, 1000005, 2500000000):
        print(format_money(amount))
    print(format_money(-1500000))
    print(receipt_line("  Nguyễn   Văn An ", 1005000))
    print(receipt_line("   ", 20000))
