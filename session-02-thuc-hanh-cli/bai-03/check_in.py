"""Nghiệp vụ danh sách hành khách check-in chuyến VJ123 của Vietjet Air.

Mỗi hành khách là một list: [mã đặt chỗ, họ tên, hành lý ký gửi (kg)].
Danh sách luôn được xếp tăng dần theo mã đặt chỗ.
"""

SAMPLE_PASSENGERS = [
    ["AB123", "Nguyễn Minh An", 15],
    ["BK207", "Trần Thu Bình", 23],
    ["CK310", "Lê Hoàng Cường", 7],
    ["DN452", "Phạm Ngọc Dung", 20],
    ["HV518", "Võ Thanh Hà", 32],
    ["QT609", "Đỗ Quang Tùng", 0],
]
BAGGAGE_LIMIT = 20


def make_passengers():
    """Có sẵn. Trả về bản sao danh sách mẫu (đã xếp tăng dần theo mã)."""
    return [p[:] for p in SAMPLE_PASSENGERS]


def format_passenger(p):
    """Có sẵn. "AB123 | Nguyễn Minh An | 15 kg"."""
    return f"{p[0]} | {p[1]} | {p[2]} kg"


def normalize_code(text):
    """Đổi mã về chữ in hoa, bỏ khoảng trắng hai đầu; mã hợp lệ gồm đúng 2 chữ cái rồi 3 chữ số.
    Sai báo ValueError("Mã đặt chỗ phải gồm 2 chữ cái và 3 chữ số")."""
    raise NotImplementedError


def parse_count(text):
    """Đổi chuỗi thành số nguyên dương; sai báo ValueError("Số hành khách phải là số nguyên dương")."""
    raise NotImplementedError


def first_k(passengers, k):
    """List k hành khách đầu (ít hơn k thì trả tất cả); không làm đổi passengers."""
    raise NotImplementedError


def last_k(passengers, k):
    """List k hành khách cuối, giữ thứ tự (ít hơn k thì trả tất cả); không làm đổi passengers."""
    raise NotImplementedError


def find_linear(passengers, code):
    """Tìm tuần tự từ đầu tới cuối. Trả về (hành khách hoặc None, số lần so sánh mã)."""
    raise NotImplementedError


def find_early_stop(passengers, code):
    """Tìm từ đầu, dựa vào danh sách đã xếp: gặp mã lớn hơn code thì dừng ngay vì phía sau không thể có.
    Trả về (hành khách hoặc None, số lần so sánh mã; mỗi phần tử xét là một lần)."""
    raise NotImplementedError


def check_in(passengers, code_text, name, kg_text):
    """Thêm hành khách vào đúng vị trí để danh sách vẫn tăng dần theo mã; trả về vị trí (đếm từ 1).
    Lỗi (danh sách giữ nguyên): thông báo của normalize_code, "Mã đặt chỗ <MÃ> đã check-in",
    "Họ tên không được để trống", "Hành lý phải là số nguyên từ 0 đến 40 kg"."""
    raise NotImplementedError


def baggage_stats(passengers):
    """Trả về (tổng kg hành lý, số hành khách có hành lý vượt BAGGAGE_LIMIT kg). Bộ nhớ phụ O(1): không tạo list phụ."""
    raise NotImplementedError
