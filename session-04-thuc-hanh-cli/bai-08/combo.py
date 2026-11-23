"""Nghiệp vụ gợi ý combo trong ngân sách cho quán Cơm Tấm Phúc Lộc Thọ trên GrabFood.

Thực đơn là list các món [mã món, tên món, giá (đồng)]. Một combo là một tập các món khác nhau (mỗi món nhiều nhất một phần),
không rỗng, tổng giá không vượt ngân sách. Các hàm liệt kê, đếm combo viết bằng ĐỆ QUY.
"""
import timeit

SAMPLE_MENU = [
    ["CT01", "Cơm tấm sườn", 55000], ["CT02", "Cơm tấm sườn bì chả", 69000], ["CT03", "Canh khổ qua", 25000],
    ["CT04", "Trà đá", 5000], ["CT05", "Chả trứng thêm", 15000], ["CT06", "Nước sâm", 18000], ["CT07", "Sườn thêm", 30000],
]


def make_menu():
    """Có sẵn. Trả về bản sao thực đơn mẫu."""
    return [m[:] for m in SAMPLE_MENU]


def make_big_prices(n):
    """Có sẵn. Giá n món giả lập (đồng)."""
    return [5000 + (k * 7919) % 60 * 1000 for k in range(n)]


def money(amount):
    """Có sẵn. 99000 -> "99.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def parse_budget(text):
    """Có sẵn. Ngân sách là số nguyên từ 10.000 đến 2.000.000; sai báo ValueError."""
    text = text.strip()
    if not text.isdigit() or not 10000 <= int(text) <= 2000000:
        raise ValueError("Ngân sách phải là số nguyên từ 10.000 đến 2.000.000")
    return int(text)


def count_combos_v1(prices, budget):
    """Giải pháp 1. Số combo (tập món không rỗng) có tổng giá <= budget; prices là list giá. Không làm đổi prices."""
    raise NotImplementedError


def count_combos_v2(prices, budget):
    """Giải pháp 2: cùng kết quả với giải pháp 1, cách làm khác, nhanh hơn rõ rệt khi ngân sách nhỏ so với thực đơn;
    40 món, ngân sách 200.000đ trong 1 giây. Không làm đổi prices."""
    raise NotImplementedError


def best_combo(menu, budget):
    """Combo có tổng giá lớn nhất không vượt budget; nhiều combo cùng tổng thì chọn combo ít món hơn,
    vẫn bằng thì chọn combo có món đứng trước trong thực đơn (so lần lượt chỉ số món). Trả về list món theo thứ tự thực đơn,
    hoặc [] nếu không món nào vừa ngân sách. Đệ quy."""
    raise NotImplementedError


def benchmark(sizes, budget=150000, number=1):
    """Với từng n trong sizes, trên make_big_prices(n): đo bằng timeit một lần mỗi giải pháp (ms).
    Trả về list bộ (n, ms giải pháp 1, ms giải pháp 2)."""
    raise NotImplementedError
