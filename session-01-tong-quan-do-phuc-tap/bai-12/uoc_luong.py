"""Ước lượng thời gian chạy báo cáo đêm của Shopee từ độ phức tạp."""

SUPPORTED = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)"]


def normalize(complexity):
    """Trả về độ phức tạp ở dạng chuẩn trong SUPPORTED, hoặc None nếu không hỗ trợ (xem đề, mục 2.1)."""
    raise NotImplementedError


def halvings(n):
    """Có sẵn: trả về số lần chia đôi n (lấy phần nguyên) cho đến khi còn 1, như bài đọc Lesson 02."""
    count = 0
    while n > 1:                  # mỗi lượt n giảm một nửa: O(log n) lượt
        n = n // 2
        count += 1
    return count


def estimate_steps(complexity, n):
    """Trả về số bước ước lượng (ít nhất 1), hoặc None nếu độ phức tạp không hỗ trợ hoặc n không dương (xem đề, mục 2.2)."""
    raise NotImplementedError


def growth_ratio(complexity, n1, n2):
    """Trả về số lần tăng số bước khi n tăng từ n1 lên n2, làm tròn 1 chữ số thập phân, hoặc None (xem đề, mục 2.3)."""
    raise NotImplementedError


def fits_window(complexity, n, steps_per_second, seconds):
    """Trả về thông báo báo cáo có chạy kịp trong khung giờ không (xem đề, mục 2.4)."""
    raise NotImplementedError


if __name__ == "__main__":
    for c in SUPPORTED:
        print(f"{c:10s} n = 1.000.000:", estimate_steps(c, 1000000))
    print("Tăng khi n từ 1.000 lên 10.000, O(n^2):", growth_ratio("O(n^2)", 1000, 10000))
    print("Tăng khi n từ 1.000 lên 10.000, O(log n):", growth_ratio("o(log N)", 1000, 10000))
    print("O(n log n) với n = 1:", estimate_steps("O(n log n)", 1))
    print(fits_window("O(n log n)", 2000000, 10000000, 7200))
    print(fits_window("O(n²)", 2000000, 10000000, 7200))
    print(fits_window("O(2^n)", 50, 10000000, 7200))
    print(fits_window("O(n)", 0, 10000000, 7200))
