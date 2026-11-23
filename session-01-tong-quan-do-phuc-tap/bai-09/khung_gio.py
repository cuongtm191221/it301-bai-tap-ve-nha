"""Tìm khung giờ cao điểm đặt hàng của gian hàng trên Shopee."""


def parse_hour(text):
    """Trả về giờ (số nguyên 0..23) của chuỗi thời điểm dạng "HH:MM", hoặc None nếu chuỗi không hợp lệ (xem đề, mục 2.1)."""
    raise NotImplementedError


def count_by_hour(times):
    """Trả về (list 24 số đếm đơn theo giờ, số dòng không hợp lệ) (xem đề, mục 2.2)."""
    raise NotImplementedError


def peak_hour_message(times):
    """Trả về thông báo khung giờ cao điểm (xem đề, mục 2.3)."""
    raise NotImplementedError


if __name__ == "__main__":
    times = ["20:15", " 09:05 ", "20:47", "13:30", "24:10", "21:02", "07:60", "20:59", "9:05", "13:01", "21:40"]
    print("parse_hour(\" 09:05 \"):", parse_hour(" 09:05 "), "| parse_hour(\"24:10\"):", parse_hour("24:10"))
    counts, invalid = count_by_hour(times)
    print("Số đơn lúc 20 giờ:", counts[20], "| số dòng lỗi:", invalid)
    print(peak_hour_message(times))
    print(peak_hour_message(["13:10", "08:00", "13:55", "08:30"]))
    print(peak_hour_message(["00:05", "23:59", "00:40"]))
    print(peak_hour_message(["25:00", "ab:cd"]))
    print(peak_hour_message([]))
