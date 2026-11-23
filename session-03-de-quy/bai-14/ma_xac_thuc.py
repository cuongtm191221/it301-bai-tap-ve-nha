"""Sinh mã xác thực theo bộ đếm cho thiết bị thanh toán MoMo tại cửa hàng (mô hình đơn giản hóa)."""


def otp_value_v1(seed, counter, mod):
    """Giá trị seed mũ counter rồi lấy phần dư khi chia cho mod (counter >= 0, mod >= 1)."""
    raise NotImplementedError


def otp_value_v2(seed, counter, mod):
    """Cùng kết quả với otp_value_v1, cài theo giải pháp thứ hai."""
    raise NotImplementedError


def otp_message(seed, counter, mod):
    """Mã hiển thị 6 chữ số trên thiết bị, dùng giải pháp đã chọn."""
    raise NotImplementedError


if __name__ == "__main__":
    print(otp_message(7, 3, 1000000))
    print(otp_message(123457, 10, 999983))
    print(otp_message(123457, 0, 999983))
    print(otp_message(5, 4, 1))
    print(otp_message(123457, -1, 999983))
    print(otp_message(123457, 5000, 999983))
    print(otp_message(123457, 1000000000, 999983))
