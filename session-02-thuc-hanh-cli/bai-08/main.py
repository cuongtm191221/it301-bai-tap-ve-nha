"""Chương trình menu dòng lệnh kiểm tra voucher Lazada. Chạy: python main.py"""
from voucher import make_vouchers, issue, total_value, find_duplicates_v1, find_duplicates_v2, benchmark

SIZES = (1000, 2000, 4000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== LAZADA - KIỂM TRA VOUCHER ĐỢT 11.11 =====")
    print("1. Xem lô voucher")
    print("2. Phát thêm voucher")
    print("3. Kiểm tra mã trùng")
    print("4. Đo so sánh hai giải pháp")
    print("5. Thoát")


def view_menu(vouchers):
    """Chức năng 1, menu phụ: 1 toàn bộ kèm tổng giá trị; 2 k voucher phát gần nhất (mới nhất trước)."""
    raise NotImplementedError


def duplicate_menu(vouchers):
    """Chức năng 3, menu phụ: chọn giải pháp; in "Mã trùng: <mã> (<k> lần), ..." hoặc "Không có mã trùng."."""
    raise NotImplementedError


def benchmark_menu():
    """Chức năng 4: in bảng thời gian hai giải pháp với n = 1.000, 2.000, 4.000."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
