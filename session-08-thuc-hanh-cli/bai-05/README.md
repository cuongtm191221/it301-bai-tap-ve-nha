# Hệ thống bảng thông báo đơn hàng của Tiki

### 1. Bối cảnh & Vấn đề

![Người dùng Tiki xem thông báo đơn hàng](minh_hoa.png)

*Người dùng Tiki xem thông báo đơn hàng*

Ứng dụng **Tiki** hiện **thông báo đơn hàng** mới nhất ở đầu bảng. Mỗi thay đổi trạng thái đơn sinh một thông báo; người dùng mua nhiều có hàng chục nghìn thông báo. Bản cũ lưu bằng list và thêm bằng `insert(0, ...)`.

Một kỹ sư đề xuất chuyển sang **danh sách liên kết đơn** vì thêm ở đầu không phải dời phần tử. Một kỹ sư khác lo màn hình "xem thông báo thứ i" sẽ chậm. Trưởng nhóm yêu cầu cài thử và **đo thật cả hai thao tác** trước khi quyết định.

Bạn xây dựng module **"Tiki Order Notices CLI"**.

### 2. Yêu cầu nghiệp vụ

Bảng mẫu: `make_feed()` có 5 thông báo. Lớp `Node` và hàm `parse_count` có sẵn.

**Chức năng 1 — Xem k thông báo mới nhất** (k lớn hơn số thông báo thì in tất cả). **Chức năng 2 — Thêm thông báo** (1 đến 60 ký tự). **Chức năng 3 — Xem thông báo thứ i** (mới nhất là 1).

**Chức năng 4 — Đo so sánh với list** (menu phụ): thêm n phần tử vào đầu (n = 10.000, 20.000, 40.000), hoặc đọc 200 vị trí rải đều (n = 2.000, 4.000, 8.000). **Chức năng 5 — Thoát.**

`NoticeFeed` không dùng list Python để lưu; `add_first` không duyệt danh sách.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== TIKI - THÔNG BÁO ĐƠN HÀNG =====
1. Xem các thông báo mới nhất
2. Thêm thông báo
3. Xem thông báo theo thứ tự
4. Đo so sánh với list
5. Thoát
Chọn chức năng (1-5): 1
Số thông báo: 3
1. TK1003 đã xác nhận
2. TK1001 đã giao
3. TK1002 đã xác nhận

[menu chính]
Chọn chức năng (1-5): 2
Nội dung: TK1003 đang giao
Đã thêm. Có 6 thông báo.

[menu chính]
Chọn chức năng (1-5): 1
Số thông báo: 10
1. TK1003 đang giao
2. TK1003 đã xác nhận
3. TK1001 đã giao
4. TK1002 đã xác nhận
5. TK1001 đang giao
6. TK1001 đã xác nhận

[menu chính]
Chọn chức năng (1-5): 3
Thứ tự: 2
TK1003 đã xác nhận

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (máy soạn đề, Python 3.10), thêm vào đầu rồi đọc theo vị trí:

```plaintext
n | list (ms) | danh sách liên kết (ms)
10000 | 15.21 | 2.58
20000 | 77.09 | 6.02
40000 | 287.33 | 10.40

n | list (ms) | danh sách liên kết (ms)
2000 | 0.01 | 3.60
4000 | 0.00 | 7.67
8000 | 0.02 | 14.88
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Thứ tự đếm từ 1.** Thông báo thứ 1 là `head`; thứ `size` là thông báo cũ nhất.

**Bẫy 2 — k lớn, bảng rỗng.** k lớn hơn số thông báo in tất cả; bảng rỗng trả list rỗng.

**Bẫy 3 — Số đo đúng cách.** Chỉ đo thao tác cần so sánh: dựng dữ liệu cho phép đọc theo vị trí nằm ngoài phần tính giờ.

**Bẫy 4 — Nhập sai.** Thứ tự ngoài 1..size (thông báo in đúng size hiện tại), k không phải số nguyên dương, nội dung trống hoặc dài; menu phụ và menu chính sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Big-O của thêm vào đầu và đọc vị trí i trên list và trên danh sách liên kết, kèm lý do (dời phần tử, đi qua node).
- Bảng số đo chức năng 4 trên máy bạn: khi n gấp đôi, mỗi cột tăng mấy lần; có khớp Big-O không?
- Kết luận cho Tiki: màn hình nào nên dùng cấu trúc nào, dựa trên số đo.

**(2) Triển khai code**

- Viết các hàm trong `thong_bao.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session08_TH05`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-08-thuc-hanh-cli/bai-05 rồi chép các tệp vào kho: `thong_bao.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
