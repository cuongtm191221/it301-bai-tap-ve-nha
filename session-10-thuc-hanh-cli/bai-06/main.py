"""Chương trình menu dòng lệnh màn hình bếp Jollibee. Chạy: python main.py"""
from man_hinh_bep import make_board, add_order, finish, bench_window

SIZES = (1000, 2000, 4000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== JOLLIBEE - MÀN HÌNH BẾP =====")
    print("1. Xem màn hình")
    print("2. Thêm đơn")
    print("3. Bếp làm xong đơn")
    print("4. Đo ba cách giữ N đơn gần nhất")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
