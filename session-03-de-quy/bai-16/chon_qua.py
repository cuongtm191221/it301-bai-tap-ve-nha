"""Đếm số cách chọn ô quà trong trò chơi "Mở hộp may mắn" của ví MoMo."""


from functools import lru_cache


def choose_count_v1(n, k):
    """Số cách chọn k ô khác nhau trong n ô (không kể thứ tự); k < 0 hoặc k > n thì 0."""
    raise NotImplementedError


def choose_count_v2(n, k):
    """Cùng kết quả với choose_count_v1, cài theo giải pháp thứ hai."""
    raise NotImplementedError


@lru_cache(maxsize=None)

def prize_message(n, k):
    """Thông báo trên màn hình trò chơi, dùng giải pháp đã chọn."""
    raise NotImplementedError


if __name__ == "__main__":
    print(prize_message(5, 2))
    print(prize_message(10, 10))
    print(prize_message(4, 6))
    print(prize_message(0, 1))
    print(prize_message(40, 20))
    print(prize_message(60, 30))
