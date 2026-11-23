# Hệ thống gợi ý combo trong ngân sách cho quán cơm tấm trên GrabFood

### 1. Bối cảnh & Vấn đề

![Chủ quán cơm tấm xem gợi ý combo trên GrabFood](minh_hoa.png)

*Chủ quán cơm tấm xem gợi ý combo trên GrabFood*

Quán **Cơm Tấm Phúc Lộc Thọ** bán trên **GrabFood** muốn có tính năng "nhập ngân sách, gợi ý combo". Thực đơn là list món `[mã, tên, giá]`; một **combo** là tập các món khác nhau (mỗi món nhiều nhất một phần), không rỗng, tổng giá không vượt ngân sách. Quán cần hai thông tin: **combo sát ngân sách nhất** để gợi ý cho khách, và **có bao nhiêu combo** trong một mức ngân sách để chọn các mức khuyến mãi (49k, 99k...).

Bản đếm hiện tại liệt kê tổng giá của mọi tập món bằng đệ quy rồi đếm: thực đơn 7 món chạy tức thì, nhưng chuỗi cửa hàng có thực đơn 40 món thì không bao giờ chạy xong. Trưởng nhóm yêu cầu một giải pháp khác (vẫn đệ quy), chứng minh bằng số đo và phân tích.

Bạn xây dựng module **"GrabFood Combo Advisor CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_menu()` trả về 7 món (xem `combo.py`).

**Chức năng 1 — Xem thực đơn.**

**Chức năng 2 — Gợi ý combo sát ngân sách.** `best_combo`: tổng giá lớn nhất không vượt ngân sách; cùng tổng thì ít món hơn, vẫn bằng thì món đứng trước trong thực đơn; in `Combo <tổng> (<k> món): <tên món>, ...` hoặc `Không có món nào vừa ngân sách.`

**Chức năng 3 — Đếm số combo trong ngân sách** (menu phụ chọn giải pháp). `count_combos_v1`, `count_combos_v2` cho **cùng kết quả**, **khác nhau về cách làm**; giải pháp 2 tính 40 món, ngân sách 200.000đ trong 1 giây; không làm đổi list giá.

**Chức năng 4 — Đo** hai giải pháp với thực đơn giả lập 16, 18, 20 món, ngân sách 150.000đ. **Chức năng 5 — Thoát.**

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== GRABFOOD - CƠM TẤM PHÚC LỘC THỌ =====
1. Xem thực đơn
2. Gợi ý combo sát ngân sách
3. Đếm số combo trong ngân sách
4. Đo so sánh hai giải pháp
5. Thoát
Chọn chức năng (1-5): 1
CT01 | Cơm tấm sườn | 55.000đ
CT02 | Cơm tấm sườn bì chả | 69.000đ
CT03 | Canh khổ qua | 25.000đ
CT04 | Trà đá | 5.000đ
CT05 | Chả trứng thêm | 15.000đ
CT06 | Nước sâm | 18.000đ
CT07 | Sườn thêm | 30.000đ

[menu chính]
Chọn chức năng (1-5): 2
Ngân sách (đồng): 100000
Combo 100.000đ (3 món): Cơm tấm sườn, Chả trứng thêm, Sườn thêm

[menu chính]
Chọn chức năng (1-5): 3
1. Giải pháp 1  2. Giải pháp 2
Chọn giải pháp: 1
Ngân sách (đồng): 100000
Có 56 combo trong 100.000đ.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
số món | giải pháp 1 (ms) | giải pháp 2 (ms)
16 | 2.9 | 0.04
18 | 11.8 | 0.05
20 | 48.6 | 0.07
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Không có combo.** Ngân sách nhỏ hơn món rẻ nhất: đếm ra 0; gợi ý in `Không có món nào vừa ngân sách.`

**Bẫy 2 — Combo rỗng không tính.** Ngân sách 5.000đ có đúng 1 combo (Trà đá).

**Bẫy 3 — Nhiều combo cùng tổng.** Theo quy tắc ít món hơn, rồi món đứng trước.

**Bẫy 4 — Thực đơn lớn.** 40 món: giải pháp 2 trong 1 giây.

**Bẫy 5 — Nhập sai.** Ngân sách ngoài 10.000–2.000.000 hoặc không phải số nguyên, menu phụ, menu chính sai: đúng thông báo của đề.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Đề xuất ít nhất hai giải pháp đếm combo khác nhau (ý tưởng, cây lời gọi với 3 món, mã giả); giải pháp 1 xét bao nhiêu tập món với n món? Giải pháp của bạn bỏ qua được những nhánh nào, vì sao vẫn đúng?
- Bảng so sánh 5 tiêu chí kèm số đo chức năng 4 trên máy bạn; chọn giải pháp và giải thích.

**(2) Triển khai code**

- Viết các hàm trong `combo.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session04_TH08`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-04-thuc-hanh-cli/bai-08 rồi chép các tệp vào kho: `combo.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
