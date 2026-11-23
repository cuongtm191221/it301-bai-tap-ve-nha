"""Chương trình menu dòng lệnh kiểm tra mã vận đơn J&T Express. Chạy: python main.py"""
from van_don import make_parcels, normalize, is_valid, check_digit, invalid_codes, receive


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== J&T EXPRESS - BƯU CỤC THỦ ĐỨC =====")
    print("1. Kiểm tra mã vận đơn")
    print("2. Nhận đơn")
    print("3. Kiểm tra lô mã của đối tác")
    print("4. Xem đơn đã nhận")
    print("5. Thoát")


def check_menu():
    """Chức năng 1, menu phụ: 1 kiểm tra một mã; 2 tính chữ số kiểm tra cho 9 chữ số đầu."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
