"""P3 - Dựng dữ liệu cho trường hợp tốt nhất và xấu nhất."""


def best_case_find(n):
    """Trả bộ (values, target): values là list n mã, find(target) chỉ so sánh 1 lần."""
    raise NotImplementedError


def worst_case_find(n):
    """Trả bộ (values, target): find(target) phải so sánh đủ n lần rồi trả None."""
    raise NotImplementedError


def tail_case_remove(n):
    """Trả bộ (values, target), n >= 2: remove(target) xóa đúng node cuối và tail phải lùi về node đứng trước."""
    raise NotImplementedError


# Big-O của find trong trường hợp xấu nhất
FIND_WORST = "?"
