"""Chương trình menu dòng lệnh lộ trình tài xế Ahamove. Chạy: python main.py"""
from lo_trinh import make_route, insert_stop, remove_stop, reverse_route, rotate_route


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== AHAMOVE - LỘ TRÌNH HÔM NAY =====")
    print("1. Xem lộ trình")
    print("2. Chèn điểm dừng")
    print("3. Xóa điểm dừng")
    print("4. Sắp lại lộ trình")
    print("5. Thoát")


def read_pos(prompt):
    """Đọc vị trí là số nguyên; không phải số nguyên báo ValueError("Vị trí phải là số nguyên")."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
