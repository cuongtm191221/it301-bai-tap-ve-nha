"""Chương trình menu dòng lệnh đối soát VNPAY. Chạy: python main.py"""
from doi_soat import make_books, money, add_tx, summary, reconcile_v1, reconcile_v2, benchmark

SIZES = (1000, 2000, 4000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VNPAY - ĐỐI SOÁT CUỐI NGÀY =====")
    print("1. Xem tóm tắt hai sổ")
    print("2. Thêm giao dịch")
    print("3. Đối soát")
    print("4. Đo so sánh hai giải pháp")
    print("5. Thoát")


def print_result(result):
    """In ba nhóm kết quả đối soát; nhóm rỗng in "(không có)"."""
    raise NotImplementedError


def add_menu(system, bank):
    """Chức năng 2, menu phụ: 1 sổ hệ thống, 2 sao kê ngân hàng; hỏi mã và số tiền."""
    raise NotImplementedError


def reconcile_menu(system, bank):
    """Chức năng 3, menu phụ: chọn giải pháp 1 hoặc 2 rồi in kết quả."""
    raise NotImplementedError


def benchmark_menu():
    """Chức năng 4: in bảng thời gian hai giải pháp với n = 1.000, 2.000, 4.000."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
