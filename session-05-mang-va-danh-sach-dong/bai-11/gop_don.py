"""Gộp hai danh sách đơn GrabFood từ hai máy chủ theo thời gian đặt."""


def merge_by_time(first, second):
    """List MỚI gồm mọi đơn của hai list (mỗi list đã xếp tăng dần theo giờ), xếp tăng dần theo giờ; cùng giờ thì đơn của first đứng trước."""
    raise NotImplementedError


def merge_unique(first, second):
    """Như merge_by_time nhưng bỏ các đơn bị ghi hai lần (cùng giờ và cùng mã với một đơn đã giữ); trả về (list mới, số đơn đã bỏ)."""
    raise NotImplementedError


def merge_report(first, second):
    """Dòng báo cáo sau khi gộp."""
    raise NotImplementedError


if __name__ == "__main__":
    server_a = [("07:05", "GF1001"), ("07:20", "GF1003"), ("08:10", "GF1006")]
    server_b = [("07:10", "GF1002"), ("07:20", "GF1004"), ("07:20", "GF1003"), ("09:00", "GF1009")]
    print(merge_by_time(server_a, server_b))
    print(merge_report(server_a, server_b))
    print(merge_report([], [("06:00", "GF0001")]))
    print(merge_report([], []))
    print("Máy chủ A vẫn giữ nguyên:", server_a)
