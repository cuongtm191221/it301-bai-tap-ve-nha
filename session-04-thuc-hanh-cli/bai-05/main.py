"""Chương trình menu dòng lệnh lịch sử ví ZaloPay. Chạy: python main.py"""
from vi_dien_tu import make_txs, make_big_txs, money, balance, largest_spend, add_tx, benchmark, recursion_fails

SIZES = (200, 400, 800)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== ZALOPAY - LỊCH SỬ VÍ =====")
    print("1. Xem số dư và khoản chi lớn nhất")
    print("2. Nạp hoặc chi")
    print("3. Nạp lịch sử dài (giả lập)")
    print("4. Đo đệ quy và vòng lặp")
    print("5. Thoát")


def summary(txs):
    """Chức năng 1: in "Số dư: <tiền> (tính bằng <cách>, <n> giao dịch)" và khoản chi lớn nhất."""
    raise NotImplementedError


def benchmark_menu():
    """Chức năng 4: bảng thời gian với n = 200, 400, 800 và kết quả thử đệ quy với 5.000 giao dịch."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
