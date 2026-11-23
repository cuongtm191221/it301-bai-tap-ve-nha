"""Chương trình menu dòng lệnh thưởng chuỗi ngày mua Bách Hóa Xanh. Chạy: python main.py"""
from chuoi_ngay import make_days, make_big_days, to_text, report_fast, add_day, benchmark, slow_fails

SIZES = (200, 400, 800)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== BÁCH HÓA XANH - THƯỞNG CHUỖI NGÀY MUA =====")
    print("1. Xem các ngày mua gần nhất")
    print("2. Ghi ngày mua")
    print("3. Báo cáo chuỗi và điểm thưởng")
    print("4. Đo bản cũ và bản mới")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
