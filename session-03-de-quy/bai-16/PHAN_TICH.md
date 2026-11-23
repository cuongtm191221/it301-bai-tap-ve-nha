# Phân tích và thiết kế: số cách chọn hộp quà

## 1. Input / Output

| Hàm | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về trong các bẫy |
|---|---|---|---|
| `choose_count_v1(n, k)` | | | |
| `choose_count_v2(n, k)` | | | |
| `prize_message(n, k)` | | | |

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

| Bước | Giải pháp 1 | Giải pháp 2 |
|---|---|---|
| | | |

Bài toán con bị tính lặp lại; tổng số lời gọi:
