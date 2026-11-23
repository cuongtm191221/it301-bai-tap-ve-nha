# Phân tích và thiết kế: nút "Hoàn tác"

## 1. Input / Output

| Chức năng | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về trong các bẫy |
|---|---|---|---|
| `add_song(code, title)` | | | |
| `remove_song(code)` | | | |
| `undo()` | | | |
| `to_lines()` | | | |

## 2. Thiết kế nhật ký thao tác

| Câu hỏi thiết kế | Quyết định | Lý do |
|---|---|---|
| Mỗi thao tác ghi những thông tin gì? | | |
| Các thao tác nối với nhau thế nào? | | |
| Thao tác mới thêm ở đầu nào, lấy ra ở đầu nào? | | |
| Bỏ thao tác cũ nhất thế nào khi vượt limit? | | |

Hình vẽ nhật ký sau ba thao tác ở bẫy 5:

## 3. Hai phương án trả bài về chỗ cũ

| | Phương án 1 | Phương án 2 |
|---|---|---|
| Thông tin phải ghi | | |
| Cách đưa bài về chỗ cũ | | |
| Chi phí | | |
| Trường hợp dễ sai | | |

Phương án được chọn và lý do:

Vì sao phương án này vẫn đúng khi hoàn tác nhiều thao tác đan xen:

## 4. Mã giả của undo

## 5. Big-O thời gian

| Việc | Big-O | Lý do |
|---|---|---|
| `add_song` | | |
| `remove_song` | | |
| `undo` | | |
| `to_lines` | | |
| Ghi một thao tác vào nhật ký | | |
| Lấy thao tác gần nhất | | |
| Bỏ thao tác cũ nhất | | |

## Nghiên cứu mở rộng

Stack là gì, push và pop, vì sao hoàn tác dùng stack; nhật ký của tôi khác stack thuần túy ở điểm:

Thiết kế nút "Làm lại": cấu trúc cần thêm, thay đổi trong `undo`, điều xảy ra khi có thao tác mới:

Mã giả của `redo`:

Một ứng dụng có hoàn tác và một thao tác không hoàn tác được:

Nguồn đã đọc:

1.
2.
