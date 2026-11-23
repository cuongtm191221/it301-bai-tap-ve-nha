# Phân tích và thiết kế: phân loại độ phức tạp từ số đo

## 1. Input / Output

| Hàm | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Báo lỗi / trả về trong các bẫy |
|---|---|---|---|
| `check_measurements` | | | |
| `growth_ratios` | | | |
| `classify` | | | |
| `report_line` | | | |

## 2. Tỉ lệ của từng lớp khi n tăng gấp đôi; vì sao các ngưỡng tách được các lớp

| Lớp | Số bước n = 1.000 | n = 2.000 | Tỉ lệ |
|---|---|---|---|
| O(1) | | | |
| O(log n) | | | |
| O(n) | | | |
| O(n log n) | | | |
| O(n²) | | | |

## 3. Vì sao check_measurements trả về bản sao

## 4. Độ phức tạp

| Hàm | Thời gian | Bộ nhớ phụ |
|---|---|---|
| | | |

## Nghiên cứu mở rộng

timeit và time.perf_counter:

| Hàm | n = 1.000 | 2.000 | 4.000 | 8.000 | classify |
|---|---|---|---|---|---|
| O(n) | | | | | |
| O(n²) | | | | | |

Phiên bản Python và máy đo:

Vì sao phân loại bằng thời gian kém ổn định:

Nguồn đã đọc:

1.
2.
