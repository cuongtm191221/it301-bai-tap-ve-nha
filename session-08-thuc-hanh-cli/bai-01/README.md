# Hệ thống hàng chờ nhận hàng tại bưu cục Viettel Post

### 1. Bối cảnh & Vấn đề

![Khách lấy số chờ nhận hàng tại bưu cục Viettel Post](minh_hoa.png)

*Khách lấy số chờ nhận hàng tại bưu cục Viettel Post*

Bưu cục **Viettel Post** cấp số thứ tự `VP001`, `VP002`, ... cho khách đến nhận hàng. Khách được gọi theo thứ tự lấy số; khách mới đứng cuối hàng; khách chờ lâu có thể **bỏ về** ở bất kỳ vị trí nào.

Phần mềm cũ lưu hàng chờ bằng list và gọi khách bằng `pop(0)`, mỗi lần gọi phải dời cả hàng; nhân viên cũng phản ánh màn hình đôi khi mất khách vừa lấy số sau khi có người bỏ về. Đội kỹ thuật quyết định cài hàng chờ bằng **danh sách liên kết đơn có `head` và `tail`**: gọi khách ở `head`, cấp số ở `tail`.

Bạn xây dựng module **"Viettel Post Waiting Line CLI"**.

### 2. Yêu cầu nghiệp vụ

Hàng chờ mẫu: `make_line()` đã cấp `VP001` đến `VP004`. Lớp `Node` và hàm `to_text` có sẵn.

**Chức năng 1 — Xem hàng chờ**: chuỗi `to_text()` và `Đang chờ: <n> khách`.

**Chức năng 2 — Lấy số**: số mới là `VP` + số lượt đã cấp (không dùng lại số cũ). **Chức năng 3 — Gọi khách tiếp theo**: hàng trống in `Không còn khách trong hàng chờ.`

**Chức năng 4 — Tra vị trí** (đếm từ 1). **Chức năng 5 — Khách bỏ về.** **Chức năng 6 — Thoát.**

Các phương thức của `WaitingLine` không dùng list Python để lưu.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== VIETTEL POST - HÀNG CHỜ NHẬN HÀNG =====
1. Xem hàng chờ
2. Lấy số
3. Gọi khách tiếp theo
4. Tra vị trí
5. Khách bỏ về
6. Thoát
Chọn chức năng (1-6): 1
VP001 -> VP002 -> VP003 -> VP004 -> None
Đang chờ: 4 khách

[menu chính]
Chọn chức năng (1-6): 3
Mời khách số VP001 đến quầy.

[menu chính]
Chọn chức năng (1-6): 2
Đã cấp số VP005. Phía trước có 3 khách.

[menu chính]
Chọn chức năng (1-6): 4
Số thứ tự: vp003
VP003 đang ở vị trí 2, còn 1 khách phía trước.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khách cuối bỏ về.** Xóa node `tail` mà không lùi `tail` thì khách lấy số sau đó bị mất khỏi hàng.

**Bẫy 2 — Gọi hết khách.** Lấy node cuối cùng phải đưa cả `head` và `tail` về `None`; sau đó lấy số vẫn đúng.

**Bẫy 3 — Hàng trống.** `remove_first` báo `IndexError("danh sách rỗng, không có phần tử để lấy")`; chương trình không dừng.

**Bẫy 4 — Nhập sai.** Số thứ tự gõ thường (`vp003` hợp lệ), sai dạng, không có trong hàng; menu sai: đúng thông báo của đề.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Vẽ sơ đồ `head`, `tail` và các node sau từng thao tác của màn hình mẫu (ít nhất: gọi khách, lấy số, khách cuối bỏ về).
- Bảng trường hợp biên của `remove_first` và `remove` (rỗng, một node, trúng `head`, trúng `tail`, không có) kèm kết quả mong đợi; Big-O của từng phương thức.

**(2) Triển khai code**

- Viết các hàm trong `hang_cho.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session08_TH01`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-08-thuc-hanh-cli/bai-01 rồi chép các tệp vào kho: `hang_cho.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
