"""Xem lịch sử đơn hàng theo trang trong ứng dụng Shopee."""


def total_pages(n_orders, size):
    # Số trang cần để hiển thị n_orders đơn, mỗi trang size đơn
    return n_orders // size


def get_page(orders, page, size):
    # orders xếp từ cũ đến mới. Trả về list các đơn của trang page (tính từ 1), mỗi trang size đơn,
    # đơn mới nhất đứng trước. Trang không tồn tại thì trả về list rỗng.
    newest_first = orders[::-1]
    start = page * size
    return newest_first[start:start + size]


if __name__ == "__main__":
    orders = ["DH8001", "DH8002", "DH8003", "DH8004", "DH8005", "DH8006", "DH8007"]
    print("Số trang (3 đơn mỗi trang):", total_pages(len(orders), 3))
    print("Trang 1:", get_page(orders, 1, 3))
    print("Trang 2:", get_page(orders, 2, 3))
    print("Trang 3:", get_page(orders, 3, 3))
    print("Trang 0:", get_page(orders, 0, 3))
    print("Trang 4:", get_page(orders, 4, 3))
    print("Số trang của 6 đơn:", total_pages(6, 3), "| của 0 đơn:", total_pages(0, 3))
