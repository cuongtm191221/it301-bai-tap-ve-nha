# Phân tích lỗi: nút "Bài trước" và "Bài tiếp theo"

## 1. current ở đâu sau play_first() và next_song()? prev_song() hiện tại dời theo liên kết nào?

## 2. Dòng lệnh cần sửa trong prev_song

## 3. Lần bấm "Bài trước" thứ hai: current thành gì? Vì sao AttributeError?

## 4. Vì sao phải kiểm tra biên trước khi dời current?

## 5. Điều kiện "đang ở bài cuối", "đang ở bài đầu" chỉ dùng current

## 6. Trình phát mới mở: current là gì? next_song() báo lỗi gì?

## 7. play_first() khi danh sách chưa có bài: hiện tại làm gì, sửa thế nào?

## 8. Số bước mỗi lần bấm nút; nếu là danh sách liên kết đơn thì nút "Bài trước" tốn bao nhiêu?

## Bảng trạng thái (nên điền)

| Thao tác | current trước | current sau | Thông báo trả về |
|---|---|---|---|
| play_first() | None | | |
| next_song() | ZM001 | | |
| prev_song() | ZM002 | | |
| prev_song() | ZM001 | | |
| next_song() ở ZM003 | ZM003 | | |
