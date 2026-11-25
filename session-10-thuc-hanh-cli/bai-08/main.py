"""Chương trình menu dòng lệnh công thức khuyến mãi Haravan. Chạy: python main.py"""
from cong_thuc import Shop, money, eval_v1, eval_v2, set_formula, promo_prices, benchmark

SIZES = (1000, 2000, 4000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== HARAVAN - CÔNG THỨC KHUYẾN MÃI =====")
    print("1. Xem giá khuyến mãi")
    print("2. Đổi công thức")
    print("3. Thử công thức với một giá")
    print("4. Đo so sánh hai giải pháp")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
