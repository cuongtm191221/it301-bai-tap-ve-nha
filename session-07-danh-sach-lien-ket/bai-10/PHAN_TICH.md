# Phân tích và thiết kế: lịch sử "Nghe gần đây"

## 1. Input / Output

| Chức năng | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về trong các bẫy |
|---|---|---|---|
| `record(code, title)` | | | |
| `remove_song(code)` | | | |
| `to_lines()` | | | |
| `to_lines_oldest_first()` | | | |

## 2. Giải pháp

Cách tổ chức mã để không lặp các đoạn sửa liên kết:

Hình vẽ bốn trường hợp gỡ node và các liên kết phải sửa:

| Trường hợp | Liên kết phải sửa |
|---|---|
| Node ở đầu | |
| Node ở giữa | |
| Node ở cuối | |
| Node duy nhất | |

## 3. Mã giả của record (đủ bốn nhánh)

## 4. Big-O thời gian (n là số bài trong lịch sử)

| Chức năng | Big-O | Lý do |
|---|---|---|
| `record` | | |
| `remove_song` | | |
| `to_lines` | | |
| `to_lines_oldest_first` | | |

Trong `record`: bước O(n) là ..., bước O(1) là ...
