# Tối ưu báo cáo cuối ca của The Coffee House

### 1. Bối cảnh & Vấn đề

![Quản lý cửa hàng The Coffee House chờ báo cáo cuối ca](minh_hoa.png)

*Quản lý cửa hàng The Coffee House chờ báo cáo cuối ca*

Cửa hàng **The Coffee House** Hồ Con Rùa ghi mỗi đơn thành `[mã đơn, tên món, số ly]`, xếp theo thời gian. Cuối ca, quản lý xem **báo cáo**: tổng số ly, số món khác nhau, món bán nhiều ly nhất và 3 đơn gần nhất.

Hàm `report_slow` (có sẵn, **không được sửa**) là bản đang chạy: kết quả đúng, nhưng các cửa hàng lớn với hàng chục nghìn đơn mỗi ngày phải chờ báo cáo rất lâu. Đọc kỹ bản cũ, bạn sẽ thấy nó dùng nhiều thao tác list tốn kém đã học ở Session 01.

Bạn viết `report_fast` cho **kết quả giống hệt** bản cũ, đưa vào ứng dụng sổ đơn, và chứng minh bằng số đo; sau đó tìm hiểu cách đo thời gian cho đáng tin.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_orders()` trả về bản sao 6 đơn; thực đơn `DRINKS` có 5 món (xem `bao_cao_ca.py`).

**Chức năng 1 — Ghi đơn mới.** In thực đơn đánh số 1-5, hỏi số thứ tự món và số ly (1-20); mã tự sinh tiếp theo (`TCH0007`).

**Chức năng 2 — Báo cáo cuối ca** dùng `report_fast` với top = 3: `Tổng: <a> ly, <b> món.`, `Bán chạy nhất: <món> (<k> ly).`, `3 đơn gần nhất: <mã>, ...`.

**Chức năng 3 — Tra cứu đơn** theo mã.

**Chức năng 4 — Đo so sánh bản cũ và bản mới** với n = 5.000, 10.000, 20.000 (sổ giả lập `make_big_orders`, có sẵn).

**Chức năng 5 — Thoát.** In `Đã chốt ca. Hẹn gặp lại!`.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== THE COFFEE HOUSE HỒ CON RÙA - SỔ ĐƠN =====
1. Ghi đơn mới
2. Báo cáo cuối ca
3. Tra cứu đơn
4. Đo so sánh bản cũ và bản mới
5. Thoát
Chọn chức năng (1-5): 2
Tổng: 11 ly, 4 món.
Bán chạy nhất: Trà đào cam sả (4 ly).
3 đơn gần nhất: TCH0006, TCH0005, TCH0004

[menu chính]
Chọn chức năng (1-5): 1
1. Cà phê sữa đá
2. Trà đào cam sả
3. Bạc xỉu
4. Trà sữa oolong
5. Cold brew
Chọn món: 2
Số ly: 2
Đã ghi TCH0007: 2 ly Trà đào cam sả.

[menu chính]
Chọn chức năng (1-5): 1
1. Cà phê sữa đá
2. Trà đào cam sả
3. Bạc xỉu
4. Trà sữa oolong
5. Cold brew
Chọn món: 6
Số ly: 1
Lỗi: Món phải là số từ 1 đến 5

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in bảng dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | bản cũ (ms) | bản mới (ms)
5000 | 8.1 | 1.8
10000 | 23.2 (x2.9) | 3.7 (x2.0)
20000 | 84.6 (x3.6) | 7.6 (x2.1)
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ.** Kiểm tra so sánh hai bản trên 200 sổ ngẫu nhiên; món bằng số ly lấy món xuất hiện trước.

**Bẫy 2 — top ở biên.** `top = 0`, top lớn hơn số đơn, sổ rỗng (`(0, 0, None, 0, [])`; chức năng 2 in `Ca này chưa có đơn nào.`).

**Bẫy 3 — Ràng buộc.** `report_fast` không gọi `report_slow`, không dùng `insert(0, ...)`, `pop(0)`, nối list bằng `+` trong vòng lặp, `dict`, `set`; không làm đổi sổ.

**Bẫy 4 — 200.000 đơn trong 2 giây.** Đừng thử bản cũ với 200.000 đơn: nó chạy rất lâu.

**Bẫy 5 — Nhập sai.** Món ngoài 1-5, số ly ngoài 1-20: đúng thông báo trong docstring của `add_order`; menu chính sai: `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.`

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Bảng các đoạn của `report_slow`: việc làm, thao tác list, số bước theo n (số đơn) và d (số món), Big-O. Đoạn nào làm bản cũ chậm nhất khi n lớn?
- Thiết kế `report_fast`: mỗi đoạn thay bằng gì; Big-O hai bản; bảng số đo chức năng 4 trên máy bạn.

**(3) Nghiên cứu mở rộng (mục cuối `PHAN_TICH.md`, được hỏi AI, phải ghi nguồn)**

- Tìm hiểu cách đo thời gian đáng tin trong Python: `time.perf_counter`, `timeit.repeat`, vì sao lấy giá trị nhỏ nhất hoặc trung vị thay vì một lần đo.
- Tạo `nghien_cuu.py`: đo `report_fast` trên 50.000 đơn bằng 20 lần `perf_counter` riêng lẻ (in nhỏ nhất, lớn nhất, trung vị) và bằng `timeit.repeat(repeat=5, number=10)`; giải thích vì sao các lần đo chênh nhau.

**(2) Triển khai code**

- Viết các hàm trong `bao_cao_ca.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 8 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session02_TH09`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-02-thuc-hanh-cli/bai-09 rồi chép các tệp vào kho: `bao_cao_ca.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`, `nghien_cuu.py (tự tạo)`.
2. Mức AI: AI-0 cho phân tích và mã; AI-1 cho nghiên cứu mở rộng (ghi nguồn, tự kiểm chứng).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
