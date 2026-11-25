# Tối ưu hệ số giá cước theo nhu cầu của ứng dụng Be

### 1. Bối cảnh & Vấn đề

![Kỹ sư Be theo dõi số cuốc đặt theo phút](minh_hoa.png)

*Kỹ sư Be theo dõi số cuốc đặt theo phút*

Ứng dụng gọi xe **Be** ghi **số cuốc đặt trong từng phút**. Hệ số giá của mỗi phút dựa vào **đỉnh**: số cuốc lớn nhất trong **k phút gần nhất** (tính cả phút đó; những phút đầu có ít hơn k phút). Đỉnh dưới 100 cuốc thì hệ số 1.0, dưới 200 thì 1.2, từ 200 thì 1.5.

Hàm `peaks_slow` trong `gia_cuoc.py` cho kết quả đúng nhưng với dữ liệu cả tháng (hàng trăm nghìn phút) và cửa sổ dài thì chạy rất lâu. Cần **viết lại** thành `peaks_fast` cho **đúng y hệt** kết quả cũ và giải thích vì sao bản mới nhanh.

Bạn xây dựng module **"Be Surge Pricing CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_counts()` 15 phút, cửa sổ ban đầu k = 5. `check_window`, `peaks_slow`, `surge`, `make_counts`, `make_big_counts` có sẵn, **không sửa**.

**Chức năng 1 — Xem 10 phút gần nhất**: số cuốc, đỉnh, hệ số. **Chức năng 2 — Ghi số cuốc phút mới.** **Chức năng 3 — Đổi cửa sổ** (1 đến 1.440 phút).

**Chức năng 4 — Đo** bản cũ và bản mới trên 20.000 phút với k = 100, 200, 400. **Chức năng 5 — Thoát.**

`peaks_fast` không gọi bản cũ, không dùng `max()`, không cắt lát; 200.000 phút với k = 1.000 trong 1 giây.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== BE - HỆ SỐ GIÁ THEO NHU CẦU =====
1. Xem 10 phút gần nhất
2. Ghi số cuốc phút mới
3. Đổi cửa sổ (số phút)
4. Đo bản cũ và bản mới
5. Thoát
Chọn chức năng (1-5): 1
Cửa sổ 5 phút
Phút 6 | 210 cuốc | đỉnh 210 | x1.5
Phút 7 | 180 cuốc | đỉnh 210 | x1.5
Phút 8 | 75 cuốc | đỉnh 210 | x1.5
Phút 9 | 70 cuốc | đỉnh 210 | x1.5
Phút 10 | 65 cuốc | đỉnh 210 | x1.5
Phút 11 | 130 cuốc | đỉnh 180 | x1.2
Phút 12 | 95 cuốc | đỉnh 130 | x1.2
Phút 13 | 100 cuốc | đỉnh 130 | x1.2
Phút 14 | 60 cuốc | đỉnh 130 | x1.2
Phút 15 | 50 cuốc | đỉnh 130 | x1.2

[menu chính]
Chọn chức năng (1-5): 2
Số cuốc: 250
Đã ghi phút 16.

[menu chính]
Chọn chức năng (1-5): 2
Số cuốc: -5
Lỗi: Số cuốc phải là số nguyên từ 0 đến 10000

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
k | bản cũ (ms) | bản mới (ms)
100 | 17.3 | 3.2
200 | 30.2 | 3.1
400 | 54.4 | 3.2
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ.** 300 bộ ngẫu nhiên có nhiều số bằng nhau; danh sách rỗng.

**Bẫy 2 — Đỉnh rời cửa sổ.** Phút 6 có 210 cuốc: từ phút 11 (k = 5) đỉnh không còn là 210.

**Bẫy 3 — Cửa sổ ở biên.** k = 1 thì đỉnh bằng chính số cuốc; k lớn hơn số phút thì đỉnh là lớn nhất từ đầu.

**Bẫy 4 — Ràng buộc.** Như mục 2; không làm đổi dữ liệu.

**Bẫy 5 — Nhập sai.** Số cuốc âm, lớn hơn 10.000, thập phân; k ngoài khoảng, không phải số; menu sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Phân tích `peaks_slow`: số phần tử bị chép và bị so sánh theo n và k; Big-O; vì sao k càng lớn càng chậm.
- Thiết kế `peaks_fast` (chạy tay trên 15 phút mẫu, k = 5: nội dung cấu trúc phụ sau mỗi phút); Big-O; bảng số đo chức năng 4 trên máy bạn.

**(3) Nghiên cứu mở rộng (mục cuối `PHAN_TICH.md`, được hỏi AI, phải ghi nguồn)**

- Vì sao tổng số lần thêm, bỏ trong cấu trúc phụ của bạn không vượt quá 2n dù có vòng lặp lồng nhau (phân tích khấu hao); `collections.deque` lưu phần tử thế nào bên trong (khối cố định).
- Tạo `nghien_cuu.py`: đếm tổng số lần thêm, bỏ khi chạy trên 100.000 phút với k = 50 và k = 5.000, so với 2n; in `sys.getsizeof` của deque có 0, 1, 64, 65, 128 phần tử và nhận xét.

**(2) Triển khai code**

- Viết các hàm trong `gia_cuoc.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session10_TH10`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-10-thuc-hanh-cli/bai-10 rồi chép các tệp vào kho: `gia_cuoc.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`, `nghien_cuu.py (tự tạo)`.
2. Mức AI: AI-0 cho phân tích và mã; AI-1 cho nghiên cứu mở rộng (ghi nguồn, tự kiểm chứng).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
