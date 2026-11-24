"""Nghiệp vụ dọn lịch hẹn khám đã hủy của bệnh viện Vinmec.

Lịch hẹn là tuple (mã, tên bệnh nhân, trạng thái), trạng thái là "chờ khám" hoặc "đã hủy".
Danh sách lịch hẹn là list theo thứ tự đặt. Không dùng dict, set.
"""
import timeit

WAITING = "chờ khám"
CANCELLED = "đã hủy"
SAMPLE = [
    ("VM001", "Nguyễn An", WAITING), ("VM002", "Trần Bình", CANCELLED), ("VM003", "Lê Chi", CANCELLED),
    ("VM004", "Phạm Dũng", WAITING), ("VM005", "Hoàng Em", CANCELLED), ("VM006", "Vũ Giang", WAITING),
]


def make_appointments():
    """Có sẵn. Trả về bản sao các lịch hẹn mẫu."""
    return SAMPLE[:]


def make_big_appointments(n):
    """Có sẵn. n lịch hẹn giả lập, cứ 3 lịch có 1 lịch đã hủy."""
    return [("VM%06d" % k, "Bệnh nhân", CANCELLED if k % 3 == 0 else WAITING) for k in range(n)]


def book(appointments, name):
    """Đặt lịch cho bệnh nhân (tên bỏ khoảng trắng hai đầu, trống báo ValueError("Tên bệnh nhân không được để trống")).
    Mã mới = "VM" + số lớn nhất đang có cộng 1, đủ 3 chữ số (danh sách rỗng: VM001). Trả về mã mới."""
    raise NotImplementedError


def cancel(appointments, code):
    """Chuyển lịch sang "đã hủy". Không có mã: ValueError("Không tìm thấy lịch hẹn"); đã hủy rồi: ValueError("Lịch hẹn đã hủy trước đó")."""
    raise NotImplementedError


def clean_v1(appointments):
    """Giải pháp 1. Xóa mọi lịch "đã hủy" ngay trên list (giữ thứ tự lịch còn lại). Trả về số lịch đã xóa."""
    raise NotImplementedError


def clean_v2(appointments):
    """Giải pháp 2: cùng kết quả với giải pháp 1, cách làm khác, nhanh hơn rõ rệt; 200.000 lịch trong 1 giây."""
    raise NotImplementedError


def benchmark(sizes, number=1):
    """Với từng n trong sizes, trên bản mới make_big_appointments(n) cho mỗi lần đo: đo bằng timeit mỗi giải pháp (ms). Trả về list bộ (n, ms 1, ms 2)."""
    raise NotImplementedError
