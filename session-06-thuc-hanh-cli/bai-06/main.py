"""Chương trình menu dòng lệnh theo dõi giá cổ phiếu SSI. Chạy: python main.py"""
from gia_co_phieu import make_prices, money, add_price, recent_average, best_trade, benchmark

SIZES = (50000, 100000, 200000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== SSI IBOARD - THEO DÕI GIÁ FPT =====")
    print("1. Thêm giá phiên mới")
    print("2. Xem k phiên gần nhất")
    print("3. Thời điểm mua bán tốt nhất trong quá khứ")
    print("4. Đo hiệu năng")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
