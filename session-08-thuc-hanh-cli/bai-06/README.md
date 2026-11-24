# Hệ thống lệnh chuyển tiền chờ xử lý của Agribank

### 1. Bối cảnh & Vấn đề

![Giao dịch viên Agribank theo dõi lệnh chuyển tiền chờ xử lý](minh_hoa.png)

*Giao dịch viên Agribank theo dõi lệnh chuyển tiền chờ xử lý*

Cuối ngày, hệ thống **Agribank** gom các lệnh chuyển tiền liên ngân hàng và xử lý **theo thứ tự nhập**: lệnh nhập trước xử lý trước. Mỗi lệnh có mã `LCxxxx`, tài khoản nhận 13 chữ số và số tiền.

Bản cũ lưu lệnh bằng list và lấy lệnh bằng `pop(0)`; ngày cao điểm có hàng chục nghìn lệnh, việc xử lý chậm dần. Đội kỹ thuật cài lại bằng **danh sách liên kết đơn có `head`, `tail`, `size`**, nhưng một chuyên viên vận hành hỏi: mỗi node có tốn nhiều bộ nhớ hơn một ô list không? Bạn cần trả lời bằng **số đo thật** cả thời gian lẫn bộ nhớ.

Bạn xây dựng module **"Agribank Pending Transfers CLI"**.

### 2. Yêu cầu nghiệp vụ

Danh sách mẫu: `make_line()` có 4 lệnh. Lớp `Node` và hàm `money` có sẵn.

**Chức năng 1 — Xem lệnh chờ**: từng lệnh và `Tổng: <n> lệnh, <tổng tiền>`. **Chức năng 2 — Nhập lệnh.** **Chức năng 3 — Xử lý k lệnh** theo thứ tự (k lớn hơn số lệnh thì xử lý hết).

**Chức năng 4 — Đo**: lấy hết n phần tử từ đầu bằng `pop(0)` và bằng `remove_first` (n = 10.000, 20.000, 40.000), rồi bộ nhớ mỗi phần tử. **Chức năng 5 — Thoát.**

`add_last`, `remove_first` không duyệt danh sách, không dùng list Python; mã lệnh không dùng lại sau khi xử lý.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== AGRIBANK - LỆNH CHUYỂN TIỀN CHỜ XỬ LÝ =====
1. Xem lệnh chờ
2. Nhập lệnh
3. Xử lý lệnh
4. Đo so sánh với list
5. Thoát
Chọn chức năng (1-5): 1
LC0001 | 1500201234567 | 2.500.000đ
LC0002 | 3100205551234 | 15.000.000đ
LC0003 | 1500209876543 | 750.000đ
LC0004 | 5400201112223 | 120.000.000đ
Tổng: 4 lệnh, 138.250.000đ

[menu chính]
Chọn chức năng (1-5): 2
Tài khoản nhận: 1500207778889
Số tiền: 5000000
Đã nhập LC0005: 5.000.000đ. Còn 5 lệnh chờ.

[menu chính]
Chọn chức năng (1-5): 2
Tài khoản nhận: 15002077
Số tiền: 100000
Lỗi: Số tài khoản phải gồm 13 chữ số

[menu chính]
Chọn chức năng (1-5): 2
Tài khoản nhận: 1500207778889
Số tiền: 5000
Lỗi: Số tiền phải là số nguyên từ 10.000 đến 500.000.000

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (máy soạn đề, Python 3.10):

```plaintext
n | pop(0) (ms) | remove_first (ms)
10000 | 6.4 | 1.7
20000 | 31.1 | 3.7
40000 | 124.7 | 7.0
Bộ nhớ mỗi phần tử: list 8 byte, node 152 byte
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Lấy hết rồi nhập tiếp.** Lấy node cuối cùng đưa `head`, `tail` về `None`, `size` về 0; lệnh nhập sau đó có mã tiếp theo.

**Bẫy 2 — Đo đúng phần cần so.** Dựng dữ liệu nằm ngoài phần tính giờ; chỉ đo việc lấy hết từ đầu.

**Bẫy 3 — Bộ nhớ đúng máy.** Số byte lấy bằng `sys.getsizeof` theo công thức trong docstring, chạy trên chính máy kiểm tra.

**Bẫy 4 — Nhập sai.** Tài khoản không đủ 13 chữ số; số tiền ngoài khoảng, thập phân, âm; k không phải số nguyên dương; xử lý khi không còn lệnh; menu sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Big-O của `pop(0)` và `remove_first`, của việc lấy hết n phần tử bằng mỗi cách; bảng số đo chức năng 4 trên máy bạn, khi n gấp đôi mỗi cột tăng mấy lần.
- Bộ nhớ: mỗi ô list và mỗi node tốn bao nhiêu byte trên máy bạn, vì sao node tốn hơn; với 40.000 lệnh, chênh lệch khoảng bao nhiêu KiB. Kết luận cho Agribank.

**(2) Triển khai code**

- Viết các hàm trong `lenh_cho.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 5 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session08_TH06`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-08-thuc-hanh-cli/bai-06 rồi chép các tệp vào kho: `lenh_cho.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
