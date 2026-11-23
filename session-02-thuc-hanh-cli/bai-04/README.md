# Hệ thống bảng doanh số nhân viên của Thế Giới Di Động

### 1. Bối cảnh & Vấn đề

![Cửa hàng trưởng TGDĐ xem bảng doanh số tháng](minh_hoa.png)

*Cửa hàng trưởng TGDĐ xem bảng doanh số tháng*

Cửa hàng **Thế Giới Di Động** Quận 7 theo dõi doanh số tháng của nhân viên bán hàng; mỗi nhân viên là một list con:

```plaintext
[mã nhân viên, họ tên, doanh số tháng (triệu đồng)]
```

Cửa hàng trưởng xem bảng theo thứ tự nhập hoặc theo xếp hạng, cộng doanh số khi có đơn mới, xóa nhân viên nghỉ việc, tìm người cao nhất và thấp nhất để khen thưởng, nhắc nhở, và thống kê số người đạt KPI. Bảng gốc dùng để chấm công nên **thứ tự trong bảng không được thay đổi** khi xem xếp hạng. Chuỗi cửa hàng có hàng trăm nghìn nhân viên, nên phần cao nhất, thấp nhất phải làm trong **một lượt duyệt**, không sắp xếp.

Bạn xây dựng module **"TGDĐ Sales Board CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_staff()` trả về bản sao của 5 nhân viên `NV01` đến `NV05` (xem `doanh_so.py`).

**Chức năng 1 — Xem bảng** (menu phụ): `1` theo thứ tự trong bảng; `2` xếp hạng doanh số giảm dần, bằng nhau giữ thứ tự trong bảng.

**Chức năng 2 — Cập nhật nhân viên** (menu phụ): `1` cộng doanh số đơn mới cho một mã; `2` xóa nhân viên nghỉ việc.

**Chức năng 3 — Cao nhất và thấp nhất.** In hai dòng `Cao nhất: ...`, `Thấp nhất: ...`; bằng nhau lấy người đứng trước.

**Chức năng 4 — Thống kê** (menu phụ): `1` số nhân viên có doanh số **lớn hơn hoặc bằng** ngưỡng KPI nhập vào; `2` doanh số trung bình, một chữ số thập phân, dấu phẩy (`104,0 triệu`).

**Chức năng 5 — Thoát.** In `Đã chốt bảng doanh số. Tạm biệt!`.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== TGDĐ QUẬN 7 - DOANH SỐ THÁNG =====
1. Xem bảng doanh số
2. Cập nhật nhân viên
3. Cao nhất và thấp nhất
4. Thống kê
5. Thoát
Chọn chức năng (1-5): 1
1. Theo thứ tự trong bảng  2. Xếp hạng doanh số
Chọn cách xem: 2
1. NV03 | Lê Phong | 150 triệu
2. NV01 | Nguyễn Hải | 120 triệu
3. NV02 | Trần Mai | 95 triệu
4. NV04 | Phạm Quỳnh | 95 triệu
5. NV05 | Đỗ Khoa | 60 triệu

[menu chính]
Chọn chức năng (1-5): 3
Cao nhất: NV03 | Lê Phong | 150 triệu
Thấp nhất: NV05 | Đỗ Khoa | 60 triệu

[menu chính]
Chọn chức năng (1-5): 4
1. Số nhân viên đạt KPI  2. Doanh số trung bình
Chọn thống kê: 1
Ngưỡng KPI (triệu): 100
Đạt KPI 100 triệu: 2/5 nhân viên.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Doanh số bằng nhau.** Xếp hạng giữ thứ tự trong bảng (`NV02` trước `NV04`); cao nhất, thấp nhất lấy người đứng trước.

**Bẫy 2 — Mã không có, số sai.** `Lỗi: Không có nhân viên <MÃ>`; doanh số, ngưỡng KPI không phải số nguyên dương: đúng thông báo trong docstring; bảng giữ nguyên.

**Bẫy 3 — Bảng rỗng.** Xóa hết nhân viên rồi chọn chức năng 1, 3, 4: in `Chưa có nhân viên nào.`, không chia cho 0.

**Bẫy 4 — Menu sai.** Menu phụ: `Lựa chọn không hợp lệ.`; menu chính: `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.`

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Xếp hạng: so sánh `sort()` và `sorted()` (thứ tự bảng gốc, bộ nhớ phụ). Bạn chọn cách nào, vì sao?
- Cao nhất và thấp nhất trong một lượt: Big-O thời gian, bộ nhớ phụ; so với cách sắp xếp rồi lấy đầu, cuối.

**(2) Triển khai code**

- Viết các hàm trong `doanh_so.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session02_TH04`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-02-thuc-hanh-cli/bai-04 rồi chép các tệp vào kho: `doanh_so.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
