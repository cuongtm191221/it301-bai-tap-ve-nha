# Phân tích và thiết kế: sắp xếp lại danh sách phát

## 1. Input / Output

| Chức năng | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về trong các bẫy |
|---|---|---|---|
| `add_song(code, title)` | | | |
| `insert_after(after_code, code, title)` | | | |
| `move_to_top(code)` | | | |
| `to_lines()` | | | |

## 2. Giải pháp

### insert_after: thứ tự gán hai liên kết, hình vẽ khi gán ngược thứ tự

### move_to_top: node cần giữ khi duyệt, hình vẽ hai trường hợp (bài ở giữa, bài ở cuối)

## 3. Mã giả

### insert_after

### move_to_top

## 4. Big-O thời gian (n là số bài)

| Chức năng | Big-O | Lý do |
|---|---|---|
| `add_song` | | |
| `insert_after` | | |
| `move_to_top` | | |
| `to_lines` | | |

Trong `move_to_top`: phần tìm tốn ..., phần gỡ và nối tốn ...

So với list Python:
