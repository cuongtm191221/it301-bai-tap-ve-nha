"""Chương trình menu dòng lệnh tiết kiệm tích lũy Techcombank. Chạy: python main.py"""
from tiet_kiem import money, parse_money, parse_rate, balance_after, months_to_reach, yearly_table


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== TECHCOMBANK - TIẾT KIỆM TÍCH LŨY =====")
    print("1. Nhập tiền gửi và lãi suất")
    print("2. Số dư sau n tháng")
    print("3. Số tháng để đạt mục tiêu")
    print("4. Bảng số dư cuối mỗi năm")
    print("5. Thoát")


def read_count(prompt, low, high, message):
    """Đọc một số nguyên từ low đến high; sai báo ValueError(message)."""
    raise NotImplementedError


def main():
    """Vòng lặp menu. Chức năng 2-4 cần nhập thông tin ở chức năng 1 trước."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
