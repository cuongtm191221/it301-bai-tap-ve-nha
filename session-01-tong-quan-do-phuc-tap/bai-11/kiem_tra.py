"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
import inspect
from giam_gia import discounted_price, apply_discount_in_place, discounted_copy, total_after_discount

PRICES = [259000, 99000, 1490000, 1500]


def check_price():
    got = (discounted_price(259000, 15), discounted_price(99000, 15), discounted_price(1500, 15), discounted_price(1000000, 90))
    assert got == (220000, 84000, 1000, 100000), f"giá sau giảm ra {got}"


def check_percent():
    for bad in (0, 95, -5, 91):
        try:
            discounted_price(100000, bad)
        except ValueError as error:
            assert str(error) == "Phần trăm giảm phải từ 1 đến 90.", f"thông báo lỗi là: {error}"
        else:
            raise AssertionError(f"giảm {bad}% phải báo ValueError")


def check_copy():
    prices = PRICES[:]
    assert discounted_copy(prices, 15) == [220000, 84000, 1266000, 1000]
    assert prices == PRICES, "discounted_copy không được sửa list gốc"
    assert discounted_copy([], 15) == []


def check_in_place():
    prices = PRICES[:]
    same = prices
    assert apply_discount_in_place(prices, 15) is None, "apply_discount_in_place phải trả về None"
    assert prices == [220000, 84000, 1266000, 1000] and same is prices, "phải sửa ngay trên list prices"
    assert "append" not in inspect.getsource(apply_discount_in_place), "giảm giá tại chỗ không được tạo list mới"


def check_total():
    assert total_after_discount(PRICES, 15) == 1571000 and total_after_discount([], 15) == 0
    src = inspect.getsource(total_after_discount)
    assert "append" not in src and "discounted_copy" not in src and "[" not in src.split("\n", 2)[2], "tính tổng không được tạo list"


CHECKS = [
    ("giá sau giảm: làm tròn xuống nghìn, giá sàn 1.000đ", check_price),
    ("phần trăm ngoài 1..90 báo ValueError", check_percent),
    ("bản sao không sửa list gốc", check_copy),
    ("giảm giá tại chỗ trả về None, không tạo list", check_in_place),
    ("tổng tiền không tạo list", check_total),
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
