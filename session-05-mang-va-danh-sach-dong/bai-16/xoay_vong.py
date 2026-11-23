"""Xoay vòng danh sách tài xế ưu tiên tại điểm đón sân bay của GrabCar."""


def rotate_v1(drivers, k):
    """List MỚI sau khi xoay drivers sang trái k bước (k âm: sang phải); không sửa drivers."""
    raise NotImplementedError


def rotate_v2(drivers, k):
    """Cùng kết quả với rotate_v1, cài theo giải pháp thứ hai."""
    raise NotImplementedError


def next_round_message(drivers, k):
    """Thông báo lượt ưu tiên sau k lượt, dùng giải pháp đã chọn."""
    raise NotImplementedError


if __name__ == "__main__":
    drivers = ["An", "Bình", "Chi", "Dũng", "Em"]
    print(rotate_v2(drivers, 2))
    print(next_round_message(drivers, 2))
    print(next_round_message(drivers, 7))
    print(next_round_message(drivers, -1))
    print(next_round_message([], 3))
    fleet = [f"TX{k}" for k in range(100000)]
    print(next_round_message(fleet, 99999), "| danh sách gốc:", fleet[0])
