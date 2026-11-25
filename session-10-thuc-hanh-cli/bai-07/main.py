"""Chương trình menu dòng lệnh hàng chờ cáp treo Vinpearl. Chạy: python main.py"""
from cap_treo import QueueV1, QueueV2, make_station, join, board, switch, benchmark

SIZES = (20000, 40000, 80000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VINPEARL - CÁP TREO =====")
    print("1. Xem hàng chờ")
    print("2. Khách xếp hàng")
    print("3. Cabin rời ga")
    print("4. Chọn giải pháp hàng chờ")
    print("5. Đo so sánh hai giải pháp")
    print("6. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-6; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
