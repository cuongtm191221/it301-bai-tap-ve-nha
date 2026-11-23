"""Báo cáo tồn kho cuối ngày của gian hàng Shopee."""


def format_money(amount):
    """Có sẵn: viết số tiền theo kiểu Việt Nam, ví dụ 12340000 thành "12.340.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def is_valid(product):
    """Trả về True nếu sản phẩm hợp lệ: giá là số nguyên lớn hơn 0 (xem đề, mục 2.1)."""
    raise NotImplementedError


def inventory_summary(products):
    """Trả về dict tóm tắt tồn kho, duyệt list một lượt, bộ nhớ phụ O(1) (xem đề, mục 2.2)."""
    raise NotImplementedError


def restock_list(products, k):
    """Trả về list mã k sản phẩm hợp lệ có tồn kho thấp nhất (xem đề, mục 2.3)."""
    raise NotImplementedError


def summary_message(products):
    """Trả về thông báo cuối ngày cho người bán (xem đề, mục 2.4)."""
    raise NotImplementedError


if __name__ == "__main__":
    shop = [
        {"code": "SP01", "price": 259000, "stock": 12},
        {"code": "SP02", "price": 1490000, "stock": 3},
        {"code": "SP03", "price": 99000, "stock": 0},
        {"code": "SP04", "price": 99000, "stock": -2},
        {"code": "SP05", "price": 0, "stock": 40},
        {"code": "SP06", "price": 459000, "stock": 5},
    ]
    print(inventory_summary(shop))
    print(summary_message(shop))
    print("Cần nhập thêm (3 sản phẩm):", restock_list(shop, 3))
    print("Cần nhập thêm (10 sản phẩm):", restock_list(shop, 10))
    print("Thứ tự gốc giữ nguyên:", [p["code"] for p in shop])
    print(summary_message([{"code": "SP09", "price": -5, "stock": 1}]))
    print(summary_message([]))
