"""Bãi đỗ xe điện GrabBike nhiều hàng, nhiều cột tại trạm sạc."""


def make_lot(rows, cols):
    """Bãi đỗ rows hàng x cols cột, mỗi ô là None (trống); mỗi hàng là một list riêng. rows, cols phải là số nguyên dương, nếu không báo ValueError("Kích thước bãi không hợp lệ")."""
    raise NotImplementedError


def find(lot, code):
    """Bộ (hàng, cột) của xe có mã code; không có trả None."""
    raise NotImplementedError


def park(lot, code):
    """Đỗ xe vào ô trống đầu tiên theo thứ tự hàng 0 trái sang phải, rồi hàng 1...; trả (hàng, cột). Xe đã có trong bãi hoặc bãi đầy trả None."""
    raise NotImplementedError


def leave(lot, code):
    """Xe rời bãi: ô của xe trở về None; trả True nếu có xe đó."""
    raise NotImplementedError


def slot_number(lot, row, col):
    """Số thứ tự ô (đếm từ 1) in trên vạch sơn: đánh số theo từng hàng, trái sang phải."""
    raise NotImplementedError


def occupancy(lot):
    """List số xe đang đỗ ở từng hàng."""
    raise NotImplementedError


if __name__ == "__main__":
    lot = make_lot(2, 3)
    for code in ("XE01", "XE02", "XE03", "XE04"):
        spot = park(lot, code)
        print(f"{code} đỗ tại {spot}, ô số {slot_number(lot, *spot)}")
    print("Đỗ lại XE02:", park(lot, "XE02"))
    print("XE02 rời bãi:", leave(lot, "XE02"), "| XE09 rời bãi:", leave(lot, "XE09"))
    print("XE05 đỗ tại:", park(lot, "XE05"), "| số xe mỗi hàng:", occupancy(lot))
    print("XE06, XE07 đỗ tại:", park(lot, "XE06"), park(lot, "XE07"), "| bãi:", lot)
