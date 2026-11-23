"""Chương trình menu dòng lệnh sổ đơn The Coffee House. Chạy: python main.py"""
from bao_cao_ca import DRINKS, make_orders, report_fast, add_order, find_order, benchmark

SIZES = (5000, 10000, 20000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== THE COFFEE HOUSE HỒ CON RÙA - SỔ ĐƠN =====")
    print("1. Ghi đơn mới")
    print("2. Báo cáo cuối ca")
    print("3. Tra cứu đơn")
    print("4. Đo so sánh bản cũ và bản mới")
    print("5. Thoát")


def add_menu(orders):
    """Chức năng 1: in thực đơn đánh số, hỏi số thứ tự món và số ly; in đơn mới hoặc "Lỗi: <thông báo>"."""
    raise NotImplementedError


def report_menu(orders):
    """Chức năng 2: báo cáo bằng report_fast với top = 3."""
    raise NotImplementedError


def benchmark_menu():
    """Chức năng 4: in bảng thời gian bản cũ và bản mới với n = 5.000, 10.000, 20.000."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
