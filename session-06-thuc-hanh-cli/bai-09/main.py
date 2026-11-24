"""Chương trình menu dòng lệnh chia chuyến giao hàng Sendo. Chạy: python main.py"""
from chia_chuyen import make_orders, money, batch_fast, add_order, benchmark, SIZE_ERROR

SIZES = (2000, 4000, 8000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== SENDO - CHIA CHUYẾN GIAO HÀNG =====")
    print("1. Xem đơn chờ giao")
    print("2. Thêm đơn")
    print("3. Chia chuyến")
    print("4. Đo bản cũ và bản mới")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
