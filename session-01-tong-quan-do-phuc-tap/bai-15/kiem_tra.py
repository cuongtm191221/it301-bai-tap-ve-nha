"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
from than_thiet import loyal_customers


def check_ai_example():
    assert loyal_customers(["KH01", "KH02", "KH01", "KH03", "KH01"], 2) == ["KH01"]


def check_ai_none():
    assert loyal_customers(["KH01", "KH02"], 2) == []


def check_ai_empty():
    assert loyal_customers([], 2) == []


CHECKS = [
    ("ví dụ 5 đơn, ngưỡng 2 (kiểm tra do AI viết)", check_ai_example),
    ("không có khách đủ ngưỡng (kiểm tra do AI viết)", check_ai_none),
    ("danh sách rỗng (kiểm tra do AI viết)", check_ai_empty),
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
