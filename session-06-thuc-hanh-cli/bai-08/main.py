"""Chương trình menu dòng lệnh lịch hẹn Vinmec. Chạy: python main.py"""
from lich_hen import make_appointments, book, cancel, clean_v1, clean_v2, benchmark

SIZES = (10000, 20000, 40000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VINMEC - LỊCH HẸN KHÁM =====")
    print("1. Đặt lịch")
    print("2. Hủy lịch")
    print("3. Dọn lịch đã hủy")
    print("4. Xem lịch hẹn")
    print("5. Đo so sánh hai giải pháp")
    print("6. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-6; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
