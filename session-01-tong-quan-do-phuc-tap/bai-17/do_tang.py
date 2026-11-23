"""Phân loại độ phức tạp của báo cáo từ các lần đo số bước, cho nhóm hiệu năng của Shopee."""


def check_measurements(measurements):
    """Trả về bản sao các lần đo đã xếp theo n tăng dần; báo ValueError nếu số đo không hợp lệ (xem đề, mục 2.1)."""
    raise NotImplementedError


def growth_ratios(measurements):
    """Trả về list tỉ lệ số bước giữa hai lần đo liên tiếp, làm tròn 2 chữ số (xem đề, mục 2.2)."""
    raise NotImplementedError


def classify(measurements):
    """Trả về lớp độ phức tạp theo bảng quy tắc ở mục 2.3 của đề."""
    raise NotImplementedError


def report_line(name, measurements):
    """Trả về một dòng của bảng hiệu năng (xem đề, mục 2.4)."""
    raise NotImplementedError


if __name__ == "__main__":
    reports = {
        "in_tieu_de": [(1000, 4), (2000, 4), (4000, 4), (8000, 4)],
        "tim_don": [(1000, 10), (2000, 11), (4000, 12), (8000, 13)],
        "tong_doanh_thu": [(1000, 1002), (2000, 2002), (4000, 4002), (8000, 8002)],
        "xep_hang": [(1000, 9976), (2000, 21952), (4000, 47904), (8000, 103808)],
        "don_trung": [(4000, 7998000), (1000, 499500), (2000, 1999000)],
        "do_nham": [(1000, 500), (3000, 1500), (9000, 4500)],
        "thieu_so_do": [(1000, 10), (2000, 20)],
        "giam_dan": [(1000, 90), (2000, 60), (4000, 30)],
    }
    for name, data in reports.items():
        print(report_line(name, data))
    print("Tỉ lệ của don_trung:", growth_ratios(reports["don_trung"]))
    print("Số đo don_trung giữ nguyên thứ tự:", reports["don_trung"][0])
