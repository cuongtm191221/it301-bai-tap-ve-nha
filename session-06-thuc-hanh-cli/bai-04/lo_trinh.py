"""Nghiệp vụ lộ trình giao hàng trong ngày của một tài xế Ahamove.

Lộ trình là list tên các điểm dừng theo thứ tự đi. Điểm dừng đánh số từ 1 khi giao tiếp với tài xế.
Các thao tác tự dịch phần tử bằng vòng lặp và đếm số lần dịch, không dùng insert, pop(i), reverse, [::-1], reversed.
"""

SAMPLE = ["Kho Quận 1", "Chợ Bến Thành", "Nhà thờ Đức Bà", "Landmark 81", "Thảo Điền"]


def make_route():
    """Có sẵn. Trả về bản sao lộ trình mẫu."""
    return SAMPLE[:]


def check_name(name):
    """Có sẵn. Tên điểm dừng đã bỏ khoảng trắng hai đầu; rỗng hoặc dài quá 40 ký tự báo ValueError."""
    name = name.strip()
    if not name or len(name) > 40:
        raise ValueError("Tên điểm dừng phải có từ 1 đến 40 ký tự")
    return name


def insert_stop(route, pos, name):
    """Chèn điểm dừng vào vị trí pos (1 đến len(route) + 1), trả về số điểm phải dịch sang phải.
    Vị trí sai báo ValueError("Vị trí phải từ 1 đến <len + 1>"). Thêm một ô ở cuối rồi dịch từ cuối về vị trí cần chèn."""
    raise NotImplementedError


def remove_stop(route, pos):
    """Xóa điểm dừng ở vị trí pos (1 đến len(route)), trả về (tên điểm đã xóa, số điểm phải dịch sang trái).
    Lộ trình rỗng hoặc vị trí sai báo ValueError("Vị trí phải từ 1 đến <len>"). Dịch rồi bỏ ô cuối bằng pop()."""
    raise NotImplementedError


def reverse_range(route, i, j):
    """Đảo ngược đoạn route[i..j] (chỉ số tính từ 0, gồm cả hai đầu) tại chỗ bằng hai chỉ số; trả về số lần đổi chỗ."""
    raise NotImplementedError


def reverse_route(route):
    """Đảo ngược cả lộ trình tại chỗ, trả về số lần đổi chỗ."""
    raise NotImplementedError


def rotate_route(route, k):
    """Xoay lộ trình để bắt đầu từ điểm dừng thứ k (1 đến len(route)); các điểm trước nó chuyển xuống cuối, giữ thứ tự.
    Tại chỗ, không cắt lát, không tạo list mới: đảo đoạn đầu, đảo đoạn sau, rồi đảo cả list. Trả về số lần đổi chỗ.
    Vị trí sai báo ValueError("Vị trí phải từ 1 đến <len>")."""
    raise NotImplementedError
