"""Trò chơi "Mã may mắn" trên ví MoMo: mã giao dịch đối xứng được thưởng."""


def reverse_code(code):
    # Trả về chuỗi code viết ngược.
    if code == "":
        return ""
    return code[0] + reverse_code(code[1:])


def is_symmetric(code):
    # True nếu code đọc xuôi và đọc ngược giống nhau. Chuỗi rỗng và chuỗi một ký tự là đối xứng.
    if len(code) == 1:
        return True
    if code[0] != code[-1]:
        return False
    return is_symmetric(code[1:-1])


if __name__ == "__main__":
    for code in ["MOMO24", "ABC", "X"]:
        print(f"Đảo {code}:", reverse_code(code))
    for code in ["121", "7887", "12321", "MOMO", "A"]:
        print(f"{code} đối xứng?", is_symmetric(code))
    print("Mã rỗng đối xứng?", is_symmetric(""))
