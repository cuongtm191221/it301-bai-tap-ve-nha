"""Chương trình menu dòng lệnh cho bưu cục GHTK. Chạy: python main.py"""
from don_hang import make_orders, money, format_order, total_cod, find_order, add_order, count_by_district


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== BƯU CỤC GHTK - ĐƠN GIAO TRONG NGÀY =====")
    print("1. Xem danh sách đơn và tổng tiền thu hộ")
    print("2. Thêm đơn mới")
    print("3. Tra cứu đơn theo mã")
    print("4. Đếm đơn theo quận")
    print("5. Thoát")


def show_orders(orders):
    """Chức năng 1: in danh sách có số thứ tự và dòng tổng; danh sách rỗng in "Danh sách đơn đang trống."."""
    raise NotImplementedError


def add_menu(orders):
    """Chức năng 2: hỏi mã, người nhận, quận, tiền thu hộ; in kết quả hoặc "Lỗi: <thông báo>"."""
    raise NotImplementedError


def find_menu(orders):
    """Chức năng 3: hỏi mã đơn, in đơn tìm thấy hoặc thông báo không tìm thấy, kèm số mã đã so sánh."""
    raise NotImplementedError


def district_menu(orders):
    """Chức năng 4: hỏi tên quận, in số đơn; tên trống in "Lỗi: Quận không được để trống"."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5, gọi chức năng tương ứng; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
