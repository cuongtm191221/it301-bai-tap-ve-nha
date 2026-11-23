"""Chương trình menu dòng lệnh bảng doanh số TGDĐ. Chạy: python main.py"""
from doanh_so import (make_staff, format_staff, add_sales, remove_staff, ranking, best_and_worst,
                      count_kpi, average_sales)

EMPTY = "Chưa có nhân viên nào."


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== TGDĐ QUẬN 7 - DOANH SỐ THÁNG =====")
    print("1. Xem bảng doanh số")
    print("2. Cập nhật nhân viên")
    print("3. Cao nhất và thấp nhất")
    print("4. Thống kê")
    print("5. Thoát")


def print_rows(rows):
    """In mỗi nhân viên một dòng có số thứ tự."""
    raise NotImplementedError


def view_menu(staff):
    """Chức năng 1, menu phụ: 1 theo thứ tự trong bảng, 2 xếp hạng doanh số giảm dần."""
    raise NotImplementedError


def update_menu(staff):
    """Chức năng 2, menu phụ: 1 cộng doanh số đơn mới, 2 xóa nhân viên nghỉ việc."""
    raise NotImplementedError


def stats_menu(staff):
    """Chức năng 4, menu phụ: 1 đếm nhân viên đạt KPI (hỏi ngưỡng), 2 doanh số trung bình."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
