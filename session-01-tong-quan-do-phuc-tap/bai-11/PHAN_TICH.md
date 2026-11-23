# Phân tích và thiết kế: giảm giá hàng loạt

## 1. Input / Output

| Hàm | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về / báo lỗi trong các bẫy |
|---|---|---|---|
| `discounted_price(price, percent)` | | | |
| `apply_discount_in_place(prices, percent)` | | | |
| `discounted_copy(prices, percent)` | | | |
| `total_after_discount(prices, percent)` | | | |

## 2. Công thức làm tròn xuống đến nghìn đồng

| Giá gốc | Giảm 15% | Sau làm tròn |
|---|---|---|
| 259.000 | | |
| 99.000 | | |
| 1.500 | | |

## 3. Hình các list trong bộ nhớ sau mỗi hàm

## 4. Độ phức tạp

| Hàm | Thời gian | Bộ nhớ phụ |
|---|---|---|
| `discounted_price` | | |
| `apply_discount_in_place` | | |
| `discounted_copy` | | |
| `total_after_discount` | | |

Vì sao màn hình "Áp dụng" không dùng discounted_copy rồi gán đè:

## 5. Số lần kiểm tra percent; list có bị giảm giá dở dang không
