"""Tra cứu đơn hàng theo mã trên Shopee."""


def find_order(orders, code):
    # Trả về (vị trí của đơn có mã code, số đơn đã xét).
    # Đơn "Đã hủy" coi như không có. Không tìm thấy thì trả về (None, số đơn đã xét).
    i = 0
    checked = 0
    while i < len(orders) - 1:
        if orders[i]["status"] == "Đã hủy":
            continue
        checked += 1
        if orders[i]["code"] == code:
            return i, checked
        i += 1
    return -1, checked


if __name__ == "__main__":
    today = [
        {"code": "DH1001", "status": "Đang giao"},
        {"code": "DH1002", "status": "Đã giao"},
        {"code": "DH1003", "status": "Chờ lấy hàng"},
        {"code": "DH1004", "status": "Đang giao"},
    ]
    print("Tra DH1002:", find_order(today, "DH1002"))
    print("Tra DH1004:", find_order(today, "DH1004"))
    print("Tra DH9999:", find_order(today, "DH9999"))
    print("Danh sách rỗng:", find_order([], "DH1001"))

    week = [
        {"code": "DH0901", "status": "Đã giao"},
        {"code": "DH0902", "status": "Đã hủy"},
        {"code": "DH0903", "status": "Đang giao"},
    ]
    print("Tra DH0903:", find_order(week, "DH0903"))
    print("Tra DH0902:", find_order(week, "DH0902"))
