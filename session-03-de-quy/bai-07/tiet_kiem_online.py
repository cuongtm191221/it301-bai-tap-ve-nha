"""Tính số dư tiết kiệm online tự tái tục trên ví MoMo."""


def balance_after(principal, rate, years):
    # Số dư sau years năm. Mỗi năm: lãi = số dư đầu năm * rate // 100, cộng vào số dư.
    if years == 1:
        return principal + principal * rate // 100
    return balance_after(principal, rate, years - 1) + principal * rate // 100


def history(principal, rate, years):
    # List số dư cuối mỗi năm, từ năm 0 (số tiền gửi ban đầu) đến năm years.
    if years == 0:
        return [principal]
    return history(principal, rate, years - 1).append(balance_after(principal, rate, years))


if __name__ == "__main__":
    print("Gửi 10.000.000đ, lãi 6%/năm, sau 1 năm:", balance_after(10000000, 6, 1))
    print("Gửi 10.000.000đ, lãi 6%/năm, sau 3 năm:", balance_after(10000000, 6, 3))
    print("Lịch sử 3 năm:", history(10000000, 6, 3))
    print("Rút ngay trong năm đầu (0 năm):", balance_after(10000000, 6, 0))
