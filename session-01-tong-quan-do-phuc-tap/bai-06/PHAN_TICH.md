# Phân tích lỗi: chia lô đơn hàng cho kho

## 1. Kiểu dữ liệu của batch / 2; biểu thức chia đôi làm tròn lên

## 2. Chạy tay 1.000 đơn, sức chứa 500

| Lượt | batch trước | Điều kiện batch >= capacity | batch sau |
|---|---|---|---|
| 1 | | | |

Cách sửa điều kiện:

## 3. Vì sao capacity = 0 làm vòng lặp không dừng

| Lượt | batch |
|---|---|
| 1 | |

Kiểm tra cần thêm trước vòng lặp:

## 4. Số lần chia đôi theo n

| n | Số lần chia |
|---|---|
| 1.000 | |
| 10.000 | |
| 100.000 | |
| 1.000.000 | |

## 5. Vì sao là O(log n)

## 6. Ước lượng với 8.000.000 đơn
