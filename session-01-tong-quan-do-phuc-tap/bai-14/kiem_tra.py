"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
from ban_chay import top_k_v1, top_k_v2, top_message

SALES = [
    {"code": "SP01", "sold": 95},
    {"code": "SP02", "sold": 40},
    {"code": "SP03", "sold": 120},
    {"code": "SP04", "sold": 7},
    {"code": "SP05", "sold": 95},
    {"code": "SP06", "sold": 60},
]
BOTH = [("top_k_v1", top_k_v1), ("top_k_v2", top_k_v2)]


def check_top3():
    for name, f in BOTH:
        got = f(SALES, 3)
        assert got == [("SP03", 120), ("SP01", 95), ("SP05", 95)], f"{name}: top 3 ra {got}"


def check_k_large_and_bad():
    for name, f in BOTH:
        assert len(f(SALES, 10)) == 6, f"{name}: k lớn hơn số sản phẩm phải trả về tất cả"
        assert f(SALES, 0) == [] and f(SALES, -2) == [] and f([], 3) == [], f"{name}: k không dương hoặc list rỗng"


def check_ties():
    data = [{"code": c, "sold": 10} for c in ("SP09", "SP02", "SP07", "SP01")]
    for name, f in BOTH:
        got = [c for c, _ in f(data, 2)]
        assert got == ["SP09", "SP02"], f"{name}: bằng nhau phải giữ thứ tự trong list, ra {got}"


def check_unchanged():
    for name, f in BOTH:
        data = [dict(s) for s in SALES]
        f(data, 3)
        assert [s["code"] for s in data] == ["SP01", "SP02", "SP03", "SP04", "SP05", "SP06"], f"{name} đã đổi thứ tự list đầu vào"


def check_same_answer():
    import random
    rng = random.Random(3)
    for _ in range(300):
        data = [{"code": f"SP{i:02d}", "sold": rng.randint(0, 9)} for i in range(rng.randint(0, 12))]
        k = rng.randint(1, 6)
        assert top_k_v1(data, k) == top_k_v2(data, k), f"hai giải pháp khác nhau với k = {k}"


def check_message():
    assert top_message(SALES, 3) == "Top 3 bán chạy: SP03 (120), SP01 (95), SP05 (95)"
    assert top_message(SALES, 10).startswith("Top 6 bán chạy: ")
    assert top_message(SALES, 0) == "Số sản phẩm cần xếp hạng phải lớn hơn 0."
    assert top_message([], 3) == "Gian hàng chưa bán được sản phẩm nào."


CHECKS = [
    ("top 3 của ví dụ", check_top3),
    ("k lớn hơn số sản phẩm, k không dương, list rỗng", check_k_large_and_bad),
    ("bằng nhau giữ thứ tự trong list", check_ties),
    ("không đổi list đầu vào", check_unchanged),
    ("hai giải pháp cho cùng kết quả", check_same_answer),
    ("thông báo bảng xếp hạng", check_message),
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
