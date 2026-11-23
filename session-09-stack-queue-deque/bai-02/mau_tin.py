"""Kiểm tra dấu ngoặc trong mẫu tin nhắn gửi khách hàng Tiki."""
def matches(open_ch, close_ch):
    # True nếu dấu mở open_ch và dấu đóng close_ch là một cặp: (), [] hoặc {}.
    return open_ch in "([{" and close_ch in ")]}"


def is_balanced(template):
    # True nếu mọi dấu ngoặc trong mẫu tin nhắn mở, đóng đúng cặp và đúng thứ tự lồng nhau.
    stack = []
    for ch in template:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            top = stack.pop()
            if not matches(top, ch):
                return False
    return True


if __name__ == "__main__":
    templates = [
        "Chào {ten}, đơn [{ma_don}] đã giao (dự kiến {ngay}).",
        "Mã {ma_giam] giảm 10%",
        "Đơn (dự kiến {ngay}",
        "Hoàn tiền) cho đơn {ma_don}",
        "Không có ngoặc",
    ]
    for t in templates:
        print("Hợp lệ" if is_balanced(t) else "Sai ngoặc", "|", t)
