"""Điểm thưởng chuỗi ngày điểm danh trên ví MoMo."""


def streak_points(n):
    # Tổng điểm thưởng của chuỗi n ngày điểm danh liên tiếp: ngày thứ k được 100 x k điểm.
    # n = 0 (chưa điểm danh) thì được 0 điểm.
    if n == 1:
        return 0
    return streak_points(n - 1) + n


def count_digits(n):
    # Số chữ số của số nguyên dương n (dùng để căn lề cột số tiền trên sao kê).
    if n < 10:
        return 0
    return 1 + count_digits(n // 10)


if __name__ == "__main__":
    for amount in [7, 45000, 1250000]:
        print(f"Số chữ số của {amount}:", count_digits(amount))
    for n in [1, 3, 7, 0]:
        print(f"Chuỗi {n} ngày:", streak_points(n), "điểm")
