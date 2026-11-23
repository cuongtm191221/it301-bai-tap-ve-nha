"""P1 - Phản biện ba hàm do AI sinh trong ai_danh_sach.py."""

# Ghi "đúng" hoặc "sai" cho nhận xét của AI ở từng hàm.
CLAIMS = {
    "count_waiting": "?",
    "newest_submission": "?",
    "has_code": "?",
}


def count_waiting_fixed(queue):
    """Đếm số node, cùng kết quả với count_waiting nhưng không làm thay đổi queue."""
    raise NotImplementedError


def newest_submission_fixed(queue):
    """Trả value của node cuối (None nếu rỗng) trong O(1)."""
    raise NotImplementedError
