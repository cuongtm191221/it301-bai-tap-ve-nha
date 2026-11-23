"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
from chuoi_tang import longest_growth_streak, streak_message

WEEK = [12, 15, 15, 18, 21, 25, 20, 22, 30]


def check_example():
    assert longest_growth_streak(WEEK) == (4, 3, 8), f"tháng 11 ra {longest_growth_streak(WEEK)}"
    assert streak_message(WEEK) == "Chuỗi tăng dài nhất: 4 ngày, từ ngày 3 đến ngày 6."


def check_equal_breaks():
    assert longest_growth_streak([5, 5, 5])[:2] == (1, 1), "hai ngày bằng nhau không phải là tăng"
    assert streak_message([9, 8, 6, 6, 2]) == "Chưa có hai ngày liên tiếp nào doanh thu tăng."


def check_tie_earliest():
    assert streak_message([5, 7, 9, 3, 4, 6]) == "Chuỗi tăng dài nhất: 3 ngày, từ ngày 1 đến ngày 3.", "dài bằng nhau phải chọn chuỗi sớm hơn"


def check_streak_at_end():
    assert streak_message([4, 6, 2, 3, 5, 8]) == "Chuỗi tăng dài nhất: 4 ngày, từ ngày 3 đến ngày 6.", "chuỗi kéo dài tới ngày cuối bị bỏ sót"


def check_small():
    assert longest_growth_streak([]) == (0, None, 0) and streak_message([]) == "Chưa có dữ liệu doanh thu."
    assert longest_growth_streak([10]) == (1, 1, 0) and streak_message([10]) == "Chưa có hai ngày liên tiếp nào doanh thu tăng."


def check_one_pass():
    assert longest_growth_streak(list(range(1000))) == (1000, 1, 999), "1.000 ngày tăng đều phải ra (1000, 1, 999)"
    assert longest_growth_streak(list(range(100000, 0, -1)))[2] == 99999, "100.000 ngày phải đúng 99.999 lần so sánh"


CHECKS = [
    ("ví dụ tháng 11", check_example),
    ("bằng nhau không phải là tăng", check_equal_breaks),
    ("dài bằng nhau chọn chuỗi sớm hơn", check_tie_earliest),
    ("chuỗi kéo dài tới ngày cuối", check_streak_at_end),
    ("không có dữ liệu và chỉ một ngày", check_small),
    ("một lượt duyệt: n - 1 lần so sánh", check_one_pass),
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
