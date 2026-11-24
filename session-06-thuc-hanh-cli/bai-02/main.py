"""Chương trình menu dòng lệnh sơ đồ ghế CGV. Chạy: python main.py"""
from ghe_cgv import make_sample_hall, render, book, cancel, free_count, find_block


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== CGV VINCOM BÀ TRIỆU - PHÒNG 3 =====")
    print("1. Xem sơ đồ ghế")
    print("2. Đặt ghế")
    print("3. Hủy ghế")
    print("4. Tìm ghế ngồi cùng nhau")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
