"""Bảng xếp hạng sản phẩm bán chạy của gian hàng Shopee."""


def top_k_v1(sales, k):
    """Giải pháp thứ nhất của bạn. Trả về list k bộ (mã, số lượng bán) bán chạy nhất (xem đề, mục 2.1)."""
    raise NotImplementedError


def top_k_v2(sales, k):
    """Giải pháp thứ hai của bạn, khác cách làm với giải pháp thứ nhất. Trả về như mục 2.1."""
    raise NotImplementedError


def top_message(sales, k):
    """Trả về thông báo bảng xếp hạng, dùng giải pháp bạn chọn (xem đề, mục 2.2)."""
    raise NotImplementedError


if __name__ == "__main__":
    sales = [
        {"code": "SP01", "sold": 95},
        {"code": "SP02", "sold": 40},
        {"code": "SP03", "sold": 120},
        {"code": "SP04", "sold": 7},
        {"code": "SP05", "sold": 95},
        {"code": "SP06", "sold": 60},
    ]
    print("Top 3 (cách 1):", top_k_v1(sales, 3))
    print("Top 3 (cách 2):", top_k_v2(sales, 3))
    print(top_message(sales, 3))
    print(top_message(sales, 10))
    print(top_message(sales, 0))
    print(top_message([], 3))
    print("Thứ tự gốc giữ nguyên:", [s["code"] for s in sales])
