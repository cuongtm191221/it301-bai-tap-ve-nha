"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
from don_trung import count_duplicate_pairs, COMPLEXITY

ORDERS = [
    {"code": "DH3001", "buyer": "an.nguyen", "product": "SP01"},
    {"code": "DH3002", "buyer": "binh.tran", "product": "SP02"},
    {"code": "DH3003", "buyer": "an.nguyen", "product": "SP01"},
    {"code": "DH3004", "buyer": "chi.le", "product": "SP03"},
    {"code": "DH3005", "buyer": "binh.tran", "product": "SP02"},
]


def check_example():
    assert count_duplicate_pairs(ORDERS) == (2, 10), f"5 đơn ra {count_duplicate_pairs(ORDERS)}"


def check_small():
    assert count_duplicate_pairs([]) == (0, 0), f"danh sách rỗng ra {count_duplicate_pairs([])}"
    assert count_duplicate_pairs(ORDERS[:1]) == (0, 0), f"1 đơn ra {count_duplicate_pairs(ORDERS[:1])}"


def check_last_order():
    data = ORDERS[:4] + [{"code": "DH3009", "buyer": "chi.le", "product": "SP03"}]
    assert count_duplicate_pairs(data)[0] == 2, "cặp trùng có đơn đứng cuối danh sách phải được đếm"


def check_triple():
    triple = [{"code": "DH", "buyer": "dung.pham", "product": "SP09"}] * 3
    assert count_duplicate_pairs(triple) == (3, 3), f"3 đơn giống nhau ra {count_duplicate_pairs(triple)}"


def check_comparisons():
    for n in (10, 100, 1000):
        many = [{"code": "DH", "buyer": f"k{i}", "product": "SP01"} for i in range(n)]
        got = count_duplicate_pairs(many)
        assert got == (0, n * (n - 1) // 2), f"{n} đơn khác nhau ra {got}"


def check_complexity():
    assert COMPLEXITY.replace(" ", "").replace("²", "^2") == "O(n^2)", f"Big-O ghi là {COMPLEXITY}"


CHECKS = [
    ("ví dụ 5 đơn: 2 cặp trùng, 10 lần so sánh", check_example),
    ("danh sách rỗng và 1 đơn", check_small),
    ("cặp trùng có đơn đứng cuối", check_last_order),
    ("3 đơn giống nhau tạo 3 cặp", check_triple),
    ("số lần so sánh bằng n(n - 1)/2", check_comparisons),
    ("Big-O ghi đúng", check_complexity),
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
