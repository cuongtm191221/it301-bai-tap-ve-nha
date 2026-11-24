"""Chương trình menu dòng lệnh quầy thuốc Long Châu. Chạy: python main.py"""
from quay_thuoc import make_shelf, receive, sell


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== NHÀ THUỐC LONG CHÂU - QUẦY THUỐC =====")
    print("1. Xem quầy thuốc")
    print("2. Nhập thuốc")
    print("3. Tra cứu thuốc")
    print("4. Bán thuốc")
    print("5. Thoát")


def show_shelf(shelf):
    """Chức năng 1: mỗi thuốc một dòng "<i>. <mã> | <tên> | <số hộp> hộp", rồi "Đang lưu <size>/<capacity> ô, đã chép <copies> lần"."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
