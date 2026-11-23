"""Sinh mã quà tặng cho chiến dịch khuyến mãi của ví MoMo."""


LIMIT = 100000


def clean_chars(chars):
    """List ký tự dùng để sinh mã: bỏ khoảng trắng, đổi sang chữ in hoa, mỗi ký tự một lần, xếp tăng dần."""
    raise NotImplementedError


def count_codes(chars, length):
    """Số mã dài length ký tự lấy từ chars (đã làm sạch), hai ký tự đứng cạnh nhau không trùng nhau."""
    raise NotImplementedError


def generate_codes(chars, length):
    """List mọi mã dài length ký tự theo quy tắc của count_codes, xếp tăng dần theo thứ tự từ điển."""
    raise NotImplementedError


def codes_message(chars, length):
    """Thông báo cho bộ phận khuyến mãi."""
    raise NotImplementedError


if __name__ == "__main__":
    print(codes_message("AB12", 3))
    print(generate_codes("AB12", 2))
    print(codes_message(" b a 1 a ", 2))
    print(codes_message("7", 3))
    print(codes_message("0123456789", 12))
    print(codes_message("", 4))
    print("Số mã dài 8 từ chữ A-Z và số 0-9:", count_codes("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 8))
