"""Giải nén chuỗi lệnh di chuyển cho robot xếp hàng trong kho Tiki."""


def decode_v1(commands):
    """Chuỗi lệnh đầy đủ sau khi giải nén; k[...] nghĩa là lặp k lần phần trong ngoặc; sai cú pháp báo ValueError("Chuỗi lệnh không hợp lệ")."""
    raise NotImplementedError


def decode_v2(commands):
    """Cùng kết quả với decode_v1, cài theo giải pháp thứ hai."""
    raise NotImplementedError


def route_message(commands):
    """Thông báo cho bảng điều khiển robot, dùng giải pháp đã chọn."""
    raise NotImplementedError


if __name__ == "__main__":
    for cmd in ("3[R]U", "2[L3[R]]D", "10[U]", "R2[]L", "3[R", "2]R", "0[R]", "2[x]"):
        print(f"{cmd!r:12} -> {route_message(cmd)}")
    print("Lồng 3.000 tầng:", route_message("1[" * 3000 + "R" + "]" * 3000))
