"""Tìm giao dịch lớn nhất trong tháng cho màn hình "Quản lý chi tiêu" của ví MoMo."""


def largest(transactions):
    # Số tiền lớn nhất trong list transactions. List rỗng: trả về None.
    if len(transactions) == 1:
        return transactions[0]
    if transactions[0] > largest(transactions[1:]):
        return transactions[0]
    return largest(transactions[1:])


if __name__ == "__main__":
    june = [150000, 2500000, 49000, 1000000, 320000]
    print("Giao dịch lớn nhất tháng 6:", largest(june))
    print("Một giao dịch:", largest([75000]))
    print("Tháng chưa có giao dịch:", largest([]))
    growing = [10000 * k for k in range(1, 31)]
    print("30 giao dịch tăng dần:", largest(growing))
    print("Số giao dịch tháng 6 không đổi:", len(june))
