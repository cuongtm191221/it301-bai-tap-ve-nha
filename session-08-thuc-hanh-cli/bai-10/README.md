# Tối ưu nhật ký bút toán có hoàn tác trên MISA

### 1. Bối cảnh & Vấn đề

![Kế toán dùng MISA ghi và hoàn tác bút toán](minh_hoa.png)

*Kế toán dùng MISA ghi và hoàn tác bút toán*

Phần mềm kế toán **MISA** cho phép kế toán ghi **bút toán** (mã `BTxxxx`, diễn giải, số tiền: dương là thu, âm là chi) và **hoàn tác** bút toán vừa ghi; sau mỗi thao tác, màn hình hiện lại **số dư** và các bút toán gần nhất.

Lớp `SlowJournal` trong `but_toan.py` (danh sách liên kết đơn, chỉ có `head`) cho kết quả đúng, nhưng cuối kỳ có hàng nghìn bút toán: mỗi lần ghi, hoàn tác hay xem số dư đều đi lại từ đầu, kế toán phải chờ. Đội kỹ thuật cần lớp `FastJournal` dùng **danh sách liên kết đôi**, **cùng phương thức, cùng kết quả, cùng lỗi** với bản cũ, và giải thích vì sao bản cũ chậm.

Bạn xây dựng module **"MISA Journal Undo CLI"**.

### 2. Yêu cầu nghiệp vụ

Nhật ký mẫu: `make_journal(FastJournal)` có 4 bút toán. `Node`, `DNode`, `SlowJournal`, `money`, `make_journal`, `workload` có sẵn, **không sửa**.

**Chức năng 1 — Xem k bút toán gần nhất.** **Chức năng 2 — Ghi bút toán.** **Chức năng 3 — Hoàn tác bút toán cuối** (mã không dùng lại). **Chức năng 4 — Xem số dư.**

**Chức năng 5 — Đo** `workload` trên hai lớp với n = 500, 1.000, 2.000. **Chức năng 6 — Thoát.**

`FastJournal`: `add_last`, `remove_last`, `size`, `balance` không duyệt danh sách; `recent(k)` đi qua tối đa k node; `workload(FastJournal, 100000)` trong 1 giây.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== MISA - NHẬT KÝ BÚT TOÁN =====
1. Xem bút toán gần nhất
2. Ghi bút toán
3. Hoàn tác bút toán cuối
4. Xem số dư
5. Đo bản cũ và bản mới
6. Thoát
Chọn chức năng (1-6): 3
Đã hoàn tác BT0004 (+7.200.000đ).

[menu chính]
Chọn chức năng (1-6): 4
Số dư: +5.150.000đ (3 bút toán)

[menu chính]
Chọn chức năng (1-6): 2
Diễn giải: Chi tiền điện
Số tiền (âm là chi): -1250000
Đã ghi BT0005: -1.250.000đ.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 5 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | bản cũ (ms) | bản mới (ms)
500 | 15.9 | 0.3
1000 | 55.3 | 0.5
2000 | 208.0 | 1.0
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ.** Kiểm tra trên 200 chuỗi thao tác ngẫu nhiên (ghi đúng, ghi sai, hoàn tác, xem): cùng kết quả, cùng lỗi.

**Bẫy 2 — Hoàn tác hết.** Node cuối cùng bị xóa thì `head`, `tail` về `None`, số dư về 0; ghi tiếp vẫn đúng.

**Bẫy 3 — Số dư luôn đúng.** Không duyệt khi xem số dư nên phải cập nhật ở mọi chỗ thêm, xóa.

**Bẫy 4 — Nhập sai.** Diễn giải trống hoặc dài; số tiền 0, `-0`, thập phân, chữ; k không phải số nguyên dương; hoàn tác khi rỗng; menu sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Phân tích `SlowJournal`: số node đi qua của `add_last`, `remove_last`, `balance`, `recent` theo n; tổng cho `workload(n)`; Big-O.
- Thiết kế `FastJournal` (sơ đồ `prev`, `next` khi hoàn tác); Big-O từng phương thức; bảng số đo chức năng 5 trên máy bạn.

**(3) Nghiên cứu mở rộng (mục cuối `PHAN_TICH.md`, được hỏi AI, phải ghi nguồn)**

- `list.append`, `list.pop()` cũng nhanh ở cuối; tìm hiểu khi nào danh sách đôi vẫn đáng dùng (gỡ một node ở giữa khi đã có tham chiếu tới node) và cái giá bộ nhớ của `prev`.
- Tạo `nghien_cuu.py`: so `sys.getsizeof` (cộng `__dict__`) của `Node` và `DNode`; viết hàm gỡ một node bất kỳ của `FastJournal` khi biết node đó (cập nhật số dư, kích thước) và chạy thử trên node giữa, node đầu, node cuối.

**(2) Triển khai code**

- Viết các hàm trong `but_toan.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session08_TH10`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-08-thuc-hanh-cli/bai-10 rồi chép các tệp vào kho: `but_toan.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`, `nghien_cuu.py (tự tạo)`.
2. Mức AI: AI-0 cho phân tích và mã; AI-1 cho nghiên cứu mở rộng (ghi nguồn, tự kiểm chứng).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
