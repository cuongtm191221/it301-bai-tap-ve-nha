"""Chương trình menu dòng lệnh báo cáo ca trụ bơm Petrolimex. Chạy: python main.py"""
from nhat_ky_bom import FUELS, make_log, liters_text, parse_liters, record, report_fast, benchmark

SIZES = (500, 1000, 2000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== PETROLIMEX - BÁO CÁO CA TRỤ BƠM =====")
    print("1. Xem nhật ký bơm")
    print("2. Ghi lần bơm")
    print("3. Báo cáo ca")
    print("4. Đo bản cũ và bản mới")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
