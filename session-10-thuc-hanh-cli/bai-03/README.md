# Hệ thống kiểm tra mẫu in hóa đơn của Sapo

### 1. Bối cảnh & Vấn đề

![Chủ cửa hàng sửa mẫu in hóa đơn trên Sapo](minh_hoa.png)

*Chủ cửa hàng sửa mẫu in hóa đơn trên Sapo*

Chủ cửa hàng dùng **Sapo** tự soạn **mẫu in hóa đơn**, chèn biến trong ngoặc như `{ten_khach}`, `[ma_don]`, `(tong_tien)`. Mẫu sai ngoặc làm máy in in ra ký hiệu lạ hoặc bỏ trống cả hóa đơn. Phần đặt trong nháy kép `"..."` là chữ in nguyên văn: ngoặc trong đó không tính.

Bản kiểm tra cũ chỉ đếm số ngoặc mở và đóng nên để lọt `([)]`; khi báo lỗi lại không nói lỗi ở đâu. Đội kỹ thuật yêu cầu kiểm tra bằng **ngăn xếp `LinkedStack`** và báo **lỗi đầu tiên kèm vị trí**.

Bạn xây dựng module **"Sapo Print Template CLI"**.

### 2. Yêu cầu nghiệp vụ

Mẫu đang dùng: `make_templates()`. Lớp `Node`, hàm `clean` có sẵn. Vị trí đếm từ 1 theo ký tự của mẫu (sau khi bỏ khoảng trắng hai đầu).

**Chức năng 1 — Xem các mẫu in.** **Chức năng 2 — Thêm mẫu in**: chỉ thêm khi hợp lệ, không thì in thông báo lỗi.

**Chức năng 3 — Kiểm tra một mẫu** (menu phụ): chỉ báo `Hợp lệ` / `Không hợp lệ`, hoặc chi tiết lỗi. **Chức năng 4 — Thoát.**

Bốn dạng thông báo lỗi (xem docstring `check_template`): ngoặc đóng không có ngoặc mở; ngoặc đóng không khớp (kèm vị trí ngoặc mở); nháy kép chưa đóng; ngoặc chưa đóng (ngoặc mở gần cuối nhất).

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== SAPO - MẪU IN HÓA ĐƠN =====
1. Xem các mẫu in
2. Thêm mẫu in
3. Kiểm tra một mẫu
4. Thoát
Chọn chức năng (1-4): 1
1. Khách: {ten_khach} - Đơn [ma_don]
2. Tổng tiền: (tong_tien) đồng
3. Ghi chú: "(không xuất hóa đơn đỏ" {ghi_chu}

[menu chính]
Chọn chức năng (1-4): 3
1. Chỉ báo đúng/sai  2. Chi tiết lỗi
Chọn cách kiểm tra: 2
Mẫu in: Tổng: {tong_tien
Vị trí 7: dấu '{' chưa được đóng

[menu chính]
Chọn chức năng (1-4): 3
1. Chỉ báo đúng/sai  2. Chi tiết lỗi
Chọn cách kiểm tra: 2
Mẫu in: Giảm (10%]
Vị trí 10: dấu ']' không khớp với '(' ở vị trí 6

[menu chính]
Chọn chức năng (1-4): 3
1. Chỉ báo đúng/sai  2. Chi tiết lỗi
Chọn cách kiểm tra: 1
Mẫu in: Phí ship)
Không hợp lệ

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Đúng số lượng, sai thứ tự.** `([)]` không hợp lệ: lỗi ở vị trí 3.

**Bẫy 2 — Ngoặc trong nháy kép.** `"{" "}"` hợp lệ; nháy kép chưa đóng báo vị trí dấu nháy.

**Bẫy 3 — Lỗi đầu tiên.** `a)(` báo vị trí 2, không báo ngoặc `(` chưa đóng.

**Bẫy 4 — Còn nhiều ngoặc mở.** `{[(` báo ngoặc mở gần cuối nhất (vị trí 3).

**Bẫy 5 — Nhập sai.** Mẫu trống hoặc dài hơn 200 ký tự; menu phụ và menu chính sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Chạy tay `check_template` trên `Giảm (10%]` và `([)]`: nội dung ngăn xếp sau mỗi ký tự ngoặc.
- Vì sao chỉ đếm số ngoặc là không đủ; Big-O theo độ dài mẫu; bộ nhớ ngăn xếp nhiều nhất khi nào.

**(2) Triển khai code**

- Viết các hàm trong `mau_in.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 5 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session10_TH03`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-10-thuc-hanh-cli/bai-03 rồi chép các tệp vào kho: `mau_in.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
