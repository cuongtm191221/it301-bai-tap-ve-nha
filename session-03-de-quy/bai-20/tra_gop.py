"""Đếm số phương án trả góp cho tính năng "Ví Trả Sau" của MoMo."""


from functools import lru_cache


def count_plans_slow(amount):
    """Có sẵn. Bản cũ đang chạy trên máy chủ: số cách trả hết amount triệu, mỗi kỳ trả 1, 2 hoặc 3 triệu, thứ tự các kỳ có ý nghĩa."""
    if amount < 0:
        return 0
    if amount == 0:
        return 1
    return count_plans_slow(amount - 1) + count_plans_slow(amount - 2) + count_plans_slow(amount - 3)


def count_plans(amount):
    """Cùng kết quả với count_plans_slow, nhanh và chịu được amount tới 3.000."""
    raise NotImplementedError


def count_plans_limited(amount, max_terms):
    """Số cách trả hết amount triệu trong không quá max_terms kỳ (mỗi kỳ 1, 2 hoặc 3 triệu)."""
    raise NotImplementedError


@lru_cache(maxsize=None)

def plan_report(amounts, max_terms):
    """List dòng báo cáo cho từng khoản vay (triệu đồng)."""
    raise NotImplementedError


if __name__ == "__main__":
    for line in plan_report([1, 3, 5, 10, 0, -2], 3):
        print(line)
    print(plan_report([4], 0)[0])
    print("Khoản 30 triệu:", count_plans(30), "cách")
    print("Khoản 3.000 triệu có", len(str(count_plans(3000))), "chữ số")
