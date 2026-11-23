"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
import inspect
from bang_gia import top_prices, average_price, cheapest_after_discount

PRICES = [259000, 99000, 1490000, 459000, 189000]


def check_top():
    prices = PRICES[:]
    assert top_prices(prices, 3) == [1490000, 459000, 259000], f"3 giá cao nhất ra {top_prices(prices, 3)}"


def check_top_keeps_order():
    prices = PRICES[:]
    top_prices(prices, 3)
    assert prices == PRICES, f"danh sách niêm yết bị đổi thành {prices}"


def check_average():
    prices = PRICES[:]
    assert average_price(prices) == 499200.0, f"giá trung bình ra {average_price(prices)}"
    assert average_price([]) is None, "gian hàng chưa có sản phẩm phải trả về None"


def check_average_no_copy():
    src = inspect.getsource(average_price)
    assert "[:]" not in src and "copy" not in src and "list(" not in src, "average_price vẫn tạo bản sao danh sách"


def check_discount():
    prices = PRICES[:]
    assert cheapest_after_discount(prices, 10) == 89100, f"rẻ nhất sau giảm 10% ra {cheapest_after_discount(prices, 10)}"
    assert prices == PRICES, f"danh sách niêm yết bị đổi thành {prices}"


CHECKS = [
    ("3 giá cao nhất", check_top),
    ("lập top không đổi thứ tự niêm yết", check_top_keeps_order),
    ("giá trung bình, kể cả gian hàng chưa có sản phẩm", check_average),
    ("giá trung bình không tạo bản sao", check_average_no_copy),
    ("giá rẻ nhất sau giảm giá, không sửa danh sách gốc", check_discount),
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
