# Phân tích và thiết kế: hàng chờ ưu tiên của phòng nghe chung

## 1. Input / Output

| Chức năng | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về trong các bẫy |
|---|---|---|---|
| `add_request(code, title, vip)` | | | |
| `play_next()` | | | |
| `cancel(code)` | | | |
| `to_lines()` | | | |

## 2. Hai thiết kế xác định ranh giới VIP / thường

| | (a) Duyệt từ head mỗi lần | (b) Giữ con trỏ tới node VIP cuối |
|---|---|---|
| Chi phí một yêu cầu VIP | | |
| Chức năng nào phải cập nhật thêm, cập nhật gì | | |
| Nguy cơ sai | | |
| Cách tính vị trí cho thông báo | | |

Thiết kế được chọn và lý do:

## 3. Bốn trường hợp chèn yêu cầu VIP

Hình vẽ và các liên kết phải gán:

- Hàng chờ trống:
- Chưa có VIP nào:
- Đã có VIP và có bài thường:
- Chỉ toàn VIP:

## 4. Big-O thời gian (n là số bài đang chờ, v là số bài VIP)

| Chức năng | Big-O | Lý do |
|---|---|---|
| `add_request` (thường) | | |
| `add_request` (VIP) | | |
| `play_next` | | |
| `cancel` | | |
| `to_lines` | | |

## Nghiên cứu mở rộng

Heap và `heapq`: khái niệm, các hàm, chi phí:

Cách giữ thứ tự đến trước giữa các yêu cầu cùng mức ưu tiên khi dùng `heapq`:

| Tiêu chí | Danh sách liên kết của tôi | `heapq` |
|---|---|---|
| Thêm một yêu cầu | | |
| Lấy bài tiếp theo | | |
| Hủy một yêu cầu bất kỳ | | |
| Hiển thị cả hàng chờ theo thứ tự | | |
| Mở rộng lên năm mức ưu tiên | | |

Nguồn đã đọc:

1.
2.
