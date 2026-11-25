# Tối ưu hoàn tác, làm lại khi soạn văn bản trên VNPT Smart Office

### 1. Bối cảnh & Vấn đề

![Chuyên viên VNPT soạn công văn và bấm hoàn tác](minh_hoa.png)

*Chuyên viên VNPT soạn công văn và bấm hoàn tác*

Trình soạn công văn của **VNPT Smart Office** cho phép thêm dòng, sửa dòng, xóa dòng, **hoàn tác** và **làm lại**. Lớp `SlowEditor` trong `soan_van_ban.py` làm đúng bằng cách lưu **bản chụp toàn bộ văn bản** sau mỗi thao tác.

Với văn bản dài (biên bản, hợp đồng hàng nghìn dòng) và nhiều lần sửa, mỗi thao tác chép lại cả văn bản: trình soạn chậm và tốn bộ nhớ. Đội kỹ thuật cần lớp `FastEditor` **cùng phương thức, cùng kết quả, cùng mô tả, cùng lỗi** với bản cũ, nhưng không chép cả văn bản ở mỗi thao tác; đồng thời giải thích vì sao bản cũ chậm và tốn bộ nhớ.

Bạn xây dựng module **"VNPT Smart Office Undo CLI"**.

### 2. Yêu cầu nghiệp vụ

Văn bản mẫu: `make_editor(FastEditor)` có 3 dòng. `check_text`, `check_index`, `SlowEditor`, `make_editor`, `workload` có sẵn, **không sửa**.

**Chức năng 1 — Xem văn bản.** **Chức năng 2 — Thêm dòng.** **Chức năng 3 — Sửa dòng.** **Chức năng 4 — Xóa dòng.**

**Chức năng 5 — Hoàn tác.** **Chức năng 6 — Làm lại.** **Chức năng 7 — Đo** `workload` trên hai lớp với n = 500, 1.000, 2.000. **Chức năng 8 — Thoát.**

Mỗi thao tác trả về mô tả (`thêm dòng 4`, `sửa dòng 2`, `xóa dòng 1`); hoàn tác, làm lại trả về mô tả của thao tác tương ứng. `workload(FastEditor, 50000)` trong 1 giây.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== VNPT SMART OFFICE - SOẠN VĂN BẢN =====
1. Xem văn bản
2. Thêm dòng
3. Sửa dòng
4. Xóa dòng
5. Hoàn tác
6. Làm lại
7. Đo bản cũ và bản mới
8. Thoát
Chọn chức năng (1-8): 1
1| CÔNG VĂN SỐ 125/VNPT
2| Kính gửi: Phòng Kế hoạch
3| V/v: Lịch bảo trì hệ thống tháng 12

[menu chính]
Chọn chức năng (1-8): 3
Dòng số: 2
Nội dung mới: Kính gửi: Phòng Kỹ thuật
Đã sửa dòng 2.

[menu chính]
Chọn chức năng (1-8): 4
Dòng số: 1
Đã xóa dòng 1.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 7 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | bản cũ (ms) | bản mới (ms)
500 | 3.2 | 0.7
1000 | 12.3 | 1.2
2000 | 61.5 | 2.6
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ.** Kiểm tra trên 200 chuỗi thao tác ngẫu nhiên, gồm cả thao tác lỗi.

**Bẫy 2 — Hoàn tác xóa, sửa.** Dòng bị xóa trở lại đúng vị trí; dòng sửa trở lại nội dung cũ.

**Bẫy 3 — Thao tác mới sau hoàn tác.** Không còn làm lại được.

**Bẫy 4 — Thứ tự kiểm tra.** Sửa dòng: kiểm tra số dòng trước, nội dung sau; văn bản rỗng báo `Văn bản chưa có dòng nào`.

**Bẫy 5 — Nhập sai.** Nội dung trống hoặc dài hơn 80 ký tự; số dòng ngoài khoảng; menu sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Phân tích `SlowEditor`: mỗi thao tác chép bao nhiêu phần tử, bộ nhớ giữ sau m thao tác trên văn bản n dòng; tổng cho `workload(n)`; Big-O.
- Thiết kế `FastEditor`: mỗi thao tác cần nhớ gì để hoàn tác được (vẽ hai ngăn xếp sau các thao tác mẫu); Big-O; bảng số đo chức năng 7 trên máy bạn.

**(3) Nghiên cứu mở rộng (mục cuối `PHAN_TICH.md`, được hỏi AI, phải ghi nguồn)**

- Tìm hiểu hai cách thiết kế hoàn tác hay gặp: lưu trạng thái (Memento) và lưu thao tác (Command); ưu, nhược mỗi cách; trình soạn văn bản thật thường kết hợp thế nào.
- Tạo `nghien_cuu.py`: đo bộ nhớ đỉnh (`tracemalloc`) của `workload` trên hai lớp với n = 1.000 và 2.000; nhận xét bộ nhớ tăng theo n thế nào.

**(2) Triển khai code**

- Viết các hàm trong `soan_van_ban.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session10_TH09`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-10-thuc-hanh-cli/bai-09 rồi chép các tệp vào kho: `soan_van_ban.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`, `nghien_cuu.py (tự tạo)`.
2. Mức AI: AI-0 cho phân tích và mã; AI-1 cho nghiên cứu mở rộng (ghi nguồn, tự kiểm chứng).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
