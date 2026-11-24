# Hệ thống sao kê tài khoản trên ứng dụng MB Bank

### 1. Bối cảnh & Vấn đề

![Kỹ sư MB Bank kiểm tra màn hình sao kê](minh_hoa.png)

*Kỹ sư MB Bank kiểm tra màn hình sao kê*

Ứng dụng **MB Bank** lưu lịch sử giao dịch của tài khoản thành list, cũ trước mới sau; mỗi giao dịch là `[mã, nội dung, số tiền]` (âm là tiền ra). Màn hình sao kê cần **mới nhất trước**. Hàm `statement_slow` (có sẵn) dựng sao kê bằng `insert(0, ...)` cho từng giao dịch: tài khoản cá nhân thì ổn, nhưng tài khoản doanh nghiệp vài chục nghìn giao dịch mỗi tháng thì mở sao kê rất chậm.

Nhóm phát triển muốn: viết lại bằng cách **đọc theo chỉ số từ cuối** và `append`; tận mắt **quan sát dung lượng list** tăng theo từng nấc bằng `sys.getsizeof`; và **đo** hai cách khi lịch sử dài gấp đôi.

Bạn xây dựng module **"MB Bank Statement CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_txs()` trả về 5 giao dịch; `make_big_txs(n)` tạo lịch sử giả lập (xem `sao_ke.py`).

**Chức năng 1 — Xem sao kê gần nhất.** Nhập k; in k giao dịch mới nhất trước, dạng `<mã> | <nội dung> | <+/-tiền>`.

**Chức năng 2 — Ghi giao dịch.** Nội dung và số tiền (số nguyên khác 0, có thể có dấu `+` hoặc `-`); mã tự sinh.

**Chức năng 3 — Quan sát dung lượng list.** Nhập n (1–100); `capacity_steps(n)` thêm lần lượt n phần tử vào list rỗng và trả về các mốc `(số phần tử, getsizeof)` mỗi khi dung lượng đổi.

**Chức năng 4 — Đo** `statement_slow` và `latest_first` với n = 20.000, 40.000, 80.000. **Chức năng 5 — Thoát.**

`latest_first` không dùng `insert`, `reverse()`, `[::-1]`, `reversed()`; không làm đổi lịch sử.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== MB BANK - SAO KÊ TÀI KHOẢN =====
1. Xem sao kê gần nhất
2. Ghi giao dịch
3. Quan sát dung lượng list
4. Đo bản cũ và bản mới
5. Thoát
Chọn chức năng (1-5): 1
Số giao dịch: 3
MB005 | Tiền nhà | -4.500.000đ
MB004 | Hoàn tiền Shopee | +120.000đ
MB003 | Chuyển khoản cho mẹ | -2.000.000đ

[menu chính]
Chọn chức năng (1-5): 2
Nội dung: Trà sữa
Số tiền (âm là tiền ra): -45000
Đã ghi MB006: -45.000đ.

[menu chính]
Chọn chức năng (1-5): 2
Nội dung: 
Số tiền (âm là tiền ra): 1000
Lỗi: Nội dung không được để trống

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 3 với n = 20 và chức năng 4 in dạng sau (máy soạn đề, Python 3.10; máy của bạn có thể khác):

```plaintext
số phần tử | getsizeof (byte)
0 | 56
1 | 88
5 | 120
9 | 184
17 | 248

n | insert(0) (ms) | đọc từ cuối (ms)
20000 | 66.9 | 1.25
40000 | 266.9 | 2.67
80000 | 1080.5 | 5.08
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — k ở biên.** k lớn hơn số giao dịch: in tất cả; lịch sử rỗng: không in gì.

**Bẫy 2 — Số tiền sai.** `0`, `-0`, `1.5`, chữ, chỉ có dấu: `Lỗi: Số tiền phải là số nguyên khác 0 (âm là tiền ra)`; nội dung trống: `Lỗi: Nội dung không được để trống`.

**Bẫy 3 — Mốc dung lượng đúng máy.** Kiểm tra so `capacity_steps` với số đo thật trên chính máy chạy, không phải con số chép từ đề.

**Bẫy 4 — Lịch sử dài.** 300.000 giao dịch: sao kê trong 1 giây.

**Bẫy 5 — Nhập sai.** k, n sai; menu sai: đúng thông báo của đề.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Số phần tử bị dịch khi `statement_slow` dựng sao kê n giao dịch; Big-O hai cách; bảng số đo chức năng 4 trên máy bạn (n gấp đôi thì mỗi cách tăng mấy lần).
- Bảng mốc dung lượng chức năng 3 với n = 40 trên máy bạn: các mốc đổi ở đâu, mỗi lần tăng thêm bao nhiêu byte; vì sao `append` tính trung bình vẫn nhanh dù thỉnh thoảng phải chép sang vùng nhớ mới.

**(2) Triển khai code**

- Viết các hàm trong `sao_ke.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session06_TH05`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-06-thuc-hanh-cli/bai-05 rồi chép các tệp vào kho: `sao_ke.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
