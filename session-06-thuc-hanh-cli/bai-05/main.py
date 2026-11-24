"""Chương trình menu dòng lệnh sao kê MB Bank. Chạy: python main.py"""
import sys
from sao_ke import make_txs, money, add_tx, latest_first, capacity_steps, benchmark

SIZES = (20000, 40000, 80000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== MB BANK - SAO KÊ TÀI KHOẢN =====")
    print("1. Xem sao kê gần nhất")
    print("2. Ghi giao dịch")
    print("3. Quan sát dung lượng list")
    print("4. Đo bản cũ và bản mới")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
