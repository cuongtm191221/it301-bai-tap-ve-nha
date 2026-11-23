"""Tìm khung giờ cao điểm của một quận cho đội tài xế GrabBike."""


def busiest_window_v1(trips, k):
    """Bộ (giờ bắt đầu, tổng số chuyến) của k giờ liên tiếp có nhiều chuyến nhất; bằng nhau lấy khung sớm nhất; k <= 0 hoặc k > len(trips) trả None."""
    raise NotImplementedError


def busiest_window_v2(trips, k):
    """Cùng kết quả với busiest_window_v1, cài theo giải pháp thứ hai."""
    raise NotImplementedError


def window_message(trips, k):
    """Thông báo cho đội tài xế, dùng giải pháp đã chọn."""
    raise NotImplementedError


if __name__ == "__main__":
    day = [12, 8, 5, 4, 6, 20, 45, 60, 38, 25, 30, 41, 50, 33, 28, 31, 47, 66, 58, 40, 27, 22, 18, 15]
    print(window_message(day, 3))
    print(window_message(day, 1))
    print(window_message([5, 9, 9, 5], 2))
    print(window_message(day[:2], 3))
    print(window_message(day, 0))
    year = [(h * 37) % 101 for h in range(24 * 365 * 20)]
    print(window_message(year, 1000))
