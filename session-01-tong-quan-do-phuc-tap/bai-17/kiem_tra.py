"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
from do_tang import check_measurements, growth_ratios, classify, report_line

def err(f, data):
    try:
        f(data)
    except ValueError as error:
        return str(error)
    return None


def check_validation():
    assert err(check_measurements, [(1000, 10), (2000, 20)]) == "Cần ít nhất 3 lần đo."
    assert err(check_measurements, [(1000, 500), (3000, 1500), (9000, 4500)]) == "Các lần đo phải có n tăng gấp đôi."
    assert err(check_measurements, [(1000, 5), (2000, 0), (4000, 9)]) == "Số bước phải lớn hơn 0."


def check_unsorted_input():
    data = [(4000, 7998000), (1000, 499500), (2000, 1999000)]
    assert growth_ratios(data) == [4.0, 4.0], f"tỉ lệ ra {growth_ratios(data)}"
    assert data == [(4000, 7998000), (1000, 499500), (2000, 1999000)], "không được sửa list số đo"


def check_classes():
    cases = {
        "O(1)": [(1000, 4), (2000, 4), (4000, 4), (8000, 4)],
        "O(log n)": [(1000, 10), (2000, 11), (4000, 12), (8000, 13)],
        "O(n)": [(1000, 1002), (2000, 2002), (4000, 4002), (8000, 8002)],
        "O(n log n)": [(1000, 9976), (2000, 21952), (4000, 47904), (8000, 103808)],
        "O(n^2)": [(1000, 499500), (2000, 1999000), (4000, 7998000)],
    }
    for label, data in cases.items():
        assert classify(data) == label, f"{label} bị phân loại là {classify(data)}"


def check_unknown():
    assert classify([(1000, 90), (2000, 60), (4000, 30)]) == "Không xác định", "số bước giảm"
    assert classify([(1000, 10), (2000, 80), (4000, 640)]) == "Không xác định", "tăng gấp 8 mỗi lần"


def check_lines():
    assert report_line("tong_doanh_thu", [(1000, 1002), (2000, 2002), (4000, 4002), (8000, 8002)]) == "tong_doanh_thu: O(n) (tỉ lệ trung bình 2.00)"
    assert report_line("thieu", [(1000, 10), (2000, 20)]) == "thieu: số đo không hợp lệ - Cần ít nhất 3 lần đo."


CHECKS = [
    ("kiểm tra số đo không hợp lệ", check_validation),
    ("số đo không theo thứ tự, không sửa list", check_unsorted_input),
    ("phân loại năm lớp độ phức tạp", check_classes),
    ("không xác định", check_unknown),
    ("dòng báo cáo", check_lines),
]


if __name__ == "__main__":
    passed = 0
    for name, check in CHECKS:
        try:
            check()
            print("ĐẠT      |", name)
            passed += 1
        except NotImplementedError:
            print("CHƯA LÀM |", name)
        except AssertionError as error:
            print("CHƯA ĐẠT |", name, "-", error)
        except Exception as error:
            print("LỖI      |", name, "-", type(error).__name__, error)
    print(f"Kết quả: {passed}/{len(CHECKS)} mục đạt")
