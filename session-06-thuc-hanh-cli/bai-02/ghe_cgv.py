"""Nghiệp vụ sơ đồ ghế một phòng chiếu CGV Vincom Bà Triệu.

Phòng chiếu là list các hàng; mỗi hàng là list các ô "." (trống) hoặc "X" (đã đặt). Hàng đặt tên A, B, C...; ghế đánh số từ 1.
"""

BOOKED = ["A3", "A4", "C5", "C6", "C7", "E1"]


def make_hall(rows, cols):
    """Phòng chiếu rows hàng, cols ghế mỗi hàng, mọi ghế trống; mỗi hàng là một list riêng.
    rows từ 1 đến 26, cols từ 1 đến 30, sai báo ValueError("Kích thước phòng không hợp lệ")."""
    raise NotImplementedError


def make_sample_hall():
    """Có sẵn. Phòng 5 hàng x 10 ghế với các ghế trong BOOKED đã đặt."""
    hall = make_hall(5, 10)
    for seat in BOOKED:
        book(hall, seat)
    return hall


def render(hall):
    """Có sẵn. Chuỗi nhiều dòng vẽ sơ đồ, ví dụ "A  . . X X . . . . . .", dòng cuối là màn hình."""
    lines = [f"{chr(65 + r)}  " + " ".join(row) for r, row in enumerate(hall)]
    return "\n".join(lines + ["   " + "MÀN HÌNH".center(2 * len(hall[0]) - 1, "=")])


def parse_seat(hall, text):
    """Đổi "C5" (chữ thường được) thành bộ (chỉ số hàng, chỉ số ghế) tính từ 0. Sai dạng (một chữ cái rồi số nguyên)
    báo ValueError("Ghế không hợp lệ"); hàng hoặc số ghế ngoài phòng báo ValueError("Ghế ngoài phòng chiếu")."""
    raise NotImplementedError


def book(hall, text):
    """Đặt ghế; ghế đã đặt báo ValueError("Ghế <GHẾ> đã có người đặt"). Trả về tên ghế chuẩn ("C5")."""
    raise NotImplementedError


def cancel(hall, text):
    """Hủy đặt ghế; ghế đang trống báo ValueError("Ghế <GHẾ> chưa được đặt"). Trả về tên ghế chuẩn."""
    raise NotImplementedError


def free_count(hall):
    """(số ghế trống, tổng số ghế)."""
    raise NotImplementedError


def find_block(hall, k):
    """Tên ghế đầu và ghế cuối của k ghế trống liền nhau đầu tiên (xét hàng A trước, trong hàng từ trái sang phải),
    ví dụ ("A5", "A7"); không có trả None. Mỗi hàng duyệt một lượt."""
    raise NotImplementedError
