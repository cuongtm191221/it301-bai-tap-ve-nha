# Phân tích và thiết kế: trình quản lý danh sách phát bằng dòng lệnh

## 1. Input / Output

### Lớp Playlist

| Phương thức | Đầu vào (kiểu dữ liệu) | Trả về | Trường hợp đặc biệt |
|---|---|---|---|
| `add_last` | | | |
| `add_first` | | | |
| `find` | | | |
| `value_at` | | | |
| `remove` | | | |
| `to_lines` | | | |

### Hàm handle

| Lệnh | Dữ liệu cần tách ra | Thông báo thành công | Thông báo trong các bẫy |
|---|---|---|---|
| `THEM` | | | |
| `DAU` | | | |
| `BO` | | | |
| `TIM` | | | |
| `XEM` | | | |
| `DEM` | | | |

## 2. Thiết kế Playlist.remove

Hình vẽ bốn trường hợp và liên kết phải sửa:

## 3. Thiết kế handle

Trình tự kiểm tra một dòng lệnh (sơ đồ hoặc mã giả):

Vì sao kiểm tra dữ liệu nhập đặt ở `handle`, không đặt trong `Playlist`:

## 4. Big-O thời gian (n là số bài)

| Phương thức / lệnh | Big-O | Lý do |
|---|---|---|
| | | |

Lệnh `TIM` duyệt danh sách ... lượt, vì:

## Nghiên cứu mở rộng

Cách tổ chức bên trong của `deque`, thao tác O(1) và O(n):

| Cấu trúc | Thời gian thêm 20.000 bài vào đầu |
|---|---|
| list (`insert(0, ...)`) | |
| `deque` (`appendleft`) | |
| `Playlist` (`add_first`) | |

Phiên bản Python và máy đo:

Giải thích số đo bằng Big-O:

Lựa chọn cho công việc thật và lý do:

Nguồn đã đọc:

1.
2.
