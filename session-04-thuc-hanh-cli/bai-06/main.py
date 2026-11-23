"""Chương trình menu dòng lệnh xếp pallet kho Vinamilk. Chạy: python main.py"""
from xep_pallet import ways, count_calls, layouts, parse_length, benchmark

SIZES = (20, 24, 28)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VINAMILK BÌNH DƯƠNG - XẾP PALLET =====")
    print("1. Số cách xếp một dãy kệ")
    print("2. Số lời gọi của bản không nhớ")
    print("3. Liệt kê các cách xếp")
    print("4. Đo bản không nhớ và bản lru_cache")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
