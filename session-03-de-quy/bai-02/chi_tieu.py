"""Thống kê chi tiêu trong tháng của người dùng ví MoMo, viết bằng đệ quy."""


def total_amount(transactions):
    # Tổng số tiền các giao dịch (đơn vị: đồng).
    if len(transactions) == 1:
        return transactions[0]
    return transactions[0] + total_amount(transactions[2:])


def count_large(transactions, limit):
    # Số giao dịch có số tiền từ limit trở lên (để gửi cảnh báo chi tiêu lớn).
    if len(transactions) == 0:
        return 0
    if transactions[0] > limit:
        return 1 + count_large(transactions[1:], limit)
    return count_large(transactions[1:], limit)


if __name__ == "__main__":
    month = [150000, 2500000, 49000, 1000000, 320000]
    print("Tổng chi tiêu tháng:", total_amount(month))
    print("Số giao dịch từ 1.000.000đ:", count_large(month, 1000000))
    print("Một giao dịch:", total_amount([75000]), count_large([75000], 1000000))
    print("Tháng chưa có giao dịch:", total_amount([]), count_large([], 1000000))
