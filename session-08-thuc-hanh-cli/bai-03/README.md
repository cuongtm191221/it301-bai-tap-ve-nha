# Hệ thống danh sách đặt cọc trước của CellphoneS

### 1. Bối cảnh & Vấn đề

![Nhân viên CellphoneS sắp xếp danh sách khách đặt cọc](minh_hoa.png)

*Nhân viên CellphoneS sắp xếp danh sách khách đặt cọc*

Mỗi đợt mở bán điện thoại mới, **CellphoneS** nhận đặt cọc theo thứ tự; khách nhận máy theo **vị trí** trong danh sách. Khách hạng thành viên cao được **chèn vào một vị trí** do quản lý chọn; khách đổi ý thì **hủy suất theo vị trí**. Nhân viên thường xem danh sách theo trang 3 khách để gọi điện xác nhận.

Danh sách được cài bằng **danh sách liên kết đơn có `head`, `tail`** để chèn, hủy không phải dời cả danh sách. Bản đầu tiên chèn vào cuối thì khách đặt cọc sau đó bị chèn sai chỗ; hủy khách cuối thì danh sách hỏng.

Bạn xây dựng module **"CellphoneS Pre-order CLI"**.

### 2. Yêu cầu nghiệp vụ

Danh sách mẫu: `make_list()` có `KH101` đến `KH105`. Lớp `Node` và hàm `to_text` có sẵn. Vị trí người dùng nhập đếm từ 1.

**Chức năng 1 — Xem danh sách** (menu phụ): toàn bộ (`to_text` và `Tổng: <n> khách`) hoặc một trang 3 khách từ vị trí người dùng nhập.

**Chức năng 2 — Khách đặt cọc** (thêm cuối). **Chức năng 3 — Chèn khách ưu tiên** vào vị trí 1 đến n + 1. **Chức năng 4 — Hủy suất theo vị trí.** **Chức năng 5 — Thoát.**

Các phương thức của `PreorderList` không dùng list Python để lưu.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== CELLPHONES - ĐẶT CỌC TRƯỚC =====
1. Xem danh sách
2. Khách đặt cọc
3. Chèn khách ưu tiên
4. Hủy suất theo vị trí
5. Thoát
Chọn chức năng (1-5): 1
1. Toàn bộ  2. Một trang 3 khách
Chọn cách xem: 1
KH101 -> KH102 -> KH103 -> KH104 -> KH105 -> None
Tổng: 5 khách

[menu chính]
Chọn chức năng (1-5): 1
1. Toàn bộ  2. Một trang 3 khách
Chọn cách xem: 2
Từ vị trí: 4
4. KH104
5. KH105

[menu chính]
Chọn chức năng (1-5): 1
1. Toàn bộ  2. Một trang 3 khách
Chọn cách xem: x
Lựa chọn không hợp lệ.

[menu chính]
Chọn chức năng (1-5): 2
Mã khách: kh106
Đã nhận cọc của KH106, vị trí 6.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Chèn, hủy ở cuối.** Chèn vào vị trí n + 1 hoặc hủy vị trí n phải cập nhật `tail`.

**Bẫy 2 — Chèn, hủy ở đầu.** Vị trí 1 thay đổi `head`; danh sách rỗng thì node mới vừa là `head` vừa là `tail`.

**Bẫy 3 — Trang cuối.** Trang bắt đầu ở vị trí n - 1 chỉ có 2 khách.

**Bẫy 4 — Vị trí sai.** `0`, lớn hơn giới hạn, không phải số nguyên: đúng thông báo, giới hạn in theo số khách hiện tại.

**Bẫy 5 — Nhập sai.** Mã sai dạng, mã đã có (kiểm tra mã trước vị trí); danh sách trống khi hủy; menu phụ và menu chính sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Vẽ sơ đồ con trỏ khi chèn vào vị trí 1, giữa, n + 1 và khi hủy vị trí n: node nào đổi `next`, khi nào đổi `head`, `tail`.
- Số node phải đi qua khi chèn, hủy ở vị trí k; Big-O của `get`, `insert_at`, `remove_at`, `page`. So với list Python: chèn ở vị trí 1 tốn gì ở mỗi cách?

**(2) Triển khai code**

- Viết các hàm trong `dat_coc.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session08_TH03`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-08-thuc-hanh-cli/bai-03 rồi chép các tệp vào kho: `dat_coc.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
