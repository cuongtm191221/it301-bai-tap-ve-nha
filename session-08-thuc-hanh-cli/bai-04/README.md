# Hệ thống lịch sử xem của Galaxy Play

### 1. Bối cảnh & Vấn đề

![Người dùng Galaxy Play mở lịch sử xem trên TV](minh_hoa.png)

*Người dùng Galaxy Play mở lịch sử xem trên TV*

Ứng dụng **Galaxy Play** giữ **lịch sử xem** tối đa **6 mục**. Màn hình TV hiện mục **mới nhất trước**, trang tài khoản trên web hiện **cũ nhất trước**. Người dùng có thể xóa mục vừa xem, và khi đăng nhập thiết bị mới thì được nhập thêm các mục cũ từ thiết bị trước vào đầu lịch sử (nếu chưa đủ 6 mục).

Bản cũ lưu lịch sử bằng danh sách liên kết đơn: hiện "mới nhất trước" phải đảo cả danh sách, xóa mục vừa xem phải đi từ đầu. Đội kỹ thuật chuyển sang **danh sách liên kết đôi** (`prev`, `next`) có biến đếm `size`: thêm, xóa ở hai đầu không phải duyệt.

Bạn xây dựng module **"Galaxy Play Watch History CLI"**.

### 2. Yêu cầu nghiệp vụ

Lịch sử mẫu: `make_history()` có 4 mục. Lớp `DNode` và hàm `to_text` có sẵn; `head` là mục cũ nhất.

**Chức năng 1 — Xem lịch sử** (menu phụ): mới nhất trước (`to_text_backward`) hoặc cũ nhất trước (`to_text`), rồi `<n> mục`.

**Chức năng 2 — Xem một phim**: ghi vào cuối; vượt 6 mục thì bỏ mục cũ nhất. **Chức năng 3 — Xóa mục vừa xem.** **Chức năng 4 — Nhập mục cũ** vào đầu. **Chức năng 5 — Thoát.**

`add_first`, `add_last`, `remove_first`, `remove_last` không duyệt danh sách và cập nhật `size`; không dùng list Python để lưu.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== GALAXY PLAY - LỊCH SỬ XEM =====
1. Xem lịch sử
2. Xem một phim
3. Xóa mục vừa xem
4. Nhập mục cũ từ thiết bị khác
5. Thoát
Chọn chức năng (1-5): 1
1. Mới nhất trước  2. Cũ nhất trước
Chọn thứ tự: 1
Hoạt hình Thỏ con -> Trận cầu đỉnh cao -> Bếp nhà mình tập 3 -> Hành trình biển xanh -> None
4 mục

[menu chính]
Chọn chức năng (1-5): 1
1. Mới nhất trước  2. Cũ nhất trước
Chọn thứ tự: 2
Hành trình biển xanh -> Bếp nhà mình tập 3 -> Trận cầu đỉnh cao -> Hoạt hình Thỏ con -> None
4 mục

[menu chính]
Chọn chức năng (1-5): 2
Tên phim: Ký sự Tây Bắc
Đã ghi Ký sự Tây Bắc vào lịch sử.

[menu chính]
Chọn chức năng (1-5): 2
Tên phim: Bếp nhà mình tập 4
Đã ghi Bếp nhà mình tập 4 vào lịch sử.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Hai chiều phải khớp.** Sau mỗi thao tác, đi xuôi và đi ngược ra cùng các mục; `head.prev` và `tail.next` là `None`.

**Bẫy 2 — Node duy nhất.** Xóa node duy nhất ở bất kỳ đầu nào đưa cả `head`, `tail` về `None`, `size` về 0.

**Bẫy 3 — Giới hạn 6 mục.** Xem phim thứ bảy bỏ mục cũ nhất; nhập mục cũ khi đủ 6 bị từ chối.

**Bẫy 4 — Rỗng.** `remove_first`, `remove_last` báo `IndexError("danh sách rỗng, không có phần tử để xóa")`; chương trình báo `Lỗi: Lịch sử xem đang trống`.

**Bẫy 5 — Nhập sai.** Tên trống hoặc dài hơn 40 ký tự; menu phụ và menu chính sai: đúng thông báo của đề.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Vẽ sơ đồ `prev`, `next`, `head`, `tail` trước và sau `remove_first`, `remove_last` khi có 3 node và khi có 1 node.
- So sánh danh sách đơn và danh sách đôi cho bốn thao tác ở hai đầu và cho việc in mới nhất trước: Big-O, bộ nhớ thêm mỗi node.

**(2) Triển khai code**

- Viết các hàm trong `lich_su_xem.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 5 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session08_TH04`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-08-thuc-hanh-cli/bai-04 rồi chép các tệp vào kho: `lich_su_xem.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
