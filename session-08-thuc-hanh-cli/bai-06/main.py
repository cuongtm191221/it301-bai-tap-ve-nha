"""Chương trình menu dòng lệnh lệnh chuyển tiền chờ Agribank. Chạy: python main.py"""
from lenh_cho import make_line, money, submit, pending_total, process, bench_drain, memory_per_item

SIZES = (10000, 20000, 40000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== AGRIBANK - LỆNH CHUYỂN TIỀN CHỜ XỬ LÝ =====")
    print("1. Xem lệnh chờ")
    print("2. Nhập lệnh")
    print("3. Xử lý lệnh")
    print("4. Đo so sánh với list")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
