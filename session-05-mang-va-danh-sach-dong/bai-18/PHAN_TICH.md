# Phân tích và thiết kế: bảng điều phối cuốc xe

## 1. Input / Output

| Hàm / phương thức | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về trong các bẫy |
|---|---|---|---|
| `DispatchQueue.add` | | | |
| `DispatchQueue.next` | | | |
| `DispatchQueue.cancel` | | | |
| `DispatchQueue.view` | | | |
| `handle` | | | |

## 2. Cách lưu hàng chờ; khi nào dọn; vì sao O(1) khấu hao

## 3. Chi phí add, cancel, view

## 4. Trạng thái qua 6 lệnh đầu

| Lệnh | Bên trong (_items và thông tin thêm) | Phản hồi |
|---|---|---|
| | | |

## 5. Độ phức tạp

| Thao tác | Thời gian |
|---|---|
| | |

## Nghiên cứu mở rộng

collections.deque:

| n | list.pop(0) | DispatchQueue | deque.popleft() |
|---|---|---|---|
| 25.000 | | | |
| 50.000 | | | |
| 100.000 | | | |

Phiên bản Python và máy đo:

Khi nào chọn deque:

Nguồn đã đọc:

1.
2.
