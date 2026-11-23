"""Chương trình menu dòng lệnh nhật ký quẹt thẻ Viettel Tower. Chạy: python main.py"""
from quet_the import make_logs, to_text, latest, add_swipe, count_card, busiest_hour, benchmark

SIZES = (20000, 40000, 80000)


def show_menu():
    """Có sẵn. In menu chính."""
    print()
    print("===== VIETTEL TOWER - NHẬT KÝ QUẸT THẺ =====")
    print("1. Xem các lượt quẹt gần nhất")
    print("2. Ghi lượt quẹt mới")
    print("3. Tra cứu")
    print("4. Đo hiệu năng")
    print("5. Thoát")


def latest_menu(logs):
    """Chức năng 1: hỏi số lượt k (số nguyên dương), in k lượt gần nhất "<i>. <HH:MM> | <mã thẻ>"."""
    raise NotImplementedError


def add_menu(logs):
    """Chức năng 2: hỏi mã thẻ, giờ quẹt; in kết quả hoặc "Lỗi: <thông báo>"."""
    raise NotImplementedError


def search_menu(logs):
    """Chức năng 3, menu phụ: 1 số lượt của một thẻ, 2 giờ đông nhất."""
    raise NotImplementedError


def benchmark_menu():
    """Chức năng 4: in bảng thời gian của hai thao tác với n = 20.000, 40.000, 80.000 và tỉ lệ so với n trước đó."""
    raise NotImplementedError


def main():
    """Vòng lặp menu: đọc lựa chọn 1-5; lựa chọn sai in thông báo và hỏi lại."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
