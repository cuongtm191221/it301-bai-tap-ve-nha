# Phân tích và thiết kế: mã xác thực theo bộ đếm

## 1. Input / Output

| Hàm | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về trong các bẫy |
|---|---|---|---|
| `otp_value_v1(seed, counter, mod)` | | | |
| `otp_value_v2(seed, counter, mod)` | | | |
| `otp_message(seed, counter, mod)` | | | |

## 2. Giải pháp 1

Ý tưởng:

Minh họa trên ví dụ ở mục 1:

Mã giả:

Ba câu hỏi kiểm tra (nếu là đệ quy); độ sâu call stack lớn nhất:

## 3. Giải pháp 2

Ý tưởng:

Minh họa trên ví dụ ở mục 1:

Mã giả:

Ba câu hỏi kiểm tra (nếu là đệ quy); độ sâu call stack lớn nhất:

## 4. Đo thời gian và số lời gọi

| Kích thước | Giải pháp 1 (giây) | Giải pháp 2 (giây) | Số lời gọi GP1 | Số lời gọi GP2 |
|---|---|---|---|---|
| | | | | |

Phiên bản Python và máy đo:

## 5. So sánh

| Tiêu chí | Giải pháp 1 | Giải pháp 2 |
|---|---|---|
| Thời gian (Big-O) | | |
| Bộ nhớ phụ, kể cả call stack (Big-O) | | |
| Kết quả đo | | |
| Dễ đọc, dễ bảo trì | | |
| Phù hợp với bối cảnh | | |

Giải pháp được chọn và lý do:

## 6. Chạy tay

| Lời gọi / vòng | Giải pháp 1 | Giải pháp 2 |
|---|---|---|
| | | |

Tổng số phép nhân: giải pháp 1 ..., giải pháp 2 ...
