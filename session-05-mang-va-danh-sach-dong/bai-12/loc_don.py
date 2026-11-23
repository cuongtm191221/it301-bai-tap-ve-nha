"""Dọn danh sách đơn GrabFood của nhà hàng tại chỗ."""


def is_cancelled(status):
    """Có sẵn. True nếu trạng thái là đã hủy (không phân biệt hoa thường, bỏ khoảng trắng hai đầu)."""
    return status.strip().upper() == "CANCELLED"


def remove_cancelled(orders):
    """Xóa tại chỗ mọi đơn đã hủy khỏi orders (list các bộ (mã, trạng thái)), giữ thứ tự đơn còn lại; trả về số đơn đã xóa."""
    raise NotImplementedError


def keep_last(orders, k):
    """Chỉ giữ k đơn mới nhất (cuối list) tại chỗ, theo đúng thứ tự; trả về số đơn đã bỏ."""
    raise NotImplementedError


def cleanup_message(orders, k):
    """Dọn đơn đã hủy rồi giữ k đơn mới nhất; trả về dòng thông báo."""
    raise NotImplementedError


if __name__ == "__main__":
    orders = [("GF1", "DONE"), ("GF2", "CANCELLED"), ("GF3", " cancelled "), ("GF4", "DONE"),
              ("GF5", "PENDING"), ("GF6", "Cancelled"), ("GF7", "DONE")]
    same = orders
    print("Xóa đơn hủy:", remove_cancelled(orders), "|", orders)
    print("Giữ 3 đơn mới nhất:", keep_last(orders, 3), "|", orders)
    print("Vẫn là cùng một list:", same is orders)
    big = [(f"GF{k}", "CANCELLED" if k % 3 == 0 else "DONE") for k in range(200000)]
    print(cleanup_message(big, 1000), "| đơn đầu:", big[0][0])
