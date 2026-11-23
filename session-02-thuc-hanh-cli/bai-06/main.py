"""Chương trình menu dòng lệnh sổ quỹ Circle K. Chạy: python main.py"""
from so_quy import make_book, money, balance, running_balances, add_tx, totals, top_expenses, benchmark

SIZES = (20000, 40000, 80000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== CIRCLE K LÊ LỢI - SỔ QUỸ TRONG CA =====")
    print("1. Xem sổ quỹ")
    print("2. Ghi giao dịch")
    print("3. Báo cáo")
    print("4. Đo hiệu năng")
    print("5. Thoát")


def format_tx(tx):
    """Một dòng giao dịch: "GD001 | THU | 450.000đ"."""
    raise NotImplementedError


def view_menu(book):
    """Chức năng 1, menu phụ: 1 toàn bộ kèm số dư sau mỗi giao dịch; 2 k giao dịch gần nhất (mới nhất trước)."""
    raise NotImplementedError


def add_menu(book):
    """Chức năng 2: hỏi loại và số tiền; in mã mới và số dư hoặc "Lỗi: <thông báo>"."""
    raise NotImplementedError


def report_menu(book):
    """Chức năng 3, menu phụ: 1 tổng thu, tổng chi, số dư; 2 top 3 khoản chi lớn nhất."""
    raise NotImplementedError


def benchmark_menu():
    """Chức năng 4: in bảng thời gian tính số dư và kích thước list sổ với n = 20.000, 40.000, 80.000."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
