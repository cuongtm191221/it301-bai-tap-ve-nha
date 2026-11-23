"""Lập kế hoạch tiết kiệm góp tăng dần cho tính năng "Heo đất" của ví MoMo."""


def money(amount):
    """Có sẵn. Số tiền có dấu chấm ngăn cách hàng nghìn, ví dụ 1234567 thành "1.234.567"."""
    if amount < 0:
        return "-" + money(-amount)
    if amount < 1000:
        return str(amount)
    return money(amount // 1000) + "." + str(amount % 1000).zfill(3)


LIMIT_MONTHS = 600


def savings_schedule(balance, goal, monthly, step):
    """List các bộ (tháng, số dư cuối tháng) từ tháng 1 tới tháng đầu tiên số dư đạt goal; mức góp tăng step sau mỗi tháng; đã đủ thì []; quá 600 tháng thì None."""
    raise NotImplementedError


def months_needed(balance, goal, monthly, step):
    """Số tháng cần góp; đã đủ thì 0; không đạt trong 600 tháng thì None."""
    raise NotImplementedError


def plan_message(balance, goal, monthly, step):
    """Thông báo trên màn hình Heo đất."""
    raise NotImplementedError


if __name__ == "__main__":
    print(plan_message(1000000, 5000000, 800000, 0))
    print(plan_message(0, 10000000, 500000, 100000))
    print(savings_schedule(0, 2000000, 500000, 100000))
    print(plan_message(6000000, 5000000, 800000, 0))
    print(plan_message(0, 3000000, -200000, 100000))
    print(plan_message(0, 5000000, 0, 0))
    print(plan_message(0, 500000000, 100000, 0))
    print(plan_message(0, 0, 100000, 0))
