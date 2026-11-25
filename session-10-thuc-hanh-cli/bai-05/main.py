"""Chương trình menu dòng lệnh hàng đợi thanh toán MoMo. Chạy: python main.py"""
from thanh_toan import make_queue, money, submit, process, bench_drain, memory_report

SIZES = (20000, 40000, 80000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== MOMO - HÀNG ĐỢI THANH TOÁN =====")
    print("1. Xem hàng đợi")
    print("2. Gửi yêu cầu")
    print("3. Xử lý yêu cầu")
    print("4. Đo ba cách cài hàng đợi")
    print("5. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
