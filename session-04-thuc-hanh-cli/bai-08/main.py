"""Chương trình menu dòng lệnh gợi ý combo GrabFood. Chạy: python main.py"""
from combo import make_menu, money, parse_budget, count_combos_v1, count_combos_v2, best_combo, benchmark

SIZES = (16, 18, 20)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== GRABFOOD - CƠM TẤM PHÚC LỘC THỌ =====")
    print("1. Xem thực đơn")
    print("2. Gợi ý combo sát ngân sách")
    print("3. Đếm số combo trong ngân sách")
    print("4. Đo so sánh hai giải pháp")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
