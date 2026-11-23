"""Chương trình menu dòng lệnh bảng xếp hạng Liên Quân. Chạy: python main.py"""
from xep_hang import make_players, top_fast, rank_fast, find_player, apply_match, benchmark

SIZES = (500, 1000, 2000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== GARENA LIÊN QUÂN - BẢNG XẾP HẠNG MÙA 30 =====")
    print("1. Xem top k")
    print("2. Cập nhật điểm sau trận")
    print("3. Tra cứu hạng")
    print("4. Đo so sánh bản cũ và bản mới")
    print("5. Thoát")


def top_menu(players):
    """Chức năng 1: hỏi k (số nguyên dương), in top k "<hạng>. <tên> - <điểm> điểm"."""
    raise NotImplementedError


def match_menu(players):
    """Chức năng 2: hỏi tên và điểm trận; in điểm mới và hạng mới, hoặc "Lỗi: <thông báo>"."""
    raise NotImplementedError


def benchmark_menu():
    """Chức năng 4: in bảng thời gian tra hạng của bản cũ và bản mới với n = 500, 1.000, 2.000."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
