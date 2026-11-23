"""Báo cáo khách hàng thân thiết của gian hàng Shopee. Hàm loyal_customers do trợ lý AI viết."""


def loyal_customers(buyers, min_orders):
    """Trả về list mã khách có từ min_orders đơn trở lên, xếp tăng dần theo mã."""
    # Duyệt từng đơn, đếm số đơn của khách đó, thêm vào kết quả nếu đủ điều kiện.
    # Độ phức tạp: O(n), bộ nhớ phụ O(1).
    result = []
    for b in buyers:
        if buyers.count(b) > min_orders and b not in result:
            result.append(b)
    return result


def loyal_customers_fast(buyers, min_orders):
    """Giải pháp thứ hai do bạn đề xuất: cùng kết quả với loyal_customers nhưng nhanh hơn khi danh sách dài."""
    raise NotImplementedError


if __name__ == "__main__":
    # Đoạn chạy thử: đổi dãy mã khách và ngưỡng dưới đây để thử các bộ dữ liệu của bạn
    buyers = ["KH01", "KH02", "KH01", "KH03", "KH01"]
    min_orders = 2
    print("Danh sách đơn:", buyers)
    print(f"Khách có từ {min_orders} đơn:", loyal_customers(buyers, min_orders))
