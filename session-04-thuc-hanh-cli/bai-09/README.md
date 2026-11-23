# Tối ưu thưởng chuỗi ngày mua hàng của Bách Hóa Xanh

### 1. Bối cảnh & Vấn đề

![Khách thân thiết Bách Hóa Xanh xem điểm thưởng chuỗi ngày mua](minh_hoa.png)

*Khách thân thiết Bách Hóa Xanh xem điểm thưởng chuỗi ngày mua*

**Bách Hóa Xanh** thưởng khách đi chợ đều đặn: lịch sử là list các ngày mua (số thứ tự ngày, tăng dần, không trùng). Các ngày liên tiếp tạo thành **chuỗi**; mỗi ngày mua được điểm bằng độ dài chuỗi tính đến ngày đó, **tối đa 7 điểm**. Ví dụ mua ngày 1, 2, 3, 5: điểm 1 + 2 + 3 + 1.

Hàm `report_slow` (có sẵn, **không được sửa**) viết bằng đệ quy, cắt list ở mỗi tầng: đúng với khách mới, nhưng khách thân thiết 5 năm (hơn 1.800 ngày mua) làm ứng dụng báo `RecursionError`, và lịch sử vài trăm ngày đã chậm thấy rõ.

Bạn viết `report_fast` cho **kết quả giống hệt** bản cũ, đưa vào ứng dụng, chứng minh bằng số đo, rồi tìm hiểu vì sao Python không tự xử lý được đệ quy sâu.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_days()` trả về 9 ngày mua trong tháng 11/2026 (xem `chuoi_ngay.py`).

**Chức năng 1 — Xem k ngày mua gần nhất** (mới nhất trước, dạng `YYYY-MM-DD`).

**Chức năng 2 — Ghi ngày mua** (`YYYY-MM-DD`, phải sau ngày mua gần nhất); in chuỗi hiện tại.

**Chức năng 3 — Báo cáo** bằng `report_fast`: `Chuỗi dài nhất: <a> ngày | Chuỗi hiện tại: <b> ngày | Điểm thưởng: <c>`.

**Chức năng 4 — Đo** bản cũ và bản mới với n = 200, 400, 800, và cho biết bản cũ với 3.000 ngày có gặp `RecursionError` không. **Chức năng 5 — Thoát.**

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== BÁCH HÓA XANH - THƯỞNG CHUỖI NGÀY MUA =====
1. Xem các ngày mua gần nhất
2. Ghi ngày mua
3. Báo cáo chuỗi và điểm thưởng
4. Đo bản cũ và bản mới
5. Thoát
Chọn chức năng (1-5): 3
Chuỗi dài nhất: 4 ngày | Chuỗi hiện tại: 4 ngày | Điểm thưởng: 19

[menu chính]
Chọn chức năng (1-5): 1
Số ngày cần xem: 3
2026-11-13, 2026-11-12, 2026-11-11

[menu chính]
Chọn chức năng (1-5): 2
Ngày mua (YYYY-MM-DD): 2026-11-14
Đã ghi 2026-11-14. Chuỗi hiện tại: 5 ngày.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | bản cũ (ms) | bản mới (ms)
200 | 0.27 | 0.031
400 | 0.85 | 0.062
800 | 3.01 | 0.124
Bản cũ với 3000 ngày: gặp RecursionError
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ.** Kiểm tra trên 200 lịch sử ngẫu nhiên; lịch sử rỗng `(0, 0, 0)`; một ngày `(1, 1, 1)`.

**Bẫy 2 — Trần 7 điểm.** Chuỗi 10 ngày: điểm 1 + 2 + ... + 7 + 7 + 7 + 7.

**Bẫy 3 — Ràng buộc.** `report_fast` không gọi bản cũ, không đổi giới hạn đệ quy, không làm đổi lịch sử; 100.000 ngày trong 1 giây.

**Bẫy 4 — Ngày sai.** Sai dạng hoặc ngày không có thật (`2026-11-31`): `Lỗi: Ngày phải có dạng YYYY-MM-DD`; không sau ngày gần nhất: `Lỗi: Ngày mua phải sau ngày mua gần nhất (<ngày>)`.

**Bẫy 5 — Menu sai.** `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.`

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Phân tích `report_slow`: độ sâu đệ quy, số phần tử bị chép khi cắt list, Big-O thời gian và bộ nhớ theo n; vì sao gặp `RecursionError`.
- Thiết kế `report_fast`; Big-O; bảng số đo chức năng 4 trên máy bạn.

**(3) Nghiên cứu mở rộng (mục cuối `PHAN_TICH.md`, được hỏi AI, phải ghi nguồn)**

- Tìm hiểu "đệ quy đuôi" (tail recursion) và vì sao CPython không tối ưu nó; vì sao tăng `sys.setrecursionlimit` không phải cách sửa an toàn.
- Tạo `nghien_cuu.py`: viết bản đệ quy đuôi của chuỗi hiện tại (tham số tích lũy), cho thấy nó vẫn gặp `RecursionError` với 5.000 ngày; in `sys.getrecursionlimit()`; đối chiếu với `report_fast`.

**(2) Triển khai code**

- Viết các hàm trong `chuoi_ngay.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 8 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session04_TH09`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-04-thuc-hanh-cli/bai-09 rồi chép các tệp vào kho: `chuoi_ngay.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`, `nghien_cuu.py (tự tạo)`.
2. Mức AI: AI-0 cho phân tích và mã; AI-1 cho nghiên cứu mở rộng (ghi nguồn, tự kiểm chứng).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
