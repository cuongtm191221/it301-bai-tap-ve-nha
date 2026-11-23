"""Báo cáo doanh thu cuối ngày của gian hàng trên Shopee, có đếm số bước."""

# Quy ước đếm: mỗi dòng lệnh được thực hiện là một bước (như bài đọc Lesson 02).


def total_revenue(orders):
    # Tổng tiền các đơn; trả về (tổng tiền, số bước)
    steps = 0
    total = 0
    for order in orders:
        total += order["amount"]
    steps += 1
    return total, steps


def count_big_orders(orders, threshold):
    # Đếm đơn có giá trị từ threshold trở lên; trả về (số đơn, số bước)
    steps = 1            # count = 0
    count = 0
    for order in orders:
        if order["amount"] > threshold:
            count += 1
            steps += 1
    steps += 1           # return
    return count, steps


# Big-O thời gian của hai hàm, ghi trong tài liệu kỹ thuật của nhóm
COMPLEXITY = {
    "total_revenue": "O(n + 2)",
    "count_big_orders": "O(2n + 2)",
}


if __name__ == "__main__":
    orders = [
        {"code": "DH2001", "amount": 120000},
        {"code": "DH2002", "amount": 560000},
        {"code": "DH2003", "amount": 500000},
        {"code": "DH2004", "amount": 89000},
        {"code": "DH2005", "amount": 1250000},
    ]
    print("Tổng doanh thu:", total_revenue(orders))
    print("Đơn từ 500.000đ:", count_big_orders(orders, 500000))

    small = [{"code": "DH", "amount": 100000}] * 1000
    big = [{"code": "DH", "amount": 600000}] * 1000
    print("1.000 đơn, tổng doanh thu:", total_revenue(small)[1], "bước")
    print("1.000 đơn nhỏ, đếm đơn lớn:", count_big_orders(small, 500000)[1], "bước")
    print("1.000 đơn lớn, đếm đơn lớn:", count_big_orders(big, 500000)[1], "bước")
    print("Big-O:", COMPLEXITY)
