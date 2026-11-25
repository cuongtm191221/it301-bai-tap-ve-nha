"""Chương trình menu dòng lệnh soạn tin nhắn Zalo. Chạy: python main.py"""
from soan_tin import Draft, type_word, delete_word, undo, redo


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== ZALO - SOẠN TIN NHẮN =====")
    print("1. Xem tin nhắn")
    print("2. Gõ một từ")
    print("3. Xóa từ cuối")
    print("4. Hoàn tác")
    print("5. Làm lại")
    print("6. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-6; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
