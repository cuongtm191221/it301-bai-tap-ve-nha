# Phân tích và thiết kế: ước lượng thời gian chạy báo cáo đêm

## 1. Input / Output

| Hàm | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về trong các bẫy |
|---|---|---|---|
| `normalize(complexity)` | | | |
| `estimate_steps(complexity, n)` | | | |
| `growth_ratio(complexity, n1, n2)` | | | |
| `fits_window(complexity, n, steps_per_second, seconds)` | | | |

## 2. Các bước chuẩn hóa

| Cách viết | Sau bước 1 | Sau bước 2 | ... | Kết quả |
|---|---|---|---|---|
| " o(log N) " | | | | |
| "O( n log n )" | | | | |
| "O(n²)" | | | | |

## 3. Mã giả của estimate_steps; vì sao dùng halvings

## 4. growth_ratio của O(n) và O(log n)

## 5. Độ phức tạp

| Hàm | Thời gian | Lý do |
|---|---|---|
| `halvings` | | |
| `estimate_steps` | | |
