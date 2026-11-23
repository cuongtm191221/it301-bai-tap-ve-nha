"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
from ton_kho import first_out_of_stock

SHOP = [
    {"code": "SP01", "stock": 12},
    {"code": "SP02", "stock": 0},
    {"code": "SP03", "stock": 5},
    {"code": "SP04", "stock": -2},
    {"code": "SP05", "stock": 30},
    {"code": "SP06", "stock": 0},
]


def check_first():
    assert first_out_of_stock(SHOP) == ("SP02", 2), f"6 sản phẩm ra {first_out_of_stock(SHOP)}"


def check_none():
    data = [SHOP[0], SHOP[2], SHOP[4]]
    assert first_out_of_stock(data) == (None, 3), f"gian hàng đủ hàng ra {first_out_of_stock(data)}"


def check_negative():
    data = [SHOP[0], SHOP[3], SHOP[4]]
    assert first_out_of_stock(data) == ("SP04", 2), f"tồn kho âm ra {first_out_of_stock(data)}"


def check_empty():
    assert first_out_of_stock([]) == (None, 0), "gian hàng chưa có sản phẩm phải trả về (None, 0)"


def check_best_worst():
    full = [{"code": "SP", "stock": 9}] * 999
    assert first_out_of_stock([{"code": "SPX", "stock": 0}] + full) == ("SPX", 1), "hết hàng ở đầu chỉ được xét 1 sản phẩm"
    assert first_out_of_stock(full + [{"code": "SPX", "stock": 0}]) == ("SPX", 1000), "hết hàng ở cuối phải xét 1.000 sản phẩm"
    assert first_out_of_stock(full) == (None, 999), "không có sản phẩm hết hàng phải xét hết danh sách"


CHECKS = [
    ("sản phẩm hết hàng đầu tiên và dừng ngay", check_first),
    ("không có sản phẩm hết hàng", check_none),
    ("tồn kho âm cũng là hết hàng", check_negative),
    ("gian hàng chưa có sản phẩm", check_empty),
    ("số sản phẩm đã xét trong trường hợp tốt nhất và xấu nhất", check_best_worst),
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
