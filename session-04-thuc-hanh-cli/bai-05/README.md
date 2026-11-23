# Hệ thống lịch sử giao dịch ví ZaloPay

### 1. Bối cảnh & Vấn đề

![Kỹ sư ZaloPay xem lỗi khi lịch sử ví quá dài](minh_hoa.png)

*Kỹ sư ZaloPay xem lỗi khi lịch sử ví quá dài*

Ví **ZaloPay** lưu lịch sử giao dịch của mỗi người dùng; mỗi giao dịch là `[mã, loại "NAP" hoặc "CHI", số tiền]`. Số dư bằng tổng NAP trừ tổng CHI. Nhóm phát triển viết hàm tính số dư bằng **đệ quy theo chỉ số** (không cắt list). Mọi thứ ổn với người dùng mới, nhưng tài khoản của một cửa hàng có 20.000 giao dịch làm ứng dụng báo lỗi `RecursionError: maximum recursion depth exceeded`.

Trưởng nhóm yêu cầu: giữ bản đệ quy cho lịch sử ngắn, thêm bản **vòng lặp** cho lịch sử dài, chọn tự động theo độ dài, và dùng **số đo** cho thấy hai bản khác nhau thế nào. Không được sửa bằng cách tăng giới hạn đệ quy.

Bạn xây dựng module **"ZaloPay Wallet History CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_txs()` trả về 6 giao dịch (số dư 411.000đ); `make_big_txs(n)` tạo lịch sử giả lập (xem `vi_dien_tu.py`).

**Chức năng 1 — Xem số dư và khoản chi lớn nhất.** `balance` dùng `net_rec` khi lịch sử không quá `RECURSION_SAFE = 500` giao dịch, ngược lại dùng `net_loop`; in `Số dư: <tiền> (tính bằng <đệ quy hoặc vòng lặp>, <n> giao dịch)`. Lịch sử không quá 500 giao dịch thì in thêm khoản chi lớn nhất (`largest_spend`, đệ quy).

**Chức năng 2 — Nạp hoặc chi.** Mã tự sinh tiếp theo; không chi quá số dư.

**Chức năng 3 — Nạp lịch sử dài** (thêm 20.000 giao dịch giả lập).

**Chức năng 4 — Đo đệ quy và vòng lặp.** `benchmark` đo bằng `timeit` với n = 200, 400, 800; `recursion_fails(5000)` cho biết bản đệ quy có gặp `RecursionError` với 5.000 giao dịch không.

**Chức năng 5 — Thoát.**

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== ZALOPAY - LỊCH SỬ VÍ =====
1. Xem số dư và khoản chi lớn nhất
2. Nạp hoặc chi
3. Nạp lịch sử dài (giả lập)
4. Đo đệ quy và vòng lặp
5. Thoát
Chọn chức năng (1-5): 1
Số dư: 411.000đ (tính bằng đệ quy, 6 giao dịch)
Khoản chi lớn nhất: ZP003 120.000đ

[menu chính]
Chọn chức năng (1-5): 2
Loại (NAP/CHI): chi
Số tiền (đồng): 150000
Đã ghi ZP007. Số dư: 261.000đ

[menu chính]
Chọn chức năng (1-5): 2
Loại (NAP/CHI): CHI
Số tiền (đồng): 999999
Lỗi: Số dư không đủ: còn 261.000đ

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | đệ quy (ms) | vòng lặp (ms)
200 | 0.026 | 0.008
400 | 0.053 | 0.016
800 | 0.109 | 0.032
Đệ quy với 5000 giao dịch: gặp RecursionError
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Lịch sử dài.** 100.000 giao dịch: `balance` dùng vòng lặp, xong trong 2 giây, không `RecursionError`.

**Bẫy 2 — Đệ quy theo chỉ số.** `net_rec`, `largest_spend` không cắt list (`[i + 1:]`), không vòng lặp; `net_loop` không đệ quy.

**Bẫy 3 — Không có khoản chi.** `largest_spend` trả `None`; bằng nhau lấy khoản đứng trước.

**Bẫy 4 — Chi vượt số dư, dữ liệu sai.** Đúng thông báo trong docstring của `add_tx`; chi đúng bằng số dư thì được.

**Bẫy 5 — Menu sai.** `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.`

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Vẽ call stack của `net_rec` với 3 giao dịch; với n giao dịch có bao nhiêu khung trên stack cùng lúc, bộ nhớ phụ Big-O? Vì sao 5.000 giao dịch gây `RecursionError` (ghi giá trị `sys.getrecursionlimit()` trên máy bạn)?
- Bảng số đo chức năng 4 trên máy bạn; so sánh đệ quy và vòng lặp về thời gian, bộ nhớ, độ an toàn. Vì sao không sửa bằng cách tăng giới hạn đệ quy?

**(2) Triển khai code**

- Viết các hàm trong `vi_dien_tu.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session04_TH05`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-04-thuc-hanh-cli/bai-05 rồi chép các tệp vào kho: `vi_dien_tu.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
