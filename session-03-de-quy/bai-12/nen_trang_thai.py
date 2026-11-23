"""Tóm tắt chuỗi trạng thái giao dịch tự động (nạp tiền điện thoại định kỳ) trên ví MoMo."""


def clean(status):
    """Có sẵn. Chuẩn hóa trạng thái: bỏ khoảng trắng hai đầu, đổi sang chữ in hoa."""
    return status.strip().upper()


def compress(statuses):
    """List các cặp (trạng thái đã chuẩn hóa, số lần liên tiếp), ví dụ ["OK", "ok", "FAIL"] thành [("OK", 2), ("FAIL", 1)]."""
    raise NotImplementedError


def longest_fail_streak(statuses):
    """Số lần FAIL liên tiếp dài nhất; không có FAIL trả về 0."""
    raise NotImplementedError


def summary(statuses):
    """Dòng tóm tắt cho người dùng, ví dụ "OK x2, FAIL x1"; list rỗng trả về "Chưa có giao dịch"."""
    raise NotImplementedError


if __name__ == "__main__":
    print(summary(["OK", "OK", "FAIL", "OK"]))
    print(summary(["ok ", " OK", "Ok"]))
    print(summary(["OK", "FAIL", "fail", "FAIL ", "OK", "FAIL"]))
    print(summary(["PENDING"]))
    print(summary([]))
    print("FAIL dài nhất:", longest_fail_streak(["FAIL", "OK", "FAIL", "FAIL"]))
