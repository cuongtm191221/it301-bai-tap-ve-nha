"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
import inspect
from phan_trang import total_pages, get_page

ORDERS = ["DH8001", "DH8002", "DH8003", "DH8004", "DH8005", "DH8006", "DH8007"]


def check_total_pages():
    got = (total_pages(7, 3), total_pages(6, 3), total_pages(0, 3), total_pages(1, 20))
    assert got == (3, 2, 0, 1), f"số trang của 7, 6, 0, 1 đơn ra {got}"


def check_pages():
    assert get_page(ORDERS, 1, 3) == ["DH8007", "DH8006", "DH8005"], f"trang 1 ra {get_page(ORDERS, 1, 3)}"
    assert get_page(ORDERS, 2, 3) == ["DH8004", "DH8003", "DH8002"], f"trang 2 ra {get_page(ORDERS, 2, 3)}"


def check_last_page():
    assert get_page(ORDERS, 3, 3) == ["DH8001"], f"trang cuối ra {get_page(ORDERS, 3, 3)}"


def check_out_of_range():
    got = (get_page(ORDERS, 0, 3), get_page(ORDERS, -1, 3), get_page(ORDERS, 4, 3), get_page([], 1, 3))
    assert got == ([], [], [], []), f"trang 0, -1, 4 và danh sách rỗng ra {got}"


def check_no_full_copy():
    src = inspect.getsource(get_page)
    assert "[::" not in src and "reverse" not in src and "copy" not in src, "get_page vẫn tạo bản sao cả danh sách"
    orders = ORDERS[:]
    get_page(orders, 2, 3)
    assert orders == ORDERS, "get_page không được sửa danh sách đơn"


CHECKS = [
    ("số trang, kể cả trang cuối thiếu đơn", check_total_pages),
    ("trang 1 và trang 2, đơn mới nhất trước", check_pages),
    ("trang cuối", check_last_page),
    ("trang không tồn tại", check_out_of_range),
    ("không tạo bản sao cả danh sách, không sửa danh sách", check_no_full_copy),
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
