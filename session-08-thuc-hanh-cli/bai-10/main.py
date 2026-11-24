"""Chương trình menu dòng lệnh nhật ký bút toán MISA. Chạy: python main.py"""
from but_toan import FastJournal, make_journal, money, record, undo, benchmark

SIZES = (500, 1000, 2000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== MISA - NHẬT KÝ BÚT TOÁN =====")
    print("1. Xem bút toán gần nhất")
    print("2. Ghi bút toán")
    print("3. Hoàn tác bút toán cuối")
    print("4. Xem số dư")
    print("5. Đo bản cũ và bản mới")
    print("6. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-6; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
