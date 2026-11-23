"""Kiểm tra mã giới thiệu bạn bè của ví MoMo."""


LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"


def valid_chars(code):
    # True nếu mọi ký tự của code là chữ in hoa hoặc chữ số. Chuỗi rỗng: True.
    if code == "":
        return True
    return code[0] in LETTERS + DIGITS or valid_chars(code[1:])


def count_digit_chars(code):
    # Số ký tự là chữ số trong code.
    if code == "":
        return 0
    if code[0] in "123456789":
        return 1 + count_digit_chars(code[1:])
    return count_digit_chars(code[1:])


def is_valid_code(code):
    # Mã hợp lệ: dài 6 đến 10 ký tự, bắt đầu bằng chữ in hoa,
    # chỉ gồm chữ in hoa và chữ số, có ít nhất 2 chữ số.
    return (len(code) > 6 and len(code) <= 10 and code[0] in LETTERS
            and valid_chars(code) and count_digit_chars(code) >= 2)


if __name__ == "__main__":
    for code in ("MOMO2024", "MOMO@24", "MOMO10", "AB1234", "MOMO100", "1MOMO23", "MOMOVN", ""):
        print(f"{code!r:12}", "hợp lệ" if is_valid_code(code) else "không hợp lệ")
