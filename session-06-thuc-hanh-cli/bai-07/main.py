"""Chương trình menu dòng lệnh minigame Shopee. Chạy: python main.py"""
from lac_xu import make_turns, add_turn, unique_v1, unique_v2, count_turns, benchmark

SIZES = (2000, 4000, 8000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== SHOPEE - MINIGAME LẮC XU =====")
    print("1. Ghi lượt tham gia")
    print("2. Danh sách người chơi")
    print("3. Số lượt của một người")
    print("4. Đo so sánh hai giải pháp")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
