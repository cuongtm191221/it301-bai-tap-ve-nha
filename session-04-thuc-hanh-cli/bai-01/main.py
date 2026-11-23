"""Chương trình menu dòng lệnh thẻ thành viên Highlands Coffee. Chạy: python main.py"""
from tich_diem import make_bills, money, total_points, count_big, largest, add_bill, tier


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== HIGHLANDS COFFEE - THẺ THÀNH VIÊN =====")
    print("1. Xem lịch sử và điểm")
    print("2. Thêm hóa đơn")
    print("3. Đếm hóa đơn lớn")
    print("4. Hóa đơn lớn nhất")
    print("5. Thoát")


def show_history(bills):
    """Chức năng 1: mỗi hóa đơn một dòng có số thứ tự, rồi "Điểm: <p> - Hạng: <hạng>"; rỗng in "Chưa có hóa đơn nào."."""
    raise NotImplementedError


def count_menu(bills):
    """Chức năng 3: hỏi ngưỡng (số nguyên dương), in "Có <k> hóa đơn từ <ngưỡng> trở lên."."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
