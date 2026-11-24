"""Chương trình menu dòng lệnh hàng chờ bưu cục Viettel Post. Chạy: python main.py"""
from hang_cho import make_line, take_ticket, call_next, position, leave


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VIETTEL POST - HÀNG CHỜ NHẬN HÀNG =====")
    print("1. Xem hàng chờ")
    print("2. Lấy số")
    print("3. Gọi khách tiếp theo")
    print("4. Tra vị trí")
    print("5. Khách bỏ về")
    print("6. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-6; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
