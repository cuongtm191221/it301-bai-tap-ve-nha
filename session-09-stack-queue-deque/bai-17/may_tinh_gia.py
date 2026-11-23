"""Máy tính công thức giá cho người bán trên Tiki: nhận biểu thức trung tố có ngoặc."""


OPERATORS = {"+": 1, "-": 1, "*": 2, "/": 2}


def tokenize(expr):
    """Tách chuỗi công thức thành list token: số nguyên (int), toán tử "+ - * /", ngoặc "(" ")". Bỏ qua khoảng trắng; ký tự khác báo ValueError("Ký tự không hợp lệ: x")."""
    raise NotImplementedError


def to_postfix(tokens):
    """Chuyển list token trung tố sang list token hậu tố. Sai ngoặc báo ValueError("Ngoặc không khớp"); sai cú pháp (thiếu số, thừa toán tử, hai số liền nhau, rỗng) báo ValueError("Biểu thức sai cú pháp")."""
    raise NotImplementedError


def evaluate_postfix(postfix):
    """Có sẵn. Tính list token hậu tố; "/" là chia lấy phần nguyên; chia cho 0 báo ZeroDivisionError("Chia cho 0")."""
    stack = []
    for tok in postfix:
        if type(tok) is int:
            stack.append(tok)
            continue
        right = stack.pop()
        left = stack.pop()
        if tok == "+":
            stack.append(left + right)
        elif tok == "-":
            stack.append(left - right)
        elif tok == "*":
            stack.append(left * right)
        else:
            if right == 0:
                raise ZeroDivisionError("Chia cho 0")
            stack.append(left // right)
    return stack[0]


def calculate(expr):
    """Tính công thức trung tố expr (chuỗi), trả về số nguyên."""
    raise NotImplementedError


def price_message(name, expr):
    """Dòng hiển thị cho người bán: "Giá <name>: <kết quả>đ" hoặc "Lỗi công thức <name>: <thông báo lỗi>"."""
    raise NotImplementedError


if __name__ == "__main__":
    print(tokenize("(199000 - 20000) * 90 / 100"))
    print(to_postfix(tokenize("(199000 - 20000) * 90 / 100")))
    print(price_message("tai nghe", "(199000 - 20000) * 90 / 100"))
    print(price_message("ốp lưng", "100000 - 20000 - 10000"))
    print(price_message("sạc", "(150000 + 5000"))
    print(price_message("cáp", "50000 * 0,9"))
    print(price_message("pin", "80000 / (2 - 2)"))
    print(price_message("loa", "300000 +"))
