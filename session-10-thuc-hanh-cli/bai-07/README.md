# Hệ thống hàng chờ cáp treo có sức chứa giới hạn của Vinpearl

### 1. Bối cảnh & Vấn đề

![Nhân viên Vinpearl điều phối khách lên cáp treo](minh_hoa.png)

*Nhân viên Vinpearl điều phối khách lên cáp treo*

Ga cáp treo **Vinpearl** có khu chờ với **sức chứa giới hạn**. Khách mua vé (mã `CTxxxx`) và xếp hàng theo nhóm; nhóm chỉ được vào khi khu chờ còn đủ chỗ cho **cả nhóm**. Mỗi cabin rời ga chở tối đa **6** khách đầu hàng.

Bản đầu tiên cài hàng chờ bằng list: đúng nhưng ngày lễ (khu chờ lớn của hệ thống đặt vé trực tuyến, hàng chục nghìn chỗ) chạy chậm dần. Đội kỹ thuật cần **hai giải pháp cùng giao diện**: `QueueV1`, `QueueV2`; giải pháp 2 chỉ dùng một vùng lưu trữ cố định tạo một lần, mọi thao tác ở hai đầu không phải dời phần tử. So sánh bằng số đo và phân tích.

Bạn xây dựng module **"Vinpearl Cable Car Queue CLI"**.

### 2. Yêu cầu nghiệp vụ

Ga mẫu: `make_station()` sức chứa 12, có 8 khách. `Station`, `make_station`, `workload` có sẵn.

**Chức năng 1 — Xem hàng chờ**: các vé, `Đang chờ <k>/<sức chứa> khách` (thêm ` (đầy)` khi đầy). **Chức năng 2 — Khách xếp hàng** (nhóm 1 đến 10). **Chức năng 3 — Cabin rời ga.**

**Chức năng 4 — Chọn giải pháp** (menu phụ), giữ nguyên khách và thứ tự. **Chức năng 5 — Đo** với n = 20.000, 40.000, 80.000. **Chức năng 6 — Thoát.**

Giao diện hàng đợi: `enqueue`, `dequeue`, `peek`, `size`, `is_full`, `items` (thông báo lỗi trong docstring `QueueV1`). Giải pháp 2: khu chờ 100.000 chỗ, hai vòng thêm đầy rồi lấy hết trong 1 giây; không dùng `deque`.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== VINPEARL - CÁP TREO =====
1. Xem hàng chờ
2. Khách xếp hàng
3. Cabin rời ga
4. Chọn giải pháp hàng chờ
5. Đo so sánh hai giải pháp
6. Thoát
Chọn chức năng (1-6): 1
CT0001, CT0002, CT0003, CT0004, CT0005, CT0006, CT0007, CT0008
Đang chờ 8/12 khách

[menu chính]
Chọn chức năng (1-6): 4
1. Giải pháp 1  2. Giải pháp 2
Chọn giải pháp: 2
Đang dùng giải pháp 2, giữ 8 khách.

[menu chính]
Chọn chức năng (1-6): 2
Số khách: 5
Lỗi: Hàng chờ chỉ còn 4 chỗ

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 5 in dạng sau (máy soạn đề, Python 3.10):

```plaintext
n | giải pháp 1 (ms) | giải pháp 2 (ms)
20000 | 63.7 | 14.7
40000 | 271.0 | 29.0
80000 | 1092.0 | 58.1
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Lấy rồi thêm khi gần đầy.** Sức chứa 3: thêm a, b, c, lấy a, thêm d: hàng là b, c, d.

**Bẫy 2 — Nhóm không vừa.** Còn 4 chỗ mà nhóm 5 khách: không ai được thêm.

**Bẫy 3 — Đổi giải pháp giữa chừng.** Khách và thứ tự giữ nguyên.

**Bẫy 4 — Dữ liệu lớn.** Giải pháp 2 với 100.000 chỗ trong 1 giây.

**Bẫy 5 — Nhập sai.** Số khách ngoài 1–10, cabin rời ga khi hàng trống; menu phụ và menu chính sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Đề xuất hai giải pháp (ý tưởng, sơ đồ vùng lưu trữ sau từng thao tác của Bẫy 1, mã giả); số phần tử bị dời mỗi lần lấy ở mỗi giải pháp.
- Bảng so sánh 5 tiêu chí (tốc độ, bộ nhớ, độ dễ đọc, dễ bảo trì, phù hợp bối cảnh) kèm số đo chức năng 5 trên máy bạn; chọn giải pháp và giải thích.

**(2) Triển khai code**

- Viết các hàm trong `cap_treo.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session10_TH07`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-10-thuc-hanh-cli/bai-07 rồi chép các tệp vào kho: `cap_treo.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
