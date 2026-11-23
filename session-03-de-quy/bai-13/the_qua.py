"""Đếm số cách ghép thẻ quà tặng để thanh toán trên ví MoMo."""


def clean_values(values):
    """List mệnh giá hợp lệ (số nguyên dương), mỗi mệnh giá một lần, xếp tăng dần."""
    raise NotImplementedError


def count_pay_ways_v1(amount, values):
    """Số cách ghép đúng amount (nghìn đồng) từ các mệnh giá trong values, mỗi mệnh giá dùng bao nhiêu thẻ cũng được, không kể thứ tự."""
    raise NotImplementedError


def count_pay_ways_v2(amount, values):
    """Cùng kết quả với count_pay_ways_v1, cài theo giải pháp thứ hai."""
    raise NotImplementedError


def pay_ways_message(amount, values):
    """Thông báo cho người dùng, dùng giải pháp đã chọn."""
    raise NotImplementedError


if __name__ == "__main__":
    print(pay_ways_message(100, [10, 20, 50]))
    print(pay_ways_message(100, [50, 20, 10, 20]))
    print(pay_ways_message(35, [10, 20]))
    print(pay_ways_message(60, [0, -10, 20, 30]))
    print(pay_ways_message(0, [10, 20]))
    print(pay_ways_message(1000, [1, 2, 5, 10, 20, 50]))
