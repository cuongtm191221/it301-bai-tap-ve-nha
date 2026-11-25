"""Chương trình menu dòng lệnh đọc báo VnExpress. Chạy: python main.py"""
from doc_bao import Reader, visit, go_back, go_forward, history


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VNEXPRESS - ĐỌC BÁO =====")
    print("1. Xem bài đang đọc")
    print("2. Mở bài")
    print("3. Quay lại")
    print("4. Tiến tới")
    print("5. Xem lịch sử")
    print("6. Thoát")


def main():
    """Vòng lặp menu: đọc lựa chọn 1-6; lỗi dữ liệu in "Lỗi: <thông báo>"."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
