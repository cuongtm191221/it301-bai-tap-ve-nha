"""Nghiệp vụ kiểm tra mã vận đơn tại bưu cục J&T Express.

Mã vận đơn gồm "JT" và 10 chữ số; chữ số cuối là chữ số kiểm tra theo thuật toán Luhn:
đi từ chữ số cuối sang trái, gấp đôi các chữ số ở vị trí thứ 2, 4, 6... (nếu được số lớn hơn 9 thì trừ 9), cộng tất cả;
mã đúng khi tổng chia hết cho 10. Các hàm xử lý chuỗi và list viết bằng ĐỆ QUY, không dùng vòng lặp.
"""

SAMPLE_PARCELS = [["JT8402193752", "Nguyễn Hoài An"], ["JT5120064380", "Trần Bảo Ngọc"], ["JT7301182643", "Lê Quốc Huy"]]


def make_parcels():
    """Có sẵn. Trả về bản sao danh sách đơn đã nhận."""
    return [p[:] for p in SAMPLE_PARCELS]


def clean(text):
    """Bỏ mọi dấu cách và dấu gạch ngang, đổi chữ thường thành chữ hoa. Đệ quy, không vòng lặp, không replace()."""
    raise NotImplementedError


def luhn_sum(digits, double):
    """Tổng Luhn của chuỗi chữ số, xét từ chữ số cuối; double cho biết chữ số cuối có được gấp đôi không. Đệ quy, không vòng lặp."""
    raise NotImplementedError


def check_digit(body):
    """Chữ số kiểm tra (0-9) cho 9 chữ số đầu body, để mã body + chữ số đó đúng theo Luhn."""
    raise NotImplementedError


def normalize(text):
    """Làm sạch mã; sai dạng báo ValueError("Mã vận đơn phải gồm JT và 10 chữ số"). Trả về mã đã làm sạch."""
    raise NotImplementedError


def is_valid(code):
    """Mã (đã làm sạch, đúng dạng) có đúng chữ số kiểm tra không."""
    raise NotImplementedError


def invalid_codes(codes):
    """List các mã sai (sai dạng hoặc sai chữ số kiểm tra) trong list chuỗi codes, giữ thứ tự, viết như người dùng gõ
    nhưng đã bỏ khoảng trắng hai đầu. Đệ quy, không vòng lặp."""
    raise NotImplementedError


def receive(parcels, code_text, name):
    """Nhận đơn mới vào cuối danh sách, trả về đơn. Lỗi (danh sách giữ nguyên): lỗi của normalize,
    "Mã vận đơn sai chữ số kiểm tra", "Mã <MÃ> đã được nhận", "Người nhận không được để trống"."""
    raise NotImplementedError
