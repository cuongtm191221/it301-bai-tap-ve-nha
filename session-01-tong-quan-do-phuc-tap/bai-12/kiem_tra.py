"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
from uoc_luong import normalize, halvings, estimate_steps, growth_ratio, fits_window


def check_normalize():
    got = [normalize(x) for x in ("O(1)", " o(log N) ", "O(n)", "O( n log n )", "O(n²)", "O(n^3)", "O(2^n)")]
    assert got == ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)", None, None], f"chuẩn hóa ra {got}"


def check_estimate():
    got = [estimate_steps(c, 1000000) for c in ("O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)")]
    assert got == [1, 19, 1000000, 19000000, 1000000000000], f"1.000.000 ra {got}"
    assert halvings(8) == 3 and halvings(1000) == 9 and halvings(1) == 0


def check_minimum_one():
    assert estimate_steps("O(log n)", 1) == 1 and estimate_steps("O(n log n)", 1) == 1, "ít nhất 1 bước khi n = 1"


def check_invalid():
    assert estimate_steps("O(2^n)", 10) is None and estimate_steps("O(n)", 0) is None and estimate_steps("O(n)", -5) is None
    assert growth_ratio("O(n^3)", 10, 100) is None and growth_ratio("O(n)", 0, 100) is None


def check_ratio():
    got = (growth_ratio("O(n^2)", 1000, 10000), growth_ratio("O(n)", 1000, 10000), growth_ratio("o(log N)", 1000, 10000), growth_ratio("O(1)", 5, 500000))
    assert got == (100.0, 10.0, 1.4, 1.0), f"tỉ lệ tăng ra {got}"


def check_window():
    assert fits_window("O(n log n)", 2000000, 10000000, 7200) == "Kịp: cần khoảng 40000000 bước, khung giờ cho phép 72000000000 bước."
    assert fits_window("O(n²)", 2000000, 10000000, 7200) == "Không kịp: cần khoảng 4000000000000 bước, vượt 3928000000000 bước."
    assert fits_window(" O(2^n) ", 50, 10000000, 7200) == "Không hỗ trợ độ phức tạp O(2^n)."
    assert fits_window("O(n)", 0, 10000000, 7200) == "Số lượng dữ liệu phải lớn hơn 0."


CHECKS = [
    ("chuẩn hóa cách viết độ phức tạp", check_normalize),
    ("ước lượng số bước với n = 1.000.000", check_estimate),
    ("ít nhất 1 bước", check_minimum_one),
    ("độ phức tạp không hỗ trợ hoặc n không dương", check_invalid),
    ("tỉ lệ tăng khi n tăng", check_ratio),
    ("thông báo kịp / không kịp khung giờ", check_window),
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
