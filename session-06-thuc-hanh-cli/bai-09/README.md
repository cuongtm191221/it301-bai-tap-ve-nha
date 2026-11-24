# Tối ưu chia chuyến giao hàng của Sendo

### 1. Bối cảnh & Vấn đề

![Điều phối viên Sendo chờ hệ thống chia chuyến xe](minh_hoa.png)

*Điều phối viên Sendo chờ hệ thống chia chuyến xe*

Kho **Sendo** gom đơn chờ giao theo thứ tự đặt; mỗi đơn có mã `SDxx` và giá trị (đồng), giá trị **0** là đơn chưa thanh toán và không được giao. Mỗi tối, điều phối viên **chia chuyến**: lấy lần lượt các đơn đã thanh toán, đủ `size` đơn thì thành một chuyến xe, chuyến cuối có thể thiếu.

Hàm `batch_slow` trong `chia_chuyen.py` cho kết quả đúng và đã dùng nhiều năm, nhưng mùa sale có hàng trăm nghìn đơn và việc chia chuyến chạy rất lâu. Đội kỹ thuật cần **viết lại** thành `batch_fast` cho **đúng y hệt** kết quả cũ (kể cả lỗi), chỉ dùng list, và giải thích vì sao bản cũ chậm.

Bạn xây dựng module **"Sendo Delivery Batching CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_orders()` trả về 8 đơn (xem `chia_chuyen.py`); `batch_slow` là hàm Có sẵn, **không sửa**.

**Chức năng 1 — Xem đơn chờ giao.** **Chức năng 2 — Thêm đơn** (mã và giá trị). **Chức năng 3 — Chia chuyến** bằng `batch_fast`: in từng chuyến `Chuyến <i>: <các mã> | <tổng>` rồi `Tổng: <a> chuyến, <b> đơn.`

**Chức năng 4 — Đo** bản cũ và bản mới với n = 2.000, 4.000, 8.000 (50 đơn mỗi chuyến). **Chức năng 5 — Thoát.**

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== SENDO - CHIA CHUYẾN GIAO HÀNG =====
1. Xem đơn chờ giao
2. Thêm đơn
3. Chia chuyến
4. Đo bản cũ và bản mới
5. Thoát
Chọn chức năng (1-5): 1
SD01 | 250.000đ
SD02 | 0đ | chưa thanh toán
SD03 | 480.000đ
SD04 | 120.000đ
SD05 | 0đ | chưa thanh toán
SD06 | 315.000đ
SD07 | 99.000đ
SD08 | 560.000đ

[menu chính]
Chọn chức năng (1-5): 3
Số đơn mỗi chuyến: 4
Chuyến 1: SD01, SD03, SD04, SD06 | 1.165.000đ
Chuyến 2: SD07, SD08 | 659.000đ
Tổng: 2 chuyến, 6 đơn.

[menu chính]
Chọn chức năng (1-5): 2
Mã đơn: sd09
Giá trị (đồng): 150000
Đã thêm SD09 (150.000đ). Có 9 đơn.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | bản cũ (ms) | bản mới (ms)
2000 | 2.6 | 0.1
4000 | 12.7 | 0.2
8000 | 59.2 | 0.5
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ.** Kiểm tra trên 200 bộ ngẫu nhiên; danh sách rỗng hoặc toàn đơn chưa thanh toán ra list rỗng; `size` lớn hơn số đơn ra một chuyến.

**Bẫy 2 — Các chuyến độc lập.** Dùng lại một list mã đơn rồi xóa nó cho chuyến sau sẽ làm rỗng cả chuyến trước.

**Bẫy 3 — Ràng buộc.** Không gọi bản cũ, không làm đổi danh sách đơn; 200.000 đơn trong 1 giây.

**Bẫy 4 — Dữ liệu sai.** `size` bằng 0, âm, không phải số; mã sai dạng, trùng (`sd09` là `SD09`); giá trị âm, số thập phân: đúng thông báo của đề.

**Bẫy 5 — Menu sai.** `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.`

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Phân tích `batch_slow`: mỗi dòng `queue = queue[1:]`, `codes = codes + [code]`, `batches = batches + [...]` chép bao nhiêu phần tử; Big-O thời gian và bộ nhớ phụ theo n.
- Thiết kế `batch_fast`; Big-O; bảng số đo chức năng 4 trên máy bạn.

**(3) Nghiên cứu mở rộng (mục cuối `PHAN_TICH.md`, được hỏi AI, phải ghi nguồn)**

- Tìm hiểu mỗi ô của list Python chứa gì; vì sao `sys.getsizeof` của list không tính các tuple đơn bên trong; `tracemalloc` đo khác gì.
- Tạo `nghien_cuu.py`: với 100.000 đơn, in `sys.getsizeof` của list và bộ nhớ đỉnh `tracemalloc` khi tạo list; so sánh bộ nhớ đỉnh của `batch_slow` và `batch_fast` trên 8.000 đơn.

**(2) Triển khai code**

- Viết các hàm trong `chia_chuyen.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session06_TH09`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-06-thuc-hanh-cli/bai-09 rồi chép các tệp vào kho: `chia_chuyen.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`, `nghien_cuu.py (tự tạo)`.
2. Mức AI: AI-0 cho phân tích và mã; AI-1 cho nghiên cứu mở rộng (ghi nguồn, tự kiểm chứng).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
