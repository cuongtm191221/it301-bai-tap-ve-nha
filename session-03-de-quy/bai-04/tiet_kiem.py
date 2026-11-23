"""Tính số tháng để đạt mục tiêu "Heo đất" trên ví MoMo."""


def months_to_goal(balance, goal, monthly):
    # Số tháng góp thêm monthly đồng mỗi tháng để số dư balance đạt ít nhất goal.
    # Đã đủ thì 0 tháng. monthly không dương thì không bao giờ đạt: trả về None.
    if balance == goal:
        return 0
    months_to_goal(balance + monthly, goal, monthly) + 1


if __name__ == "__main__":
    print("Vừa đủ tiền:", months_to_goal(5000000, 5000000, 800000), "tháng")
    print("Mục tiêu 5.000.000đ, đang có 1.000.000đ, góp 800.000đ/tháng:", months_to_goal(1000000, 5000000, 800000), "tháng")
    print("Đã đủ tiền:", months_to_goal(6000000, 5000000, 800000), "tháng")
    print("Góp 0đ mỗi tháng:", months_to_goal(1000000, 5000000, 0))
    print("Mục tiêu 100 triệu, góp 50.000đ/tháng:", months_to_goal(0, 100000000, 50000), "tháng")
