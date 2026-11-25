"""Nghiệp vụ công thức giá khuyến mãi dạng hậu tố trên Haravan.

Công thức viết dạng hậu tố (toán tử đứng sau hai toán hạng, không cần ngoặc), các phần cách nhau bằng khoảng trắng:
số nguyên không âm, biến gia (giá gốc), toán tử + - * / (/ là chia lấy phần nguyên //).
Ví dụ "gia 90 * 100 /" là giảm 10%; "gia 20000 -" là giảm 20.000đ.
"""
import timeit

OPS = ("+", "-", "*", "/")
INVALID = "Biểu thức không hợp lệ"
DIV_ZERO = "Không chia được cho 0"


def to_tokens(text, price):
    """Có sẵn. Tách công thức thành list: số (int) hoặc toán tử (str); gia thay bằng price. Phần lạ hoặc công thức trống báo
    ValueError(INVALID)."""
    parts = text.split()
    if not parts:
        raise ValueError(INVALID)
    tokens = []
    for part in parts:
        if part == "gia":
            tokens.append(price)
        elif part.isdigit():
            tokens.append(int(part))
        elif part in OPS:
            tokens.append(part)
        else:
            raise ValueError(INVALID)
    return tokens


def apply(op, a, b):
    """Có sẵn. a op b; chia cho 0 báo ValueError(DIV_ZERO)."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if b == 0:
        raise ValueError(DIV_ZERO)
    return a // b


def eval_v1(text, price):
    """Giải pháp 1. Giá trị công thức với gia = price. Lỗi: ValueError(INVALID) khi phần lạ, thiếu toán hạng, thừa toán hạng;
    ValueError(DIV_ZERO) khi chia cho 0 (xét theo thứ tự tính từ trái sang phải). Không làm đổi gì ngoài biến cục bộ."""
    raise NotImplementedError


def eval_v2(text, price):
    """Giải pháp 2: cùng kết quả, cùng lỗi, cách làm khác, nhanh hơn rõ rệt; công thức 200.001 phần trong 1 giây."""
    raise NotImplementedError


class Shop:
    """Có sẵn. Sản phẩm (mã, tên, giá gốc) và công thức đang áp dụng."""

    def __init__(self):
        self.products = [("SP01", "Áo thun", 250000), ("SP02", "Quần jean", 480000), ("SP03", "Mũ lưỡi trai", 120000)]
        self.formula = "gia"


def money(value):
    """Có sẵn. 225000 -> "225.000đ"."""
    return ("-" if value < 0 else "") + f"{abs(value):,}".replace(",", ".") + "đ"


def set_formula(shop, text):
    """Đổi công thức (bỏ khoảng trắng thừa): phải tính được (eval_v2) cho mọi sản phẩm và không ra giá âm, không thì báo lỗi của
    eval_v2 hoặc ValueError("Giá sau khuyến mãi của <mã> bị âm") (sản phẩm đầu tiên bị âm) và giữ công thức cũ. Trả về công thức."""
    raise NotImplementedError


def promo_prices(shop):
    """List (mã, tên, giá gốc, giá khuyến mãi) theo công thức hiện tại."""
    raise NotImplementedError


def benchmark(sizes):
    """Với từng n: công thức "gia" + n lần " 1 +"; đo (ms) eval_v1 và eval_v2 với giá 100. Trả về list bộ (n, ms 1, ms 2)."""
    raise NotImplementedError
