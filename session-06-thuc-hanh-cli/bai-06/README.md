# Hệ thống phân tích giá đóng cửa cổ phiếu trên SSI iBoard

### 1. Bối cảnh & Vấn đề

![Chuyên viên dữ liệu SSI xem dãy giá đóng cửa](minh_hoa.png)

*Chuyên viên dữ liệu SSI xem dãy giá đóng cửa*

Ứng dụng **SSI iBoard** có mục "học phân tích dữ liệu" cho nhà đầu tư mới: giá đóng cửa các phiên của một mã (ví dụ FPT) lưu trong list số nguyên, phiên cũ trước. Người dùng xem k phiên gần nhất và giá trung bình, và hỏi một câu kinh điển: **nếu mua một lần và bán ở một phiên sau đó, trong quá khứ lãi nhiều nhất bao nhiêu?** (Bài chỉ để học xử lý mảng, không phải khuyến nghị đầu tư.)

Bản thử đầu tiên thử mọi cặp (phiên mua, phiên bán): dữ liệu 20 năm theo phút có hàng trăm nghìn mốc và chạy không xong. Nhóm cần cách **một lượt duyệt**, và **số đo** thời gian, bộ nhớ khi dữ liệu gấp đôi.

Bạn xây dựng module **"SSI Price Lab CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_prices()` trả về giá 10 phiên của FPT (xem `gia_co_phieu.py`).

**Chức năng 1 — Thêm giá phiên mới** (1.000–10.000.000đ). **Chức năng 2 — Xem k phiên gần nhất** và `Trung bình <k> phiên: <giá>` (làm tròn xuống).

**Chức năng 3 — Thời điểm mua bán tốt nhất trong quá khứ.** `best_trade`: in `Mua phiên <a>, bán phiên <b>: lãi <tiền> mỗi cổ phiếu.` hoặc `Không có cách mua bán nào có lãi.` Nhiều cách cùng lãi thì chọn phiên bán sớm nhất, rồi phiên mua sớm nhất. Một lượt duyệt, bộ nhớ phụ O(1).

**Chức năng 4 — Đo hiệu năng.** `benchmark` đo bằng `timeit` thời gian `best_trade` và lấy `sys.getsizeof` của list giá với n = 50.000, 100.000, 200.000. **Chức năng 5 — Thoát.**

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== SSI IBOARD - THEO DÕI GIÁ FPT =====
1. Thêm giá phiên mới
2. Xem k phiên gần nhất
3. Thời điểm mua bán tốt nhất trong quá khứ
4. Đo hiệu năng
5. Thoát
Chọn chức năng (1-5): 2
Số phiên: 3
102.800đ, 101.900đ, 103.500đ
Trung bình 3 phiên: 102.733đ

[menu chính]
Chọn chức năng (1-5): 3
Mua phiên 4, bán phiên 10: lãi 8.100đ mỗi cổ phiếu.

[menu chính]
Chọn chức năng (1-5): 1
Giá đóng cửa (đồng): 101000
Đã thêm phiên 11.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (máy soạn đề, Python 3.10):

```plaintext
n | best_trade (ms) | getsizeof list giá (byte)
50000 | 3.74 | 444376
100000 | 7.56 (x2.0) | 800984
200000 | 14.96 (x2.0) | 1624056
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Bán phải sau mua.** Giá giảm dần thì không có lãi; không được "bán" ở phiên trước phiên mua.

**Bẫy 2 — Cùng lãi.** `[5000, 3000, 3000, 6000, 6000]`: mua phiên 2, bán phiên 4.

**Bẫy 3 — Ít phiên.** Rỗng hoặc một phiên: không có lãi; k lớn hơn số phiên thì lấy tất cả.

**Bẫy 4 — Dữ liệu lớn.** 500.000 phiên trong 1 giây.

**Bẫy 5 — Nhập sai.** Giá ngoài khoảng hoặc không phải số nguyên, k không phải số nguyên dương, menu sai: đúng thông báo của đề.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- So sánh cách thử mọi cặp và cách một lượt: số phép so sánh theo n, Big-O, ước tính thời gian với 500.000 phiên; chạy tay `best_trade` trên 10 phiên mẫu (phiên thấp nhất đến hiện tại, lãi tốt nhất sau mỗi phiên).
- Bảng số đo chức năng 4 trên máy bạn: thời gian và `getsizeof` tăng bao nhiêu lần khi n gấp đôi; `getsizeof` của list giá có tính bộ nhớ của các số bên trong không?

**(2) Triển khai code**

- Viết các hàm trong `gia_co_phieu.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session06_TH06`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-06-thuc-hanh-cli/bai-06 rồi chép các tệp vào kho: `gia_co_phieu.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
