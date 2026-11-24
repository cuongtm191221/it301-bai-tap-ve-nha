"""Chương trình menu dòng lệnh quầy thu ngân Co.opmart. Chạy: python main.py"""
from quay_thu_ngan import make_store, join, serve, merge_v1, merge_v2, benchmark

SIZES = (500, 1000, 2000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== CO.OPMART - QUẦY THU NGÂN =====")
    print("1. Xem hai quầy")
    print("2. Khách vào quầy")
    print("3. Đóng quầy 2, chuyển khách sang quầy 1")
    print("4. Phục vụ khách")
    print("5. Đo so sánh hai giải pháp")
    print("6. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-6; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
