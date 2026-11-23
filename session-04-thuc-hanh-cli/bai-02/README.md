# Hệ thống tính tiết kiệm tích lũy của Techcombank

### 1. Bối cảnh & Vấn đề

![Giao dịch viên Techcombank tư vấn gói tiết kiệm tích lũy](minh_hoa.png)

*Giao dịch viên Techcombank tư vấn gói tiết kiệm tích lũy*

Tại quầy **Techcombank**, giao dịch viên tư vấn gói **tiết kiệm tích lũy**: tiền lãi mỗi tháng được nhập vào gốc, tháng sau tính lãi trên số dư mới. Quy tắc tính (số nguyên, đồng):

```plaintext
lãi một tháng = số dư * lãi suất (điểm cơ bản) // 120000      ví dụ 6,5%/năm là 650 điểm cơ bản
```

Khách thường hỏi ba câu: sau n tháng tôi có bao nhiêu, bao lâu thì đạt số tiền mục tiêu, và cuối mỗi năm số dư là bao nhiêu. Mỗi câu trả lời có cấu trúc lặp lại theo tháng, nên nhóm phát triển yêu cầu viết bằng **đệ quy** (không vòng lặp). Bản thử đầu tiên bị treo khi khách nhập lãi suất 0%: hàm "số tháng đạt mục tiêu" gọi lại chính nó mãi mà không tiến về trường hợp cơ sở.

Bạn xây dựng module **"Techcombank Savings CLI"**.

### 2. Yêu cầu nghiệp vụ

**Chức năng 1 — Nhập tiền gửi và lãi suất** (hàm `parse_money`, `parse_rate` có sẵn). Chức năng 2–4 dùng thông tin này; chưa nhập thì in `Chưa nhập tiền gửi và lãi suất (chức năng 1).`

**Chức năng 2 — Số dư sau n tháng** (1–600): `balance_after`.

**Chức năng 3 — Số tháng để đạt mục tiêu:** `months_to_reach`; in `Cần <k> tháng để đạt <tiền>.`

**Chức năng 4 — Bảng số dư cuối mỗi năm** (1–50 năm): `yearly_table`, mỗi năm một dòng `Năm <i>: <tiền>`.

**Chức năng 5 — Thoát.**

Ba hàm `balance_after`, `months_to_reach`, `yearly_table` viết bằng đệ quy, không vòng lặp.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== TECHCOMBANK - TIẾT KIỆM TÍCH LŨY =====
1. Nhập tiền gửi và lãi suất
2. Số dư sau n tháng
3. Số tháng để đạt mục tiêu
4. Bảng số dư cuối mỗi năm
5. Thoát
Chọn chức năng (1-5): 2
Chưa nhập tiền gửi và lãi suất (chức năng 1).

[menu chính]
Chọn chức năng (1-5): 1
Tiền gửi (đồng): 100000000
Lãi suất (%/năm): 6,5
Đã lưu: gửi 100.000.000đ, lãi 6.50%/năm.

[menu chính]
Chọn chức năng (1-5): 2
Số tháng: 12
Sau 12 tháng: 106.697.178đ

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Không bao giờ đạt mục tiêu.** Lãi một tháng bằng 0 (lãi suất 0%, hoặc số dư quá nhỏ so với lãi suất): báo `Số dư không tăng, không bao giờ đạt mục tiêu` **ngay**, không được đệ quy vô hạn.

**Bẫy 2 — Cần quá nhiều tháng.** Mục tiêu cần hơn 600 tháng: báo `Cần hơn 600 tháng để đạt mục tiêu`, không được để lỗi `RecursionError`.

**Bẫy 3 — Đã đạt mục tiêu, 0 tháng.** Mục tiêu không lớn hơn tiền gửi: 0 tháng.

**Bẫy 4 — Nhập sai.** Tiền, lãi suất, số tháng, số năm, menu sai: in `Lỗi: <thông báo>` đúng như trong mã có sẵn và docstring, rồi quay lại menu.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Với mỗi hàm đệ quy: trường hợp cơ sở, bước đệ quy, vì sao chắc chắn dừng (kể cả khi lãi bằng 0).
- `months_to_reach` cần tối đa bao nhiêu tầng gọi? Vì sao giới hạn 600 tháng giúp tránh `RecursionError`?

**(2) Triển khai code**

- Viết các hàm trong `tiet_kiem.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session04_TH02`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-04-thuc-hanh-cli/bai-02 rồi chép các tệp vào kho: `tiet_kiem.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
