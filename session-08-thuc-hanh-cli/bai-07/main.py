"""Chương trình menu dòng lệnh hành trình Vietnam Airlines. Chạy: python main.py"""
from hanh_trinh import make_route, add_airport, reverse_v1, reverse_v2, benchmark

SIZES = (1000, 2000, 4000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VIETNAM AIRLINES - HÀNH TRÌNH NHIỀU CHẶNG =====")
    print("1. Xem hành trình")
    print("2. Thêm sân bay")
    print("3. Đảo chiều hành trình")
    print("4. Đo so sánh hai giải pháp")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
