"""Báo cáo khách hàng chi tiêu cao của gian hàng trên Shopee (để gửi mã giảm giá tri ân)."""


def above_average(customers):
    # Trả về (danh sách mã khách có tổng chi tiêu LỚN HƠN mức trung bình của gian hàng, số lần cộng).
    # Số lần cộng: mỗi lần cộng một khoản chi tiêu vào tổng tính là 1.
    result = []
    additions = 0
    for c in customers:
        total = 0
        for other in customers:
            total += other["spent"]
            additions += 1
        average = total // len(customers)
        if c["spent"] >= average:
            result.append(c["code"])
    return result, additions


if __name__ == "__main__":
    customers = [
        {"code": "KH01", "spent": 1000000},
        {"code": "KH02", "spent": 2000000},
        {"code": "KH03", "spent": 1500000},
        {"code": "KH04", "spent": 1500001},
    ]
    print("4 khách:", above_average(customers))
    same = [{"code": "KH05", "spent": 500000}, {"code": "KH06", "spent": 500000}]
    print("2 khách chi bằng nhau:", above_average(same))
    print("Chưa có khách:", above_average([]))
    for n in [100, 1000]:
        many = [{"code": f"KH{i}", "spent": i * 1000} for i in range(n)]
        print(f"{n} khách:", above_average(many)[1], "lần cộng")
