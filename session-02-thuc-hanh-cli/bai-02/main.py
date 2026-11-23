"""Chương trình menu dòng lệnh cho kho sách Fahasa. Chạy: python main.py"""
from kho_sach import make_books, money, format_book, stock_summary, find_book, add_stock, add_book, sell_book, top_stock


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== FAHASA NGUYỄN HUỆ - QUẢN LÝ KHO SÁCH =====")
    print("1. Xem kho sách")
    print("2. Nhập sách")
    print("3. Bán sách")
    print("4. Top 3 sách tồn nhiều nhất")
    print("5. Thoát")


def show_books(books):
    """Chức năng 1: mỗi đầu sách một dòng có số thứ tự, rồi dòng tổng; kho rỗng in "Kho sách đang trống."."""
    raise NotImplementedError


def receive_menu(books):
    """Chức năng 2: hỏi mã; mã đã có thì chỉ hỏi số lượng nhập thêm, mã mới thì hỏi tên, giá, số lượng."""
    raise NotImplementedError


def sell_menu(books):
    """Chức năng 3: hỏi mã và số lượng bán; in kết quả hoặc "Lỗi: <thông báo>"."""
    raise NotImplementedError


def top_menu(books):
    """Chức năng 4: in "Top 3 sách tồn nhiều nhất:" và các dòng có số thứ tự; kho rỗng in "Kho sách đang trống."."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5, gọi chức năng tương ứng; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
