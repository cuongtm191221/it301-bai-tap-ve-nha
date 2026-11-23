"""Thống kê chi tiêu theo nhóm lồng nhau trên màn hình "Quản lý chi tiêu" của ví MoMo."""


def total_spending(items):
    # Tổng tiền của mọi giao dịch trong items, kể cả giao dịch nằm trong các nhóm con.
    # Mỗi phần tử là một số tiền (số nguyên) hoặc một nhóm con (list).
    total = 0
    for item in items:
        if type(item) == list:
            total += total_spending(item)
        elif item > 0:
            total += item
    return total


def count_transactions(items):
    # Số giao dịch (số tiền) trong items, kể cả trong các nhóm con.
    count = 0
    for item in items:
        if type(item) == list:
            count += 1 + count_transactions(item)
        else:
            count += 1
    return count


def deepest_level(items):
    # Số cấp sâu nhất: list không có nhóm con là 1 cấp.
    deepest = 1
    for item in items:
        if type(item) == list:
            deepest = deepest_level(item) + 1
    return deepest


if __name__ == "__main__":
    spending = [120000, [45000, 30000], 15000]
    print("Tổng chi tiêu:", total_spending(spending))
    print("Số giao dịch:", count_transactions([120000, 45000, 15000]))
    print("Số cấp sâu nhất:", deepest_level([120000, [45000, [30000]]]))
    print("Tháng chưa có giao dịch:", total_spending([]))
