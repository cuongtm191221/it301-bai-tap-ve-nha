# Tối ưu báo cáo ca trụ bơm xăng Petrolimex

### 1. Bối cảnh & Vấn đề

![Trưởng ca Petrolimex chờ báo cáo cuối ca](minh_hoa.png)

*Trưởng ca Petrolimex chờ báo cáo cuối ca*

Mỗi trụ bơm của **Petrolimex** ghi **nhật ký bơm** bằng danh sách liên kết đơn: mỗi lần bơm có mã `Bxxxxx`, loại nhiên liệu (`RON95`, `E5`, `DO`) và số lít (lưu bằng decilít). Cuối ca, trưởng ca in **báo cáo**: tổng lít từng loại, lần bơm nhiều nhất, các lần bơm từ một ngưỡng trở lên (để đối chiếu hóa đơn).

Hàm `report_slow` trong `nhat_ky_bom.py` cho kết quả đúng nhưng trạm cao tốc có hàng chục nghìn lần bơm mỗi ca, báo cáo chạy rất lâu. Người viết bản cũ quen làm với list nên duyệt nhật ký "theo chỉ số". Cần **viết lại** thành `report_fast` cho **đúng y hệt** kết quả cũ và giải thích vì sao bản cũ chậm.

Bạn xây dựng module **"Petrolimex Shift Report CLI"**.

### 2. Yêu cầu nghiệp vụ

Nhật ký mẫu: `make_log()` có 6 lần bơm. Lớp `PumpLog`, các hàm `liters_text`, `parse_liters`, `report_slow` có sẵn, **không sửa**.

**Chức năng 1 — Xem nhật ký bơm.** **Chức năng 2 — Ghi lần bơm** (nhiên liệu, số lít). **Chức năng 3 — Báo cáo ca** bằng `report_fast` với ngưỡng người dùng nhập.

**Chức năng 4 — Đo** bản cũ và bản mới với n = 500, 1.000, 2.000. **Chức năng 5 — Thoát.**

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== PETROLIMEX - BÁO CÁO CA TRỤ BƠM =====
1. Xem nhật ký bơm
2. Ghi lần bơm
3. Báo cáo ca
4. Đo bản cũ và bản mới
5. Thoát
Chọn chức năng (1-5): 1
B00001 | RON95 | 35.5 lít
B00002 | DO | 120.0 lít
B00003 | E5 | 18.2 lít
B00004 | RON95 | 50.0 lít
B00005 | DO | 120.0 lít
B00006 | E5 | 7.5 lít

[menu chính]
Chọn chức năng (1-5): 3
Ngưỡng (lít): 50
RON95: 85.5 lít | E5: 25.7 lít | DO: 240.0 lít
Lần bơm nhiều nhất: B00002
Từ 50.0 lít trở lên: B00002, B00004, B00005

[menu chính]
Chọn chức năng (1-5): 2
Nhiên liệu (RON95, E5, DO): ron95
Số lít: 42,7
Đã ghi B00007: RON95 42.7 lít.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | bản cũ (ms) | bản mới (ms)
500 | 2.3 | 0.0
1000 | 8.1 | 0.1
2000 | 32.2 | 0.2
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ.** Kiểm tra trên 200 nhật ký ngẫu nhiên; nhật ký rỗng ra `((0, 0, 0), None, [])`; tổng là tuple.

**Bẫy 2 — Bằng nhau.** `B00002`, `B00005` cùng 120 lít: lấy lần đầu; ngưỡng tính cả lần bơm đúng bằng ngưỡng.

**Bẫy 3 — Ràng buộc.** Không gọi bản cũ, `get`, `count`; không làm đổi nhật ký; 200.000 lần bơm trong 1 giây.

**Bẫy 4 — Nhập sai.** Nhiên liệu ngoài ba loại (gõ thường hợp lệ); số lít ngoài 0,1–200, quá 1 chữ số thập phân (`12,5` và `12.5` đều hợp lệ); menu sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Phân tích `report_slow`: mỗi lần `log.get(i)`, `log.count()`, ghép tuple và `over + [code]` đi qua hoặc chép bao nhiêu phần tử; tổng theo n; Big-O thời gian và bộ nhớ phụ.
- Thiết kế `report_fast`; Big-O; bảng số đo chức năng 4 trên máy bạn (n gấp đôi thì mỗi cột tăng mấy lần).

**(3) Nghiên cứu mở rộng (mục cuối `PHAN_TICH.md`, được hỏi AI, phải ghi nguồn)**

- Tìm hiểu `__slots__` trong lớp Python: node thường lưu thuộc tính ở đâu, `__slots__` thay đổi gì, đánh đổi là gì.
- Tạo `nghien_cuu.py`: lớp node có `__slots__` cùng thuộc tính với `Node`; in `sys.getsizeof` một node mỗi loại (node thường cộng cả `__dict__`), và bộ nhớ đỉnh `tracemalloc` khi tạo 100.000 node mỗi loại.

**(2) Triển khai code**

- Viết các hàm trong `nhat_ky_bom.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session08_TH09`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-08-thuc-hanh-cli/bai-09 rồi chép các tệp vào kho: `nhat_ky_bom.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`, `nghien_cuu.py (tự tạo)`.
2. Mức AI: AI-0 cho phân tích và mã; AI-1 cho nghiên cứu mở rộng (ghi nguồn, tự kiểm chứng).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
