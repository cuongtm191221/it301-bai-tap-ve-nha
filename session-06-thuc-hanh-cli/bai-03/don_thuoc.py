"""Nghiệp vụ danh sách đơn đặt thuốc online trong ngày của Pharmacity.

Mỗi đơn là một list [mã đơn, trạng thái "MOI" hoặc "HUY", số tiền]. Các thao tác dọn danh sách làm TẠI CHỖ
(sửa chính list, không tạo list mới), trong MỘT lượt duyệt, không gọi pop/remove/insert trong vòng lặp.
"""

SAMPLE = [
    ["PC1001", "MOI", 120000], ["PC1002", "HUY", 45000], ["PC1003", "MOI", 89000], ["PC1003", "MOI", 89000],
    ["PC1004", "HUY", 230000], ["PC1005", "MOI", 56000], ["PC1005", "MOI", 56000], ["PC1005", "MOI", 56000], ["PC1006", "MOI", 310000],
]


def make_orders():
    """Có sẵn. Trả về bản sao danh sách mẫu (có đơn hủy và đơn bị gửi trùng liền nhau)."""
    return [o[:] for o in SAMPLE]


def money(amount):
    """Có sẵn. 120000 -> "120.000đ"."""
    return f"{amount:,}".replace(",", ".") + "đ"


def add_order(orders, code, amount_text):
    """Thêm đơn mới trạng thái "MOI" vào cuối. Lỗi: "Mã đơn phải có dạng PC và 4 chữ số", "Số tiền phải là số nguyên dương"."""
    raise NotImplementedError


def cancel_order(orders, code):
    """Chuyển mọi đơn có mã code đang "MOI" sang "HUY", trả về số đơn đã hủy; không có đơn nào để hủy báo
    ValueError("Không có đơn <MÃ> đang chờ")."""
    raise NotImplementedError


def compact(orders):
    """Dồn các đơn "MOI" lên đầu, giữ nguyên thứ tự giữa chúng; các đơn "HUY" về cuối (thứ tự giữa chúng không quan trọng).
    Tại chỗ, một lượt. Trả về bộ (số đơn "MOI", số lần gán phần tử vào list)."""
    raise NotImplementedError


def drop_cancelled(orders):
    """Bỏ mọi đơn "HUY" khỏi danh sách (tại chỗ: dồn rồi cắt phần đuôi một lần), trả về số đơn đã bỏ."""
    raise NotImplementedError


def merge_duplicates(orders):
    """Gộp các đơn liền nhau có cùng mã (hệ thống gửi trùng): giữ đơn đầu tiên của mỗi nhóm liền nhau. Tại chỗ, một lượt.
    Trả về số đơn đã bỏ."""
    raise NotImplementedError


def reverse_in_place(orders):
    """Đảo ngược thứ tự danh sách tại chỗ bằng hai chỉ số đi từ hai đầu vào giữa; không dùng reverse(), [::-1], reversed()."""
    raise NotImplementedError
