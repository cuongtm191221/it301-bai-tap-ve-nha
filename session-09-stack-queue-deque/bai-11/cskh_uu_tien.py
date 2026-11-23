"""Hàng chờ chăm sóc khách hàng Tiki có ưu tiên khách TikiNOW (VIP) nhưng không bỏ quên khách thường."""


from collections import deque

VIP_STREAK = 3


class PriorityDesk:
    """Hai hàng chờ: khách VIP (TikiNOW) và khách thường; VIP được phục vụ trước, nhưng sau 3 khách VIP liên tiếp mà có khách thường đang chờ thì phục vụ một khách thường."""

    def __init__(self):
        self.vip = deque()
        self.normal = deque()

    def add(self, code, is_vip=False):
        """Thêm khách vào cuối hàng tương ứng; mã đã có trong một trong hai hàng thì trả False."""
        raise NotImplementedError

    def serve(self):
        """Mã khách được phục vụ tiếp theo theo quy tắc ưu tiên; cả hai hàng rỗng trả None."""
        raise NotImplementedError

    def waiting(self):
        """Bộ (số khách VIP đang chờ, số khách thường đang chờ)."""
        raise NotImplementedError


def serve_all(desk):
    """List mã khách theo thứ tự được phục vụ cho tới khi hết hàng."""
    raise NotImplementedError


if __name__ == "__main__":
    desk = PriorityDesk()
    for code in ("T1", "T2"):
        desk.add(code)
    for code in ("V1", "V2", "V3", "V4", "V5"):
        desk.add(code, is_vip=True)
    print("Thêm trùng V2:", desk.add("V2", is_vip=True), "| đang chờ (VIP, thường):", desk.waiting())
    print("Thứ tự phục vụ:", serve_all(desk))
    only_vip = PriorityDesk()
    for k in range(5):
        only_vip.add(f"V{k}", is_vip=True)
    print("Chỉ có VIP:", serve_all(only_vip))
