"""Chương trình menu dòng lệnh bảng thông báo Tiki. Chạy: python main.py"""
from thong_bao import make_feed, push, latest, notice_at, bench_front, bench_index

FRONT_SIZES = (10000, 20000, 40000)
INDEX_SIZES = (2000, 4000, 8000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== TIKI - THÔNG BÁO ĐƠN HÀNG =====")
    print("1. Xem các thông báo mới nhất")
    print("2. Thêm thông báo")
    print("3. Xem thông báo theo thứ tự")
    print("4. Đo so sánh với list")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
