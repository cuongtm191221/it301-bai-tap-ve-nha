# Hệ thống quầy thuốc dùng mảng động của Nhà thuốc Long Châu

### 1. Bối cảnh & Vấn đề

![Dược sĩ Long Châu nhập thuốc lên quầy](minh_hoa.png)

*Dược sĩ Long Châu nhập thuốc lên quầy*

Ở **Nhà thuốc Long Châu**, phần mềm quầy giữ danh sách thuốc đang bày bán, mỗi thuốc là `[mã thuốc, tên, số hộp]`. Nhóm phát triển muốn hiểu rõ chi phí của danh sách, nên tự cài lớp **`DrugArray`** theo mô hình mảng động của Session 05: vùng lưu trữ `_data = [None] * capacity` có số ô cố định, capacity ban đầu 1, **đầy thì tạo vùng gấp đôi và chép sang**; bộ đếm `copies` ghi số phần tử đã chép, `checks` ghi số lần so sánh mã khi tìm.

Dược sĩ cần xem quầy (kèm số ô đang dùng), nhập thuốc (mã đã có thì **cộng dồn** số hộp), tra cứu theo mã và bán thuốc.

Bạn xây dựng module **"Long Chau Counter CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_shelf()` trả về quầy có 3 thuốc `LC101`, `LC102`, `LC103` (xem `quay_thuoc.py`; `size`, `capacity`, `get` có sẵn).

**Chức năng 1 — Xem quầy thuốc.** Mỗi thuốc một dòng, rồi `Đang lưu <size>/<capacity> ô, đã chép <copies> lần`.

**Chức năng 2 — Nhập thuốc.** Nhập mã, tên, số hộp; mã đã có thì cộng số hộp (`Đã cộng thêm <mã>: còn <n> hộp.`), mã mới thì thêm vào cuối (`Đã thêm mới ...`).

**Chức năng 3 — Tra cứu thuốc.** In `Vị trí <i>: <tên>, còn <n> hộp (so sánh <k> mã).` hoặc `Không có thuốc này (so sánh <k> mã).`

**Chức năng 4 — Bán thuốc.** Không bán quá số hộp đang có. **Chức năng 5 — Thoát.**

Trong `DrugArray`, bạn viết `append` (kèm hàm phụ đổi vùng lưu trữ), `find`, `items`. Vùng lưu trữ chỉ được đọc, gán theo chỉ số: **không** dùng `append`, `insert` trên `_data`.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== NHÀ THUỐC LONG CHÂU - QUẦY THUỐC =====
1. Xem quầy thuốc
2. Nhập thuốc
3. Tra cứu thuốc
4. Bán thuốc
5. Thoát
Chọn chức năng (1-5): 1
1. LC101 | Panadol Extra | 24 hộp
2. LC102 | Berberin | 15 hộp
3. LC103 | Vitamin C 500mg | 40 hộp
Đang lưu 3/4 ô, đã chép 0 lần

[menu chính]
Chọn chức năng (1-5): 2
Mã thuốc: LC104
Tên thuốc: Men vi sinh Biolactyl
Số hộp: 30
Đã thêm mới LC104: còn 30 hộp.

[menu chính]
Chọn chức năng (1-5): 2
Mã thuốc: lc102
Tên thuốc: 
Số hộp: 10
Đã cộng thêm LC102: còn 25 hộp.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Ô trống không phải thuốc.** Quầy 5 thuốc có 8 ô; `items()` chỉ trả 5 thuốc.

**Bẫy 2 — Gấp đôi đúng lúc.** Sau 9 lần thêm: capacity 16, `copies` là 1 + 2 + 4 + 8 = 15.

**Bẫy 3 — Dữ liệu sai.** Mã sai dạng, số hộp không phải số nguyên dương, tên trống (với mã mới), mã không có khi bán, bán quá số hộp: đúng thông báo trong docstring; quầy giữ nguyên.

**Bẫy 4 — Menu sai.** `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.`

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Bảng `size`, `capacity`, `copies` sau mỗi lần thêm, từ 1 đến 9 thuốc; tổng số lần chép khi thêm n thuốc khoảng bao nhiêu, vì sao thêm vào cuối vẫn nhanh tính trung bình.
- Số lần so sánh của `find` khi mã ở đầu, ở cuối, không có; Big-O của `append` (trường hợp đổi vùng và không đổi vùng), `find`, `items`.

**(2) Triển khai code**

- Viết các hàm trong `quay_thuoc.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session06_TH01`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-06-thuc-hanh-cli/bai-01 rồi chép các tệp vào kho: `quay_thuoc.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
