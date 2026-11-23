"""Sổ giá vốn hàng tồn kho theo lô cho người bán trên Tiki."""


class StockLedger:
    """Sổ kho một mã hàng, lưu các lô nhập (số lượng, đơn giá). method = "FIFO" (xuất lô nhập trước) hoặc "LIFO" (xuất lô nhập sau)."""

    def __init__(self, method):
        if method not in ("FIFO", "LIFO"):
            raise ValueError("Phương pháp không hỗ trợ")
        self.method = method

    def on_hand(self):
        """Tổng số lượng đang tồn."""
        raise NotImplementedError

    def stock_value(self):
        """Giá trị hàng tồn (đồng) = tổng số lượng còn × đơn giá của từng lô."""
        raise NotImplementedError

    def receive(self, qty, unit_cost):
        """Nhập một lô; qty và unit_cost phải là số nguyên dương, sai báo ValueError("Số lượng và đơn giá phải là số nguyên dương")."""
        raise NotImplementedError

    def issue(self, qty):
        """Xuất qty sản phẩm, trả về giá vốn (đồng). qty không phải số nguyên dương báo ValueError("Số lượng xuất phải là số nguyên dương"); thiếu hàng báo ValueError("Không đủ hàng: còn <n>") và sổ giữ nguyên."""
        raise NotImplementedError

    def lots(self):
        """List các bộ (số lượng còn, đơn giá) theo thứ tự nhập."""
        raise NotImplementedError


def cost_report(method, events):
    """events: list bộ ("IN", qty, unit_cost) hoặc ("OUT", qty). Trả về dòng "<method>: giá vốn <tổng>đ, tồn <n> sp trị giá <giá trị>đ"; gặp lỗi thì trả "<method>: lỗi ở bước <k>: <thông báo>" (k đếm từ 1)."""
    raise NotImplementedError


if __name__ == "__main__":
    events = [("IN", 10, 100000), ("IN", 5, 120000), ("OUT", 12), ("IN", 8, 130000), ("OUT", 6)]
    for method in ("FIFO", "LIFO"):
        print(cost_report(method, events))
    ledger = StockLedger("FIFO")
    ledger.receive(10, 100000)
    ledger.receive(5, 120000)
    print("Xuất 12, giá vốn:", ledger.issue(12), "| lô còn lại:", ledger.lots())
    print(cost_report("FIFO", [("IN", 3, 50000), ("OUT", 5)]))
    print(cost_report("FIFO", [("IN", 0, 50000)]))
