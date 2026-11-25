"""Nghiệp vụ nút Quay lại, Tiến tới trên ứng dụng đọc báo VnExpress.

current là bài đang đọc. back giữ các bài có thể quay lại (gần nhất ở cuối), là deque(maxlen=MAX_BACK): đủ chỗ thì
bài cũ nhất tự rơi ra. forward là list dùng như ngăn xếp (append, pop ở cuối) giữ các bài có thể tiến tới.
"""
from collections import deque

MAX_BACK = 5


class Reader:
    """Có sẵn. Trạng thái người đọc: bắt đầu ở trang chủ "A100"."""

    def __init__(self):
        self.current = "A100"
        self.back = deque(maxlen=MAX_BACK)
        self.forward = []


def check_code(text):
    """Có sẵn. Mã bài viết hoa, bỏ khoảng trắng; dạng "A" + 3 chữ số, sai báo ValueError("Mã bài phải có dạng A và 3 chữ số")."""
    code = text.strip().upper()
    if len(code) != 4 or code[0] != "A" or not code[1:].isdigit():
        raise ValueError("Mã bài phải có dạng A và 3 chữ số")
    return code


def visit(reader, text):
    """Mở bài mới: bài đang đọc vào back, xóa sạch forward. Mở lại đúng bài đang đọc báo
    ValueError("Bạn đang đọc bài <mã>"). Trả về mã bài."""
    raise NotImplementedError


def go_back(reader):
    """Quay lại: bài đang đọc vào forward, lấy bài gần nhất của back. Không có báo ValueError("Không có bài để quay lại").
    Trả về bài mới đang đọc."""
    raise NotImplementedError


def go_forward(reader):
    """Tiến tới: bài đang đọc vào back, lấy bài trên đỉnh forward. Không có báo ValueError("Không có bài để tiến tới").
    Trả về bài mới đang đọc."""
    raise NotImplementedError


def history(reader, which):
    """List mã bài, bài sẽ tới trước đứng trước: which "back" là thứ tự bấm Quay lại, "forward" là thứ tự bấm Tiến tới.
    Không làm đổi back, forward."""
    raise NotImplementedError
