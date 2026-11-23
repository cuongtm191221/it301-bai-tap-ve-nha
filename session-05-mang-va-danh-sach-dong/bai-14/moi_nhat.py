"""Màn hình "Hoạt động gần đây" của ứng dụng Grab: sự kiện mới nhất hiện trước."""


def latest_first_v1(events):
    """List MỚI các sự kiện theo thứ tự mới nhất trước (events xếp từ cũ tới mới); không sửa events."""
    raise NotImplementedError


def latest_first_v2(events):
    """Cùng kết quả với latest_first_v1, cài theo giải pháp thứ hai."""
    raise NotImplementedError


def recent_message(events, k):
    """Dòng hiển thị k sự kiện mới nhất, dùng giải pháp đã chọn."""
    raise NotImplementedError


if __name__ == "__main__":
    events = ["Đặt GrabBike", "Thanh toán 25.000đ", "Đánh giá 5 sao", "Đặt GrabFood", "Nhận ưu đãi"]
    print(latest_first_v2(events))
    print(recent_message(events, 3))
    print(recent_message(events, 10))
    print(recent_message([], 3))
    print(recent_message(events, 0))
    log = [f"SK{k}" for k in range(200000)]
    print(recent_message(log, 2), "| nhật ký gốc giữ nguyên:", log[0])
