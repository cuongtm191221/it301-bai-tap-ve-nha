# Phân tích và thiết kế: chia chuyến giao hàng Sendo

## 1. Input / Output

| Chức năng | Dữ liệu nhập (kiểu) | Kết quả in ra khi hợp lệ | Thông báo trong các bẫy |
|---|---|---|---|
| | | | |

## 2. Phân tích batch_slow

| Dòng lệnh | Số phần tử bị chép mỗi lần | Tổng theo n | Lý do |
|---|---|---|---|
| queue = queue[1:] | | | |
| codes = codes + [code] | | | |
| batches = batches + [...] | | | |

Big-O thời gian, bộ nhớ phụ:

## 3. Thiết kế batch_fast và số đo

Phiên bản Python, máy đo:

| n | Bản cũ (ms) | Bản mới (ms) |
|---|---|---|
| 2.000 | | |
| 4.000 | | |
| 8.000 | | |

## Nghiên cứu mở rộng

Mỗi ô của list chứa gì:

getsizeof và tracemalloc:

Kết quả nghien_cuu.py:

Nguồn đã đọc:

1.
2.
