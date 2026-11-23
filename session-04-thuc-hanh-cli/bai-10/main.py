"""Chương trình menu dòng lệnh tách chuỗi tìm kiếm Điện Máy Xanh. Chạy: python main.py"""
from tach_tu_khoa import make_keywords, normalize, count_fast, best_split, add_keyword, benchmark

REPEATS = (6, 8, 10)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== ĐIỆN MÁY XANH - TÁCH CHUỖI TÌM KIẾM =====")
    print("1. Tách chuỗi tìm kiếm")
    print("2. Thêm từ khóa")
    print("3. Xem từ điển")
    print("4. Đo bản cũ và bản mới")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
