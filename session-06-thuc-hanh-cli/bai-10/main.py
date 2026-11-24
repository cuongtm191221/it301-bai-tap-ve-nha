"""Chương trình menu dòng lệnh chốt ca KiotViet. Chạy: python main.py"""
from chot_ca import make_catalog, make_sales, close_fast, add_sale, benchmark

SIZES = (500, 1000, 2000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== KIOTVIET - CHỐT CA BÁN HÀNG =====")
    print("1. Xem danh mục đầu ca")
    print("2. Ghi giao dịch bán")
    print("3. Chốt ca")
    print("4. Đo bản cũ và bản mới")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
