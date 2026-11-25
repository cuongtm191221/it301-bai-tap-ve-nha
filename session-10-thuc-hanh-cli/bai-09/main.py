"""Chương trình menu dòng lệnh soạn văn bản VNPT Smart Office. Chạy: python main.py"""
from soan_van_ban import FastEditor, make_editor, benchmark

SIZES = (500, 1000, 2000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VNPT SMART OFFICE - SOẠN VĂN BẢN =====")
    print("1. Xem văn bản")
    print("2. Thêm dòng")
    print("3. Sửa dòng")
    print("4. Xóa dòng")
    print("5. Hoàn tác")
    print("6. Làm lại")
    print("7. Đo bản cũ và bản mới")
    print("8. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-8; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
