# Hệ thống đối soát giao dịch cuối ngày của VNPAY

### 1. Bối cảnh & Vấn đề

![Nhân viên đối soát VNPAY so khớp hai sổ giao dịch](minh_hoa.png)

*Nhân viên đối soát VNPAY so khớp hai sổ giao dịch*

Cuối mỗi ngày, cổng thanh toán **VNPAY** phải **đối soát** sổ giao dịch của hệ thống với sao kê ngân hàng gửi về. Mỗi giao dịch là `[mã giao dịch, số tiền]`; trong mỗi sổ mã không trùng nhau, nhưng hai sổ ghi theo thứ tự khác nhau. Cần tìm ba loại sai lệch: giao dịch **chỉ có ở hệ thống**, **chỉ có ở ngân hàng**, và giao dịch có ở cả hai nhưng **lệch số tiền**.

Bản đang chạy so từng giao dịch với cả sổ bên kia: đủ nhanh với vài nghìn giao dịch, nhưng ngày sale có hơn 100.000 giao dịch và quy trình đối soát kéo dài quá giờ chốt sổ. Trưởng nhóm yêu cầu một giải pháp khác, chứng minh bằng số đo và phân tích.

Bạn xây dựng module **"VNPAY Reconciliation CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_books()` trả về bản sao hai sổ, mỗi sổ 5 giao dịch (xem `doi_soat.py`).

**Chức năng 1 — Xem tóm tắt hai sổ.** Mỗi sổ một dòng: số giao dịch và tổng tiền.

**Chức năng 2 — Thêm giao dịch** (menu phụ chọn sổ): nhập mã (`VP` + từ 4 chữ số) và số tiền.

**Chức năng 3 — Đối soát** (menu phụ chọn giải pháp). In ba dòng nhóm, mã xếp tăng dần; nhóm rỗng in `(không có)`. Hai hàm `reconcile_v1`, `reconcile_v2` trả về **cùng kết quả** nhưng **khác nhau về cách làm**; giải pháp 2 phải xử lý 100.000 giao dịch trong 2 giây. Không làm đổi hai sổ.

**Chức năng 4 — Đo so sánh hai giải pháp.** `benchmark` đo bằng `timeit` trên hai sổ giả lập (`make_big_books`, có sẵn) với n = 1.000, 2.000, 4.000; in bảng thời gian và tỉ lệ so với n trước đó.

**Chức năng 5 — Thoát.** In `Đã lưu biên bản đối soát. Tạm biệt!`.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== VNPAY - ĐỐI SOÁT CUỐI NGÀY =====
1. Xem tóm tắt hai sổ
2. Thêm giao dịch
3. Đối soát
4. Đo so sánh hai giải pháp
5. Thoát
Chọn chức năng (1-5): 1
Hệ thống: 5 giao dịch, tổng 4.299.000đ
Ngân hàng: 5 giao dịch, tổng 3.793.000đ

[menu chính]
Chọn chức năng (1-5): 3
1. Giải pháp 1  2. Giải pháp 2
Chọn giải pháp: 1
Chỉ có ở hệ thống: VP1005
Chỉ có ở ngân hàng: VP1004
Lệch số tiền: VP1003 hệ thống 89.000đ, ngân hàng 98.000đ

[menu chính]
Chọn chức năng (1-5): 3
1. Giải pháp 1  2. Giải pháp 2
Chọn giải pháp: 2
Chỉ có ở hệ thống: VP1005
Chỉ có ở ngân hàng: VP1004
Lệch số tiền: VP1003 hệ thống 89.000đ, ngân hàng 98.000đ

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in bảng dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | giải pháp 1 (ms) | giải pháp 2 (ms)
1000 | 19.6 | 0.5
2000 | 78.3 (x4.0) | 1.2 (x2.2)
4000 | 313.8 (x4.0) | 2.4 (x2.0)
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Hai sổ khác thứ tự.** Cùng một giao dịch có thể nằm ở vị trí bất kỳ trong sổ kia.

**Bẫy 2 — Sổ rỗng.** Một hoặc cả hai sổ rỗng: mọi giao dịch của sổ còn lại thuộc nhóm "chỉ có ở".

**Bẫy 3 — Thêm giao dịch sai.** Mã sai dạng, mã đã có trong sổ đó, số tiền không phải số nguyên dương: đúng thông báo trong docstring của `add_tx`.

**Bẫy 4 — Không làm đổi sổ.** Đối soát xong, thứ tự hai sổ giữ nguyên (sổ dùng cho kiểm toán).

**Bẫy 5 — Menu sai.** Menu phụ: `Lựa chọn không hợp lệ.`; menu chính: `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.`

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Đề xuất ít nhất hai giải pháp đối soát khác nhau: ý tưởng, hình minh họa trên dữ liệu mẫu, mã giả.
- Bảng so sánh 5 tiêu chí (tốc độ, bộ nhớ phụ, độ dễ đọc, dễ bảo trì, phù hợp bối cảnh) kèm Big-O và số đo của chức năng 4 trên máy bạn; chọn giải pháp cho ngày sale và giải thích.

**(2) Triển khai code**

- Viết các hàm trong `doi_soat.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 8 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session02_TH07`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-02-thuc-hanh-cli/bai-07 rồi chép các tệp vào kho: `doi_soat.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
