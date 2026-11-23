"""Chương trình menu dòng lệnh quầy đổi tiền Tết Vietcombank. Chạy: python main.py"""
from doi_tien import money, parse_amount, count_ways_v1, count_ways_v2, fewest_notes, benchmark

AMOUNTS = (500000, 1000000, 1500000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VIETCOMBANK HOÀN KIẾM - ĐỔI TIỀN MỚI =====")
    print("1. Phương án ít tờ nhất")
    print("2. Số cách đổi")
    print("3. Lịch sử đổi trong phiên")
    print("4. Đo so sánh hai giải pháp")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
