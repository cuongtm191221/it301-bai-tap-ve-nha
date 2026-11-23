"""Chương trình menu dòng lệnh quầy check-in Vietjet. Chạy: python main.py"""
from check_in import (make_passengers, format_passenger, normalize_code, parse_count, first_k, last_k,
                      find_linear, find_early_stop, check_in, baggage_stats, BAGGAGE_LIMIT)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VIETJET VJ123 - QUẦY CHECK-IN =====")
    print("1. Xem danh sách hành khách")
    print("2. Check-in hành khách")
    print("3. Tra cứu mã đặt chỗ")
    print("4. Thống kê hành lý")
    print("5. Thoát")


def print_list(passengers):
    """In mỗi hành khách một dòng "<số thứ tự>. <thông tin>"."""
    raise NotImplementedError


def view_menu(passengers):
    """Chức năng 1, menu phụ: 1 toàn bộ, 2 k người đầu, 3 k người cuối (hỏi k)."""
    raise NotImplementedError


def checkin_menu(passengers):
    """Chức năng 2: hỏi mã, họ tên, hành lý; in vị trí trong danh sách hoặc "Lỗi: <thông báo>"."""
    raise NotImplementedError


def find_menu(passengers):
    """Chức năng 3, menu phụ: 1 tìm tuần tự, 2 tìm có dừng sớm; in kết quả kèm số lần so sánh."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
