"""Chương trình menu dòng lệnh hệ số giá cước Be. Chạy: python main.py"""
from gia_cuoc import make_counts, record, parse_window, report, benchmark

WINDOWS = (100, 200, 400)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== BE - HỆ SỐ GIÁ THEO NHU CẦU =====")
    print("1. Xem 10 phút gần nhất")
    print("2. Ghi số cuốc phút mới")
    print("3. Đổi cửa sổ (số phút)")
    print("4. Đo bản cũ và bản mới")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
