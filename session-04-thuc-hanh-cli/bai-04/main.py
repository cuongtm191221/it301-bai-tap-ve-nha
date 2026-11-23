"""Chương trình menu dòng lệnh tiền điện tổ dân phố. Chạy: python main.py"""
from tien_dien import TIERS, make_customers, money, usage, bill, breakdown, total_bill, top_user, update_reading


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== EVN HÀ NỘI - TIỀN ĐIỆN TỔ DÂN PHỐ 12 =====")
    print("1. Xem tiền điện")
    print("2. Ghi chỉ số mới")
    print("3. Tổng tiền cả tổ")
    print("4. Hộ dùng nhiều điện nhất")
    print("5. Thoát")


def view_menu(customers):
    """Chức năng 1, menu phụ: 1 mọi hộ "<mã> | <tên> | <kWh> kWh | <tiền>"; 2 chi tiết từng bậc của một hộ."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
