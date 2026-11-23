# Hệ thống tích điểm thẻ thành viên của Highlands Coffee

### 1. Bối cảnh & Vấn đề

![Thu ngân Highlands Coffee tra điểm thẻ thành viên](minh_hoa.png)

*Thu ngân Highlands Coffee tra điểm thẻ thành viên*

**Highlands Coffee** lưu lịch sử hóa đơn của mỗi hội viên thành một list số tiền (đồng), cũ trước mới sau, ví dụ:

```python
SAMPLE_BILLS = [45000, 120000, 59000, 35000, 210000, 65000]
```

Mỗi hóa đơn được `số tiền // 10000` điểm; tổng điểm quyết định hạng thẻ (hàm `tier` có sẵn: Thành viên, Bạc từ 50, Vàng từ 100, Kim cương từ 200). Thu ngân cần xem lịch sử kèm điểm và hạng, thêm hóa đơn mới, đếm hóa đơn từ một ngưỡng (để tặng voucher) và xem hóa đơn lớn nhất.

Nhóm phát triển muốn bạn luyện **tư duy đệ quy** trên list: ba hàm tính toán phải viết **bằng đệ quy, không dùng vòng lặp** (tách phần tử đầu và phần còn lại), có trường hợp cơ sở đúng.

Bạn xây dựng module **"Highlands Membership CLI"**.

### 2. Yêu cầu nghiệp vụ

**Chức năng 1 — Xem lịch sử và điểm.** Mỗi hóa đơn một dòng có số thứ tự, rồi `Điểm: <p> - Hạng: <hạng>`.

**Chức năng 2 — Thêm hóa đơn.** Nhập số tiền; thêm vào cuối; in `Đã thêm hóa đơn <tiền>. Điểm mới: <p>.`

**Chức năng 3 — Đếm hóa đơn lớn.** Nhập ngưỡng; in `Có <k> hóa đơn từ <ngưỡng> trở lên.` (bằng ngưỡng cũng tính).

**Chức năng 4 — Hóa đơn lớn nhất.** In `Hóa đơn lớn nhất: <tiền>`, không dùng `max()`.

**Chức năng 5 — Thoát.** In `Cảm ơn quý khách. Hẹn gặp lại!`.

Ba hàm `total_points`, `count_big`, `largest` viết bằng đệ quy, không vòng lặp, không làm đổi lịch sử.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== HIGHLANDS COFFEE - THẺ THÀNH VIÊN =====
1. Xem lịch sử và điểm
2. Thêm hóa đơn
3. Đếm hóa đơn lớn
4. Hóa đơn lớn nhất
5. Thoát
Chọn chức năng (1-5): 1
1. 45.000đ
2. 120.000đ
3. 59.000đ
4. 35.000đ
5. 210.000đ
6. 65.000đ
Điểm: 51 - Hạng: Bạc

[menu chính]
Chọn chức năng (1-5): 2
Số tiền hóa đơn (đồng): 95000
Đã thêm hóa đơn 95.000đ. Điểm mới: 60.

[menu chính]
Chọn chức năng (1-5): 3
Ngưỡng (đồng): 60000
Có 4 hóa đơn từ 60.000đ trở lên.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Lịch sử rỗng, một hóa đơn.** Tổng điểm 0; đếm ra 0; lớn nhất trả `None` (chức năng 1, 4 in `Chưa có hóa đơn nào.`). Đây chính là trường hợp cơ sở của đệ quy.

**Bẫy 2 — Hóa đơn dưới 10.000đ.** Được 0 điểm; đúng 10.000đ được 1 điểm.

**Bẫy 3 — Số tiền, ngưỡng sai.** Số tiền ngoài 1.000–5.000.000 hoặc không phải số nguyên: `Lỗi: Số tiền phải là số nguyên từ 1.000 đến 5.000.000`; ngưỡng không phải số nguyên dương: `Lỗi: Ngưỡng phải là số nguyên dương`.

**Bẫy 4 — Menu sai.** In `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.` và hỏi lại.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Với mỗi hàm đệ quy: trường hợp cơ sở, bước đệ quy, vì sao chắc chắn dừng; vẽ chuỗi lời gọi của `total_points([45000, 120000, 59000])`.
- Một hội viên có 5.000 hóa đơn thì chuyện gì xảy ra với các hàm đệ quy này? Vì sao?

**(2) Triển khai code**

- Viết các hàm trong `tich_diem.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session04_TH01`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-04-thuc-hanh-cli/bai-01 rồi chép các tệp vào kho: `tich_diem.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
