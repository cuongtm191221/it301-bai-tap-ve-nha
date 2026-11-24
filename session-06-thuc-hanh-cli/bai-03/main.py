"""Chương trình menu dòng lệnh đơn thuốc online Pharmacity. Chạy: python main.py"""
from don_thuoc import make_orders, money, add_order, cancel_order, drop_cancelled, merge_duplicates, reverse_in_place


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== PHARMACITY - ĐƠN ONLINE TRONG NGÀY =====")
    print("1. Xem danh sách đơn")
    print("2. Nhận đơn")
    print("3. Hủy đơn")
    print("4. Dọn danh sách")
    print("5. Thoát")


def show_orders(orders):
    """Chức năng 1: "<i>. <mã> | <trạng thái> | <tiền>" từng đơn, rồi "Tổng: <n> đơn"; rỗng in "Chưa có đơn nào."."""
    raise NotImplementedError


def clean_menu(orders):
    """Chức năng 4, menu phụ: 1 bỏ đơn hủy, 2 gộp đơn trùng liền nhau, 3 đảo thứ tự (mới nhất lên đầu)."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
