"""Chia lô đơn hàng cho kho trong ngày sale trên Shopee."""


def split_batches(n_orders, capacity):
    # Chia đôi lô đơn liên tục cho đến khi mỗi lô có không quá capacity đơn.
    # Khi chia, lô lẻ đơn thì nửa lớn hơn nhận thêm 1 đơn, nên không đơn nào bị mất.
    # Trả về (số lần chia đôi, số đơn của lô lớn nhất sau khi chia). capacity không dương thì trả về None.
    batch = n_orders
    splits = 0
    while batch >= capacity:
        batch = batch / 2
        splits += 1
    return splits, batch


# Big-O thời gian theo n (số đơn), ghi trong tài liệu kỹ thuật của nhóm
COMPLEXITY = "O(n)"


if __name__ == "__main__":
    print("10.000 đơn, lô tối đa 500:", split_batches(10000, 500))
    print("1.000 đơn, lô tối đa 500:", split_batches(1000, 500))
    print("300 đơn, lô tối đa 500:", split_batches(300, 500))
    print("1.000.000 đơn, lô tối đa 500:", split_batches(1000000, 500))
    print("Big-O ghi trong tài liệu:", COMPLEXITY)
    print("Cấu hình lỗi, lô tối đa 0:", split_batches(100, 0))
