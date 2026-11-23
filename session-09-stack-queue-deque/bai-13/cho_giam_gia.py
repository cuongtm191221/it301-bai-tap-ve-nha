"""Gợi ý "chờ giá giảm" trên trang theo dõi giá sản phẩm Tiki."""


def money(amount):
    """Có sẵn. Số tiền có dấu chấm ngăn cách hàng nghìn."""
    return f"{amount:,}".replace(",", ".")


def wait_days_v1(prices):
    """List: phần tử thứ i là số ngày từ ngày i tới ngày gần nhất sau đó có giá THẤP HƠN hẳn; không có thì 0."""
    raise NotImplementedError


def wait_days_v2(prices):
    """Cùng kết quả với wait_days_v1, cài theo giải pháp thứ hai."""
    raise NotImplementedError


def wait_message(prices, day):
    """Gợi ý cho khách đang xem sản phẩm ở ngày day (đếm từ 1), dùng giải pháp đã chọn."""
    raise NotImplementedError


if __name__ == "__main__":
    history = [129000, 125000, 135000, 140000, 119000, 119000, 139000, 99000]
    print(wait_days_v2(history))
    for day in (1, 3, 5, 8, 9):
        print(wait_message(history, day))
    long = [(k * 7919) % 100003 + 50000 for k in range(200000)]
    print("200.000 ngày, ngày đầu:", wait_message(long, 1))
