# Hệ thống sổ quỹ tiền mặt trong ca của Circle K

### 1. Bối cảnh & Vấn đề

![Trưởng ca Circle K đối chiếu sổ quỹ](minh_hoa.png)

*Trưởng ca Circle K đối chiếu sổ quỹ*

Cửa hàng **Circle K** Lê Lợi mở 24 giờ. Mỗi ca nhận quỹ đầu ca 2.000.000đ và ghi mọi khoản tiền mặt vào sổ quỹ, xếp theo thời gian:

```plaintext
[mã giao dịch, loại "THU" hoặc "CHI", số tiền (đồng)]
```

Trưởng ca cần xem sổ kèm **số dư sau từng giao dịch**, ghi thêm khoản thu chi, xem tổng thu chi và các khoản chi lớn nhất. Khoản chi lớn hơn số dư phải bị từ chối. Bản thử đầu tiên tính số dư từng dòng bằng cách cộng lại từ đầu sổ cho mỗi dòng; cửa hàng đông khách có hàng chục nghìn giao dịch mỗi ca và màn hình đứng hình. Quản lý vùng muốn có **số đo** thời gian và bộ nhớ khi sổ dài gấp đôi.

Bạn xây dựng module **"Circle K Cash Book CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_book()` trả về bản sao 6 giao dịch `GD001` đến `GD006`; hằng `OPENING = 2000000` (xem `so_quy.py`).

**Chức năng 1 — Xem sổ quỹ** (menu phụ): `1` toàn bộ, mỗi dòng kèm `số dư <tiền>` sau giao dịch đó, **tính trong một lượt duyệt**; `2` k giao dịch gần nhất, mới nhất trước.

**Chức năng 2 — Ghi giao dịch.** Nhập loại (THU/CHI, gõ thường được) và số tiền; mã tự sinh tiếp theo (`GD007`); in `Đã ghi <mã>. Số dư: <tiền>`.

**Chức năng 3 — Báo cáo** (menu phụ): `1` tổng thu, tổng chi, số dư; `2` top 3 khoản chi lớn nhất, bằng nhau giữ thứ tự trong sổ, không làm đổi sổ.

**Chức năng 4 — Đo hiệu năng.** Hàm `benchmark` đo bằng `timeit` thời gian một lần tính số dư cuối và lấy `sys.getsizeof` của list sổ, với sổ giả lập (`make_big_book`, có sẵn) n = 20.000, 40.000, 80.000.

**Chức năng 5 — Thoát.** In `Chốt ca với số dư <tiền>. Tạm biệt!`.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== CIRCLE K LÊ LỢI - SỔ QUỸ TRONG CA =====
1. Xem sổ quỹ
2. Ghi giao dịch
3. Báo cáo
4. Đo hiệu năng
5. Thoát
Chọn chức năng (1-5): 1
1. Toàn bộ kèm số dư  2. k giao dịch gần nhất
Chọn cách xem: 1
GD001 | THU | 450.000đ | số dư 2.450.000đ
GD002 | CHI | 120.000đ | số dư 2.330.000đ
GD003 | THU | 980.000đ | số dư 3.310.000đ
GD004 | CHI | 300.000đ | số dư 3.010.000đ
GD005 | THU | 215.000đ | số dư 3.225.000đ
GD006 | CHI | 75.000đ | số dư 3.150.000đ

[menu chính]
Chọn chức năng (1-5): 2
Loại (THU/CHI): chi
Số tiền (đồng): 500000
Đã ghi GD007. Số dư: 2.650.000đ

[menu chính]
Chọn chức năng (1-5): 1
1. Toàn bộ kèm số dư  2. k giao dịch gần nhất
Chọn cách xem: 2
Số giao dịch: 2
GD007 | CHI | 500.000đ
GD006 | CHI | 75.000đ

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in bảng dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | tính số dư (ms) | getsizeof list sổ (byte)
20000 | 0.74 | 173016
40000 | 1.47 (x2.0) | 351064
80000 | 3.19 (x2.2) | 711960
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Chi vượt quỹ.** `Lỗi: Không đủ tiền trong quỹ: số dư <tiền>`, sổ giữ nguyên; chi đúng bằng số dư thì được (số dư về 0).

**Bẫy 2 — Dữ liệu sai.** Loại khác THU/CHI; số tiền `0`, `-5`, `1.5`, chữ: đúng thông báo trong docstring của `add_tx`; k không phải số nguyên dương: `Lỗi: Số giao dịch phải là số nguyên dương`.

**Bẫy 3 — Số dư từng dòng với sổ dài.** 40.000 giao dịch phải xong trong 1 giây.

**Bẫy 4 — Khoản chi bằng nhau, chưa có khoản chi.** Giữ thứ tự trong sổ; không có khoản chi nào thì in `Chưa có khoản chi nào.`

**Bẫy 5 — Menu sai.** Menu phụ: `Lựa chọn không hợp lệ.`; menu chính: `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.`

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- So sánh hai cách tính số dư từng dòng: cộng lại từ đầu cho mỗi dòng và một lượt duyệt: số phép cộng theo n, Big-O, thời gian ước tính với 40.000 giao dịch.
- Bảng số đo của chức năng 4 trên máy bạn; thời gian và `getsizeof` tăng bao nhiêu lần khi n gấp đôi? `getsizeof` của list sổ có tính các list con không?

**(2) Triển khai code**

- Viết các hàm trong `so_quy.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session02_TH06`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-02-thuc-hanh-cli/bai-06 rồi chép các tệp vào kho: `so_quy.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
