# Hệ thống tính phương án xếp pallet cho kho Vinamilk

### 1. Bối cảnh & Vấn đề

![Trưởng kho Vinamilk lên phương án xếp pallet](minh_hoa.png)

*Trưởng kho Vinamilk lên phương án xếp pallet*

Kho **Vinamilk** Bình Dương có các dãy kệ dài n mét, được lấp kín bằng pallet loại **1 mét** và **2 mét** xếp nối nhau. Phòng kế hoạch muốn biết có bao nhiêu cách xếp để đánh giá độ linh hoạt khi xếp các lô sữa khác nhau. Pallet đầu tiên dài 1 mét thì phần còn lại dài n − 1; dài 2 mét thì còn n − 2, nên:

```plaintext
ways(1) = 1     ways(2) = 2     ways(n) = ways(n - 1) + ways(n - 2)
```

Bản đệ quy viết thẳng theo công thức chạy tức thì với dãy 10 mét nhưng với dãy 40 mét thì chờ rất lâu; dãy 1.000 mét thì bản có nhớ kết quả cũng báo `RecursionError`. Trưởng kho muốn thấy **vì sao** chậm (đếm số lời gọi), có bản nhanh (`lru_cache`), bản cho dãy dài (vòng lặp), và số đo.

Bạn xây dựng module **"Vinamilk Pallet Planner CLI"**.

### 2. Yêu cầu nghiệp vụ

**Chức năng 1 — Số cách xếp một dãy kệ** (1–1.000 m): `ways` dùng `ways_cached` khi n ≤ 400, ngược lại dùng `ways_loop`; kết quả quá 30 chữ số thì in `số có <k> chữ số`.

**Chức năng 2 — Số lời gọi của bản không nhớ** (1–30 m): `count_calls` tự tính bằng đệ quy, không chạy `ways_naive`.

**Chức năng 3 — Liệt kê các cách xếp** (1–8 m): `layouts`, cách bắt đầu bằng pallet 1 mét trước.

**Chức năng 4 — Đo** `ways_naive` và `ways_cached` (xóa cache trước mỗi lần) với n = 20, 24, 28. **Chức năng 5 — Thoát.**

`ways_naive`, `count_calls` viết bằng đệ quy, không vòng lặp; `ways_cached` dùng `functools.lru_cache`.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== VINAMILK BÌNH DƯƠNG - XẾP PALLET =====
1. Số cách xếp một dãy kệ
2. Số lời gọi của bản không nhớ
3. Liệt kê các cách xếp
4. Đo bản không nhớ và bản lru_cache
5. Thoát
Chọn chức năng (1-5): 1
Chiều dài dãy kệ (m): 10
Dãy 10 m có 89 cách xếp (tính bằng lru_cache).

[menu chính]
Chọn chức năng (1-5): 1
Chiều dài dãy kệ (m): 90
Dãy 90 m có 4660046610375530309 cách xếp (tính bằng lru_cache).

[menu chính]
Chọn chức năng (1-5): 1
Chiều dài dãy kệ (m): 1000
Dãy 1000 m có số có 209 chữ số cách xếp (tính bằng vòng lặp).

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | không nhớ (ms) | lru_cache (ms)
20 | 0.6 | 0.005
24 | 4.0 | 0.004
28 | 27.4 | 0.005
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Trường hợp cơ sở.** n = 1 và n = 2 phải đúng (1 và 2 cách); `count_calls(1)`, `count_calls(2)` là 1.

**Bẫy 2 — Dãy dài.** n = 1.000 phải ra kết quả (209 chữ số) trong 2 giây, không `RecursionError`, không tăng giới hạn đệ quy.

**Bẫy 3 — Giới hạn từng chức năng.** Chiều dài ngoài khoảng cho phép hoặc không phải số nguyên: `Lỗi: Chiều dài phải là số nguyên từ 1 đến <giới hạn> mét`.

**Bẫy 4 — Liệt kê không trùng.** 8 mét có đúng 34 cách khác nhau.

**Bẫy 5 — Menu sai.** `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.`

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Vẽ cây lời gọi của `ways_naive(5)`; những lời gọi nào bị lặp lại? Bảng số lời gọi với n = 10, 20, 25, 30; n tăng 1 thì số lời gọi tăng khoảng bao nhiêu lần?
- Vì sao `lru_cache` nhanh hơn (mỗi n tính mấy lần)? Vì sao nó vẫn gặp `RecursionError` khi n lớn? Bảng số đo chức năng 4 trên máy bạn.

**(2) Triển khai code**

- Viết các hàm trong `xep_pallet.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session04_TH06`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-04-thuc-hanh-cli/bai-06 rồi chép các tệp vào kho: `xep_pallet.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
