"""Nghiệp vụ bảng doanh số tháng của nhân viên bán hàng cửa hàng Thế Giới Di Động (TGDĐ) Quận 7.

Mỗi nhân viên là một list: [mã nhân viên, họ tên, doanh số tháng (triệu đồng)].
"""

SAMPLE_STAFF = [
    ["NV01", "Nguyễn Hải", 120],
    ["NV02", "Trần Mai", 95],
    ["NV03", "Lê Phong", 150],
    ["NV04", "Phạm Quỳnh", 95],
    ["NV05", "Đỗ Khoa", 60],
]


def make_staff():
    """Có sẵn. Trả về bản sao bảng mẫu."""
    return [s[:] for s in SAMPLE_STAFF]


def format_staff(s):
    """Có sẵn. "NV03 | Lê Phong | 150 triệu"."""
    return f"{s[0]} | {s[1]} | {s[2]} triệu"


def parse_positive(text, message):
    """Có sẵn. Đổi chuỗi thành số nguyên dương; sai báo ValueError(message)."""
    text = text.strip()
    if not text.isdigit() or int(text) == 0:
        raise ValueError(message)
    return int(text)


def find_staff(staff, code):
    """Nhân viên có mã code (không phân biệt hoa thường, bỏ khoảng trắng) hoặc None."""
    raise NotImplementedError


def add_sales(staff, code, amount_text):
    """Cộng doanh số đơn mới cho nhân viên, trả về nhân viên đó. Lỗi (bảng giữ nguyên):
    "Không có nhân viên <MÃ>", "Doanh số phải là số nguyên dương"."""
    raise NotImplementedError


def remove_staff(staff, code):
    """Xóa nhân viên nghỉ việc, trả về nhân viên đã xóa; không có báo ValueError("Không có nhân viên <MÃ>")."""
    raise NotImplementedError


def ranking(staff):
    """List mới xếp doanh số giảm dần; bằng nhau giữ thứ tự trong bảng; không làm đổi thứ tự của staff."""
    raise NotImplementedError


def best_and_worst(staff):
    """(nhân viên doanh số cao nhất, thấp nhất) tìm trong MỘT lượt duyệt, không sắp xếp; bằng nhau lấy người đứng trước.
    Bảng rỗng trả (None, None)."""
    raise NotImplementedError


def count_kpi(staff, threshold_text):
    """Số nhân viên có doanh số >= ngưỡng; ngưỡng sai báo ValueError("Ngưỡng KPI phải là số nguyên dương")."""
    raise NotImplementedError


def average_sales(staff):
    """Doanh số trung bình (số thực) hoặc None khi bảng rỗng."""
    raise NotImplementedError
