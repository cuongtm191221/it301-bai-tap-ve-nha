"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
import inspect
from ton_kho import is_valid, inventory_summary, restock_list, summary_message

SHOP = [
    {"code": "SP01", "price": 259000, "stock": 12},
    {"code": "SP02", "price": 1490000, "stock": 3},
    {"code": "SP03", "price": 99000, "stock": 0},
    {"code": "SP04", "price": 99000, "stock": -2},
    {"code": "SP05", "price": 0, "stock": 40},
    {"code": "SP06", "price": 459000, "stock": 5},
]


def check_valid():
    got = [is_valid(p) for p in SHOP] + [is_valid({"code": "X", "price": 99.5, "stock": 1}), is_valid({"code": "X", "price": -1, "stock": 1})]
    assert got == [True, True, True, True, False, True, False, False], f"is_valid ra {got}"


def check_summary():
    s = inventory_summary(SHOP)
    want = {"valid": 5, "out_of_stock": 2, "stock_value": 9873000, "cheapest": "SP03", "priciest": "SP02", "skipped": 1}
    assert s == want, f"tóm tắt ra {s}"


def check_summary_one_pass():
    src = inspect.getsource(inventory_summary)
    assert src.count("for ") == 1 and "sort" not in src and "append" not in src and "min(" not in src and "max(" not in src, "inventory_summary phải duyệt một lượt, không tạo list, không sắp xếp"


def check_restock():
    shop = [dict(p) for p in SHOP]
    assert restock_list(shop, 3) == ["SP04", "SP03", "SP02"], f"3 sản phẩm ra {restock_list(shop, 3)}"
    assert restock_list(shop, 10) == ["SP04", "SP03", "SP02", "SP06", "SP01"]
    assert restock_list(shop, 0) == [] and restock_list([], 3) == []
    assert [p["code"] for p in shop] == ["SP01", "SP02", "SP03", "SP04", "SP05", "SP06"], "không được đổi thứ tự list gốc"


def check_message():
    assert summary_message(SHOP) == "5 sản phẩm, 2 hết hàng. Giá trị tồn kho: 9.873.000đ. Rẻ nhất: SP03, đắt nhất: SP02. Bỏ qua 1 dòng lỗi."
    assert summary_message([{"code": "SP09", "price": -5, "stock": 1}]) == "Chưa có sản phẩm hợp lệ. Bỏ qua 1 dòng lỗi."
    assert summary_message([]) == "Chưa có sản phẩm hợp lệ. Bỏ qua 0 dòng lỗi."


CHECKS = [
    ("sản phẩm hợp lệ", check_valid),
    ("tóm tắt tồn kho của ví dụ", check_summary),
    ("tóm tắt duyệt một lượt, bộ nhớ phụ O(1)", check_summary_one_pass),
    ("danh sách cần nhập thêm", check_restock),
    ("thông báo cuối ngày", check_message),
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
