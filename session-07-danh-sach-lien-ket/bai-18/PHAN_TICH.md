# Phân tích và thiết kế: nút "Lùi" và "Tiến" trong phiên nghe

## 1. Input / Output

| Chức năng | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về trong các bẫy |
|---|---|---|---|
| `play(code, title)` | | | |
| `back()` | | | |
| `forward()` | | | |
| `to_lines()` | | | |

## 2. Thiết kế play

Hình trước và sau, các liên kết phải gán và thứ tự gán:

- Phiên nghe trống:
- `current` đang là `tail`:
- `current` ở giữa (bỏ nhánh sau):

## 3. Bảng trạng thái của kịch bản chạy thử

| Lệnh | head | tail | current | size |
|---|---|---|---|---|
| | | | | |

## 4. Big-O thời gian (n là số bài trong phiên nghe)

| Chức năng | Big-O | Lý do |
|---|---|---|
| `play` | | |
| `back` | | |
| `forward` | | |
| `to_lines` | | |

Số lần đổi liên kết để bỏ nhánh sau:

Chi phí cập nhật `size` trong thiết kế của tôi, và cách để `play` là O(1):

So sánh với list Python kèm chỉ số:

## Nghiên cứu mở rộng

History API và chức năng tương ứng trong lớp của tôi:

| Lệnh của trình duyệt | Chức năng tương ứng | Ghi chú |
|---|---|---|
| `history.back()` | | |
| `history.forward()` | | |
| `history.go(n)` | | |
| `history.pushState()` | | |

Thiết kế `go(steps)`: mã giả, các bẫy và thông báo đề xuất:

Giới hạn độ dài lịch sử: chi phí bỏ bài cũ nhất và các liên kết phải sửa:

Nguồn đã đọc:

1.
2.
