"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
from bao_cao import total_revenue, count_big_orders, COMPLEXITY

ORDERS = [
    {"code": "DH2001", "amount": 120000},
    {"code": "DH2002", "amount": 560000},
    {"code": "DH2003", "amount": 500000},
    {"code": "DH2004", "amount": 89000},
    {"code": "DH2005", "amount": 1250000},
]


def check_total():
    assert total_revenue(ORDERS) == (2519000, 7), f"5 đơn ra {total_revenue(ORDERS)}"
    assert total_revenue([]) == (0, 2), f"danh sách rỗng ra {total_revenue([])}"


def check_total_steps_formula():
    for n in (1, 10, 1000):
        steps = total_revenue([{"amount": 1}] * n)[1]
        assert steps == n + 2, f"n = {n}: đếm được {steps} bước"


def check_big_orders():
    assert count_big_orders(ORDERS, 500000)[0] == 3, "đơn đúng 500.000đ cũng là đơn từ 500.000đ trở lên"
    assert count_big_orders(ORDERS, 500000) == (3, 10), f"5 đơn ra {count_big_orders(ORDERS, 500000)}"


def check_big_orders_steps():
    for amount, expected in ((100000, 1002), (600000, 2002)):
        steps = count_big_orders([{"amount": amount}] * 1000, 500000)[1]
        assert steps == expected, f"1.000 đơn giá {amount}: đếm được {steps} bước"


def check_complexity():
    clean = {k: v.replace(" ", "") for k, v in COMPLEXITY.items()}
    assert clean.get("total_revenue") == "O(n)", "Big-O của total_revenue chưa rút gọn đúng"
    assert clean.get("count_big_orders") == "O(n)", "Big-O của count_big_orders chưa rút gọn đúng"


CHECKS = [
    ("tổng doanh thu và số bước", check_total),
    ("số bước của total_revenue bằng n + 2", check_total_steps_formula),
    ("đếm đơn từ ngưỡng trở lên", check_big_orders),
    ("số bước của count_big_orders khi ít và nhiều đơn lớn", check_big_orders_steps),
    ("Big-O đã rút gọn", check_complexity),
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
