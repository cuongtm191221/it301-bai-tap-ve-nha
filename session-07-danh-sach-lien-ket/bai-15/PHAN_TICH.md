# Phản biện mã do AI viết: lọc bài trùng

## 1. Các bộ dữ liệu thử

| Bộ | Dữ liệu (dãy mã bài) | Kết quả đúng (số bài bỏ, danh sách, size, tail) | Kết quả của mã AI | Đúng / Sai | Sau khi sửa (hàm 1 / hàm 2) |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |

## 2. Các lỗi tìm được

| Lỗi | Bộ dữ liệu làm lộ lỗi | Dòng lệnh gây lỗi | Nguyên nhân |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### Chạy tay lỗi 1

| Bước | current | runner | runner.next | Danh sách lúc này |
|---|---|---|---|---|
| | | | | |

### Chạy tay lỗi 2

### Chạy tay lỗi 3

## 3. Nhật ký giữ – sửa – loại bỏ

| Phần trong mã của AI | Quyết định (giữ / sửa / loại bỏ) | Lý do |
|---|---|---|
| Hai vòng lặp `current`, `runner` | | |
| Lệnh gỡ node `runner.next = runner.next.next` | | |
| Lệnh `runner = runner.next` | | |
| Giá trị trả về `removed` | | |
| (phần bạn bổ sung) | | |

## 4. Giải pháp thứ hai

Ý tưởng:

Mã giả:

| Tiêu chí | Hai vòng lặp | Giải pháp thứ hai |
|---|---|---|
| Thời gian (Big-O) | | |
| Bộ nhớ dùng thêm (Big-O) | | |
| Số lượt duyệt | | |
| Dễ đọc | | |
| Phù hợp với 100 bài / 10.000 bài | | |

Giải pháp chọn cho bản chính thức và lý do:

## 5. Nhận xét về lời giải thích của AI

Với 10.000 bài, vòng lặp trong chạy khoảng ... lượt.

"Đã kiểm tra với ba test" có đủ để tin không? Vì sao?
