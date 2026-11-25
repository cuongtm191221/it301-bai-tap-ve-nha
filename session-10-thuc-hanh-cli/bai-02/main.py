"""Chương trình menu dòng lệnh hàng chờ tổng đài Mobifone. Chạy: python main.py"""
from tong_dai import make_queue, incoming, answer, waiting


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== MOBIFONE - TỔNG ĐÀI 9090 =====")
    print("1. Xem hàng chờ")
    print("2. Có cuộc gọi đến")
    print("3. Nhận cuộc gọi")
    print("4. Xem cuộc gọi tiếp theo")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
