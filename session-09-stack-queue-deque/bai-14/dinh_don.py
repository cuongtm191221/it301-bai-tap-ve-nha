"""Tìm đỉnh số đơn trong từng khung k phút để điều phối nhân sự kho Tiki."""


from collections import deque


def window_max_v1(orders, k):
    """List: phần tử thứ s là số đơn lớn nhất trong các phút s đến s + k - 1; k <= 0 hoặc k > len(orders) trả list rỗng."""
    raise NotImplementedError


def window_max_v2(orders, k):
    """Cùng kết quả với window_max_v1, cài theo giải pháp thứ hai."""
    raise NotImplementedError


def peak_message(orders, k):
    """Thông báo cho trưởng kho, dùng giải pháp đã chọn."""
    raise NotImplementedError


if __name__ == "__main__":
    minutes = [12, 30, 25, 8, 41, 19, 7, 33, 33, 10]
    print(window_max_v2(minutes, 3))
    print(peak_message(minutes, 3))
    print(peak_message(minutes, 1))
    print(peak_message(minutes, 11))
    print(peak_message(minutes, 0))
    day = [(m * 37) % 211 for m in range(24 * 60 * 30)]
    print(peak_message(day, 600))
