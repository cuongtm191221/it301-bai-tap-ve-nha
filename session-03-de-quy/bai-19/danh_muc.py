"""Báo cáo chi tiêu theo cây danh mục cho màn hình "Quản lý chi tiêu" của ví MoMo."""


def money(amount):
    """Có sẵn. Số tiền có dấu chấm ngăn cách hàng nghìn, ví dụ 1234567 thành "1.234.567"."""
    if amount < 0:
        return "-" + money(-amount)
    if amount < 1000:
        return str(amount)
    return money(amount // 1000) + "." + str(amount % 1000).zfill(3)


def normalize(name):
    """Có sẵn. Chuẩn hóa tên danh mục để so sánh: bỏ khoảng trắng thừa, đổi sang chữ thường."""
    return " ".join(name.split()).lower()


def category_total(category):
    """Tổng tiền của danh mục (tên, list phần tử); mỗi phần tử là số tiền hoặc danh mục con; số âm là hoàn tiền."""
    raise NotImplementedError


def report_lines(category, level=0):
    """List dòng báo cáo: mỗi danh mục một dòng "<thụt lề><tên>: <tổng>đ", thụt 2 dấu cách mỗi cấp, danh mục cha đứng trước danh mục con."""
    raise NotImplementedError


def find_path(category, name):
    """Đường dẫn "Gốc > ... > Danh mục" tới danh mục đầu tiên (theo thứ tự báo cáo) có tên trùng name sau khi chuẩn hóa; không có thì None."""
    raise NotImplementedError


def category_report(category):
    """Toàn bộ báo cáo dưới dạng một chuỗi nhiều dòng."""
    raise NotImplementedError


if __name__ == "__main__":
    june = ("Tháng 6", [
        ("Ăn uống", [120000, ("Cà phê", [45000, 30000, -30000]), 85000]),
        ("Di chuyển", [("Xe ôm", [25000, 40000]), ("Xăng", [100000])]),
        ("Hóa đơn", [350000, 220000]),
        ("Giải trí", []),
    ])
    print(category_report(june))
    print(find_path(june, " xe  ÔM "))
    print(find_path(june, "Cà phê"))
    print(find_path(june, "Du lịch"))
