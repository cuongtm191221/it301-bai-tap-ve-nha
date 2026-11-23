"""Tính giá khuyến mãi theo công thức hậu tố của bộ phận marketing Tiki."""


def money(amount):
    """Có sẵn. Số tiền có dấu chấm ngăn cách hàng nghìn, ví dụ 225000 thành "225.000"."""
    sign = "-" if amount < 0 else ""
    return sign + f"{abs(amount):,}".replace(",", ".")


OPS = "+-*/"


def evaluate(formula):
    """Giá trị số nguyên của công thức hậu tố; công thức sai báo ValueError với thông báo đúng đặc tả."""
    raise NotImplementedError


def price_message(formula):
    """Dòng hiển thị cho người duyệt khuyến mãi."""
    raise NotImplementedError


if __name__ == "__main__":
    for formula in ("120000 2 * 15000 -", "500000 500000 10 * 100 / -", "  99000   ",
                    "120000 * 2", "120000 2 3 *", "100000 0 /", "120000 2 x", "", "5000 8000 -"):
        print(f"{formula!r:32} -> {price_message(formula)}")
