"""Phát hiện đơn đặt trùng (khách bấm "Đặt hàng" nhiều lần) trên Shopee."""


def count_duplicate_pairs(orders):
    # Đếm số cặp đơn trùng: hai đơn khác nhau, cùng người mua và cùng sản phẩm.
    # Trả về (số cặp trùng, số lần so sánh hai đơn).
    pairs = 0
    comparisons = 0
    n = len(orders)
    for i in range(n-1):
        for j in range(n - 1):
            comparisons += 1
            if orders[i]["buyer"] == orders[j]["buyer"] and orders[i]["product"] == orders[j]["product"]:
                pairs += 1
    return pairs, comparisons


# Big-O thời gian ghi trong tài liệu kỹ thuật của nhóm
COMPLEXITY = "O(n)"


if __name__ == "__main__":
    orders = [
        {"code": "DH3001", "buyer": "an.nguyen", "product": "SP01"},
        {"code": "DH3002", "buyer": "binh.tran", "product": "SP02"},
        {"code": "DH3003", "buyer": "an.nguyen", "product": "SP01"},
        {"code": "DH3004", "buyer": "chi.le", "product": "SP03"},
        {"code": "DH3005", "buyer": "binh.tran", "product": "SP02"},
    ]
    print("5 đơn trong ngày:", count_duplicate_pairs(orders))
    print("1 đơn:", count_duplicate_pairs(orders[:1]))
    triple = [{"code": "DH", "buyer": "dung.pham", "product": "SP09"}] * 3
    print("Bấm đặt 3 lần:", count_duplicate_pairs(triple))
    for n in [100, 1000]:
        many = [{"code": "DH", "buyer": f"khach{i}", "product": "SP01"} for i in range(n)]
        print(f"{n} đơn khác nhau:", count_duplicate_pairs(many)[1], "lần so sánh")
    print("Big-O ghi trong tài liệu:", COMPLEXITY)
