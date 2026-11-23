# Hệ thống quản lý kho sách của nhà sách Fahasa

### 1. Bối cảnh & Vấn đề

![Nhân viên Fahasa nhập và bán sách trên màn hình dòng lệnh](minh_hoa.png)

*Nhân viên Fahasa nhập và bán sách trên màn hình dòng lệnh*

Nhà sách **Fahasa** chi nhánh Nguyễn Huệ quản lý kho bằng một danh sách; mỗi đầu sách là một list con theo thứ tự cố định:

```plaintext
[mã sách, tên sách, số cuốn tồn, giá bán (đồng)]
```

Hằng ngày nhân viên nhập sách từ nhà phát hành (đầu sách đã có thì **cộng dồn**, không tạo dòng mới), bán sách tại quầy và xem các đầu sách tồn nhiều nhất để đưa ra kệ khuyến mãi. Cuối tháng, kế toán đối chiếu tổng giá trị tồn kho; tính sai hoặc bán quá số tồn đều làm lệch sổ.

Bạn xây dựng module **"Fahasa Stock CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu ban đầu (hàm `make_books()` có sẵn trả về bản sao):

```python
SAMPLE_BOOKS = [
    ["FB001", "Đắc Nhân Tâm", 12, 86000],
    ["FB002", "Nhà Giả Kim", 25, 79000],
    ["FB003", "Tuổi Trẻ Đáng Giá Bao Nhiêu", 8, 90000],
    ["FB004", "Cây Cam Ngọt Của Tôi", 25, 108000],
    ["FB005", "Mắt Biếc", 4, 110000],
]
```

**Chức năng 1 — Xem kho sách.** Mỗi đầu sách một dòng có số thứ tự, rồi dòng `Tổng: <a> đầu sách, <b> cuốn, trị giá <c>`.

**Chức năng 2 — Nhập sách.** Nhập mã. Mã đã có: in tên và số tồn, hỏi số lượng nhập thêm, cộng dồn. Mã mới: hỏi tên, giá bán, số lượng rồi thêm vào cuối kho.

**Chức năng 3 — Bán sách.** Nhập mã và số lượng bán; trừ tồn và in số cuốn còn lại.

**Chức năng 4 — Top 3 sách tồn nhiều nhất.** Nhiều trước; tồn bằng nhau thì giữ thứ tự trong kho. **Thứ tự của kho không được thay đổi** sau khi xem top.

**Chức năng 5 — Thoát.** In `Đã đóng sổ kho. Hẹn gặp lại!`.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== FAHASA NGUYỄN HUỆ - QUẢN LÝ KHO SÁCH =====
1. Xem kho sách
2. Nhập sách
3. Bán sách
4. Top 3 sách tồn nhiều nhất
5. Thoát
Chọn chức năng (1-5): 4
Top 3 sách tồn nhiều nhất:
1. FB002 | Nhà Giả Kim | tồn 25 | 79.000đ
2. FB004 | Cây Cam Ngọt Của Tôi | tồn 25 | 108.000đ
3. FB001 | Đắc Nhân Tâm | tồn 12 | 86.000đ

[menu chính]
Chọn chức năng (1-5): 2
Mã sách: fb005
Mã đã có: Mắt Biếc (tồn 4).
Số lượng nhập thêm: 6
Đã cộng thêm sách. Tồn mới: 10.

[menu chính]
Chọn chức năng (1-5): 2
Mã sách: FB006
Tên sách: Hai Số Phận
Giá bán (đồng): 135000
Số lượng nhập: 20
Đã thêm sách mới FB006. Kho có 6 đầu sách.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Số lượng, giá bán sai.** `0`, `-2`, `2.5`, `abc`, bỏ trống: in `Lỗi: Số lượng phải là số nguyên dương` (hoặc `Giá bán phải là số nguyên dương`), kho giữ nguyên.

**Bẫy 2 — Bán sai.** Mã không có: `Lỗi: Mã sách <MÃ> không có trong kho`. Bán quá tồn: `Lỗi: Không đủ sách: còn <n> cuốn`, tồn giữ nguyên. Bán đúng bằng số tồn thì còn 0 cuốn.

**Bẫy 3 — Thêm sách mới thiếu thông tin.** Mã trống, mã đã có, tên trống: đúng thông báo trong docstring của `add_book`.

**Bẫy 4 — Lựa chọn menu không hợp lệ.** In `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.` và hỏi lại.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Giải thích vì sao top 3 không được sắp xếp thẳng trên danh sách kho; cách của bạn tốn thêm bao nhiêu bộ nhớ phụ theo n (số đầu sách).
- Big-O thời gian của bốn chức năng theo n.

**(2) Triển khai code**

- Viết các hàm trong `kho_sach.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session02_TH02`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-02-thuc-hanh-cli/bai-02 rồi chép các tệp vào kho: `kho_sach.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
