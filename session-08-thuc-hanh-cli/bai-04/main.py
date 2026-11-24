"""Chương trình menu dòng lệnh lịch sử xem Galaxy Play. Chạy: python main.py"""
from lich_su_xem import make_history, watch, undo_last, import_old


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== GALAXY PLAY - LỊCH SỬ XEM =====")
    print("1. Xem lịch sử")
    print("2. Xem một phim")
    print("3. Xóa mục vừa xem")
    print("4. Nhập mục cũ từ thiết bị khác")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
