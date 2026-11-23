"""Áp dụng giảm giá hàng loạt cho gian hàng trên Shopee."""


def discounted_price(price, percent):
    """Trả về giá sau khi giảm percent%: làm tròn xuống đến nghìn đồng, không thấp hơn 1.000đ (xem đề, mục 2.1)."""
    raise NotImplementedError


def apply_discount_in_place(prices, percent):
    """Giảm giá ngay trên list prices, không tạo list mới, không trả về gì (xem đề, mục 2.2)."""
    raise NotImplementedError


def discounted_copy(prices, percent):
    """Trả về list mới chứa giá sau giảm; list prices giữ nguyên (xem đề, mục 2.3)."""
    raise NotImplementedError


def total_after_discount(prices, percent):
    """Trả về tổng tiền nếu mua mỗi sản phẩm một cái sau khi giảm, không tạo list nào (xem đề, mục 2.4)."""
    raise NotImplementedError


if __name__ == "__main__":
    prices = [259000, 99000, 1490000, 1500]
    print("Giá 259.000đ giảm 15%:", discounted_price(259000, 15))
    preview = discounted_copy(prices, 15)
    print("Xem trước:", preview, "| giá gốc:", prices)
    print("Tổng nếu mua mỗi món một cái:", total_after_discount(prices, 15))
    print("Áp dụng tại chỗ trả về:", apply_discount_in_place(prices, 15))
    print("Giá sau khi áp dụng:", prices)
    print("Gian hàng trống:", discounted_copy([], 15), total_after_discount([], 15))
    try:
        discounted_copy(prices, 95)
    except ValueError as error:
        print("Giảm 95%:", error)
