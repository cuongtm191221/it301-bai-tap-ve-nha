"""Ước lượng chi phí thao tác trên hàng đơn GrabFood trước khi chạy."""
def shift_cost(op, n, i=None):
    # Số tham chiếu phải dịch khi chạy thao tác op trên list n phần tử (Lesson 03).
    # op: "append", "pop_end" (pop()), "pop" (pop(i)), "insert" (insert(i, x)).
    # i âm tính từ cuối. pop với i ngoài -n đến n - 1: ValueError("chỉ số không hợp lệ").
    # insert với i vượt khỏi khoảng thì kẹp vào 0 hoặc n như list.insert.
    if op in ("append", "pop_end"):
        return 0
    if op == "pop":
        if not -n <= i < n:
            raise ValueError("chỉ số không hợp lệ")
        return n - i
    if op == "insert":
        if i > n:
            i = n
        return n - i - 1
    raise ValueError("thao tác không hỗ trợ")


def queue_cost(n, k):
    # Tổng số tham chiếu phải dịch khi phục vụ k người đầu hàng bằng k lần pop(0), hàng ban đầu n người.
    return k * shift_cost("pop", n, 0)


if __name__ == "__main__":
    print("pop(0) trên 6 phần tử:", shift_cost("pop", 6, 0))
    print("pop(-1) trên 6 phần tử:", shift_cost("pop", 6, -1))
    print("insert(2, x) trên 6 phần tử:", shift_cost("insert", 6, 2))
    print("insert(-2, x) trên 6 phần tử:", shift_cost("insert", 6, -2))
    print("insert(99, x) trên 6 phần tử:", shift_cost("insert", 6, 99))
    print("Phục vụ 3 người đầu hàng 5 người:", queue_cost(5, 3))
    print("Phục vụ hết hàng 200.000 người:", queue_cost(200000, 200000))
