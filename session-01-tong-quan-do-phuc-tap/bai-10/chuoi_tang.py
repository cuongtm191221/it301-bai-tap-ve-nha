"""Tìm chuỗi ngày doanh thu tăng liên tiếp dài nhất của gian hàng trên Shopee."""


def longest_growth_streak(revenues):
    """Trả về (độ dài chuỗi dài nhất, ngày bắt đầu tính từ 1, số lần so sánh) (xem đề, mục 2.1)."""
    raise NotImplementedError


def streak_message(revenues):
    """Trả về thông báo cho người bán (xem đề, mục 2.2)."""
    raise NotImplementedError


if __name__ == "__main__":
    week = [12, 15, 15, 18, 21, 25, 20, 22, 30]
    print("Tháng 11:", longest_growth_streak(week))
    print(streak_message(week))
    print(streak_message([5, 7, 9, 3, 4, 6]))
    print(streak_message([9, 8, 6, 6, 2]))
    print(streak_message([4, 6, 2, 3, 5, 8]))
    print(streak_message([10]))
    print(streak_message([]))
    print("1.000 ngày:", longest_growth_streak(list(range(1000)))[2], "lần so sánh")
