"""Đọc số tiền người dùng nhập ở ô "Số tiền chuyển" trên ví MoMo."""


DIGITS = "0123456789"


def digits_value(digits):
    """Giá trị số nguyên của chuỗi chỉ gồm chữ số, ví dụ "2024" thành 2024; chuỗi rỗng hoặc có ký tự khác chữ số trả về None."""
    raise NotImplementedError


def parse_amount(text):
    """Số tiền (số nguyên) từ chuỗi người dùng nhập, ví dụ " 1.234.567đ " thành 1234567; không hợp lệ trả về None."""
    raise NotImplementedError


def total_amounts(texts):
    """Bộ (tổng các số tiền hợp lệ, số dòng không hợp lệ) của list chuỗi texts."""
    raise NotImplementedError


if __name__ == "__main__":
    for text in ("50000", "1.234.567đ", " 20.000 đ ", "0", "1.23.456", "12a", "", ".500", "1.000."):
        print(repr(text), "->", parse_amount(text))
    print("Tổng hóa đơn chia nhóm:", total_amounts(["120.000đ", "85.500", "abc", "1.000.000đ"]))
