"""Báo cáo cuối ngày của sàn Shopee. Hàm daily_report là bản đang chạy; bạn viết daily_report_fast."""


def daily_report(orders):
    """Có sẵn: bản đang chạy. orders là list dict {"code", "buyer", "amount"}. Không sửa hàm này."""
    total = 0
    for o in orders:
        total += o["amount"]

    buyers = []
    for o in orders:
        if o["buyer"] not in buyers:
            buyers.append(o["buyer"])

    best_buyer, best_spent = None, -1
    for b in buyers:
        spent = 0
        for o in orders:
            if o["buyer"] == b:
                spent += o["amount"]
        if spent > best_spent:
            best_buyer, best_spent = b, spent

    big = []
    for o in orders:
        average = sum(x["amount"] for x in orders) / len(orders)
        if o["amount"] > 2 * average:
            big.append(o["code"])

    orders.sort(key=lambda o: o["amount"], reverse=True)
    return {"total": total, "buyers": len(buyers), "best_buyer": best_buyer,
            "big_orders": big, "largest": orders[0]["code"]}


def daily_report_fast(orders):
    """Bản bạn viết: cùng kết quả với daily_report, chạy 200.000 đơn trong 3 giây, không sửa orders (xem đề, mục 2)."""
    raise NotImplementedError


if __name__ == "__main__":
    def sample():
        return [
            {"code": "DH01", "buyer": "an", "amount": 300000},
            {"code": "DH02", "buyer": "binh", "amount": 1500000},
            {"code": "DH03", "buyer": "an", "amount": 200000},
            {"code": "DH04", "buyer": "chi", "amount": 250000},
            {"code": "DH05", "buyer": "binh", "amount": 100000},
            {"code": "DH06", "buyer": "dung", "amount": 1600000},
            {"code": "DH07", "buyer": "an", "amount": 150000},
        ]
    orders = sample()
    print("Bản đang chạy:", daily_report(orders))
    print("Thứ tự đơn sau khi chạy:", [o["code"] for o in orders])
    orders = sample()
    print("Bản của bạn:  ", daily_report_fast(orders))
    print("Thứ tự đơn sau khi chạy:", [o["code"] for o in orders])
    print("Ngày chưa có đơn:", daily_report_fast([]))
