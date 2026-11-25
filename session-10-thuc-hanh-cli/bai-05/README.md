# Hệ thống hàng đợi yêu cầu thanh toán của ví MoMo

### 1. Bối cảnh & Vấn đề

![Kỹ sư MoMo theo dõi hàng đợi yêu cầu thanh toán](minh_hoa.png)

*Kỹ sư MoMo theo dõi hàng đợi yêu cầu thanh toán*

Ví **MoMo** đưa mỗi yêu cầu thanh toán (mã `YCxxxxx`, số điện thoại, số tiền) vào **hàng đợi**: gửi trước xử lý trước. Giờ cao điểm (giờ ăn trưa, ngày sale) hàng đợi có hàng chục nghìn yêu cầu.

Bản đầu tiên dùng list và `pop(0)`. Một kỹ sư đề xuất `LinkedQueue` tự cài (Session 09), một kỹ sư khác đề xuất `collections.deque`. Trưởng nhóm yêu cầu dùng `deque` cho hệ thống và **đo thật cả ba cách** (thời gian lấy hết hàng đợi, bộ nhớ) để ghi vào tài liệu thiết kế.

Bạn xây dựng module **"MoMo Payment Queue CLI"**.

### 2. Yêu cầu nghiệp vụ

Hàng đợi mẫu: `make_queue()` có 4 yêu cầu. `LinkedQueue`, `PaymentQueue` (có `requests` là `deque`), `money` có sẵn.

**Chức năng 1 — Xem hàng đợi.** **Chức năng 2 — Gửi yêu cầu** (số điện thoại, số tiền 1.000 đến 50.000.000). **Chức năng 3 — Xử lý k yêu cầu** đầu hàng (lấy bằng `popleft`).

**Chức năng 4 — Đo**: lấy hết n phần tử bằng ba cách (n = 20.000, 40.000, 80.000), rồi số byte của list và deque 80.000 phần tử. **Chức năng 5 — Thoát.**

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== MOMO - HÀNG ĐỢI THANH TOÁN =====
1. Xem hàng đợi
2. Gửi yêu cầu
3. Xử lý yêu cầu
4. Đo ba cách cài hàng đợi
5. Thoát
Chọn chức năng (1-5): 1
YC00001 | 0901112223 | 150.000đ
YC00002 | 0934556677 | 2.500.000đ
YC00003 | 0987001122 | 45.000đ
YC00004 | 0909090909 | 800.000đ
Đang chờ: 4 yêu cầu

[menu chính]
Chọn chức năng (1-5): 2
Số điện thoại: 0977123456
Số tiền: 300000
Đã nhận YC00005: 300.000đ.

[menu chính]
Chọn chức năng (1-5): 2
Số điện thoại: 977123456
Số tiền: 1000
Lỗi: Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0

[menu chính]
Chọn chức năng (1-5): 2
Số điện thoại: 0977123456
Số tiền: 999
Lỗi: Số tiền phải là số nguyên từ 1.000 đến 50.000.000

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (máy soạn đề, Python 3.10):

```plaintext
n | list.pop(0) (ms) | LinkedQueue (ms) | deque (ms)
20000 | 26.9 | 3.5 | 0.4
40000 | 125.0 | 6.9 | 0.8
80000 | 517.9 | 14.5 | 1.6
80000 phần tử: list 640056 byte, deque 660624 byte
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Thứ tự.** Xử lý theo thứ tự gửi; k lớn hơn số yêu cầu thì xử lý hết.

**Bẫy 2 — Đo đúng phần cần so.** Dựng ba hàng đợi ngoài phần tính giờ; chỉ đo việc lấy hết.

**Bẫy 3 — Số đo theo máy.** Bộ nhớ lấy bằng `sys.getsizeof` trên chính máy kiểm tra.

**Bẫy 4 — Nhập sai.** Số điện thoại, số tiền ngoài khoảng, k không phải số nguyên dương, xử lý khi hàng trống; menu sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Big-O của `pop(0)`, `dequeue`, `popleft` và của việc lấy hết n phần tử; bảng số đo chức năng 4 trên máy bạn (n gấp đôi thì mỗi cột tăng mấy lần).
- So sánh bộ nhớ list và deque trên máy bạn; ưu, nhược của `LinkedQueue` tự cài so với `deque` (tốc độ, bộ nhớ, công sức bảo trì). Kết luận cho MoMo.

**(2) Triển khai code**

- Viết các hàm trong `thanh_toan.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 5 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session10_TH05`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-10-thuc-hanh-cli/bai-05 rồi chép các tệp vào kho: `thanh_toan.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
