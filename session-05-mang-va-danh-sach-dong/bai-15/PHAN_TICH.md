# Phản biện mã do AI viết: mảng động lưu đơn giao ghép

## 1. Các bộ dữ liệu thử

| Bộ | Dữ liệu | Phương thức | Kết quả đúng | Kết quả của mã AI | Đúng / Sai | Sau khi sửa |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |
| 6 | | | | | | |

## 2. Các lỗi tìm được

| Lỗi | Bộ dữ liệu làm lộ lỗi | Dòng lệnh gây lỗi | Nguyên nhân |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### Chạy tay lỗi 1

### Chạy tay lỗi 2

### Chạy tay lỗi 3

## 3. Độ phức tạp thật của remove_all

Số tham chiếu phải dịch khi xóa m đơn trong n đơn:

Big-O: ... ; thời gian đo với 40.000 đơn: ... giây (Python ..., máy ...)

## 4. Nhật ký giữ – sửa – loại bỏ

| Phần trong mã của AI | Quyết định (giữ / sửa / loại bỏ) | Lý do |
|---|---|---|
| Điều kiện mở rộng trong extend | | |
| `self._resize(2 * self._capacity)` | | |
| `return -1` trong index_of | | |
| `j += 1` sau khi pop trong remove_all | | |
| Lời giải thích "duyệt một lượt nên O(n)" | | |

## 5. Giải pháp thứ hai

Ý tưởng:

Mã giả:

| Tiêu chí | remove_all (đã sửa) | remove_all_fast |
|---|---|---|
| Thời gian (Big-O) | | |
| Bộ nhớ phụ (Big-O) | | |
| Thời gian đo | | |
| Dễ đọc | | |
| Phù hợp với 5 đơn / 200.000 đơn | | |

Giải pháp chọn và lý do:
