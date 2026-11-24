# Tối ưu chốt ca bán hàng trên KiotViet

### 1. Bối cảnh & Vấn đề

![Chủ cửa hàng chờ phần mềm KiotViet chốt ca](minh_hoa.png)

*Chủ cửa hàng chờ phần mềm KiotViet chốt ca*

Chuỗi tạp hóa dùng **KiotViet**: mỗi mặt hàng có **mã 4 chữ số** (0000–9999, không trùng), tên và tồn đầu ca. Cuối ca, phần mềm **chốt ca**: áp lần lượt các giao dịch bán; giao dịch có mã không nằm trong danh mục, hoặc bán nhiều hơn tồn hiện tại, bị **từ chối** để kế toán kiểm tra.

Hàm `close_slow` trong `chot_ca.py` cho kết quả đúng nhưng mỗi giao dịch lại dò cả danh mục; cửa hàng 10.000 mặt hàng, 200.000 giao dịch mỗi ca thì chốt ca không xong. Cần **viết lại** thành `close_fast` cho **đúng y hệt** kết quả cũ, chỉ dùng list, và giải thích vì sao cách mới làm được.

Bạn xây dựng module **"KiotViet Shift Closing CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_catalog()` có 5 mặt hàng, `make_sales()` có 7 giao dịch (xem `chot_ca.py`); `close_slow` là hàm Có sẵn, **không sửa**.

**Chức năng 1 — Xem danh mục đầu ca.** **Chức năng 2 — Ghi giao dịch bán** (mã, số lượng). **Chức năng 3 — Chốt ca** bằng `close_fast`: in tồn cuối ca từng mặt hàng và `Giao dịch bị từ chối: <các số thứ tự>` (hoặc `không có`).

**Chức năng 4 — Đo** bản cũ và bản mới với n = 500, 1.000, 2.000 (n mặt hàng, n giao dịch). **Chức năng 5 — Thoát.**

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== KIOTVIET - CHỐT CA BÁN HÀNG =====
1. Xem danh mục đầu ca
2. Ghi giao dịch bán
3. Chốt ca
4. Đo bản cũ và bản mới
5. Thoát
Chọn chức năng (1-5): 1
1001 | Mì Hảo Hảo | tồn 50
1002 | Sữa TH 180ml | tồn 24
2005 | Nước mắm Nam Ngư | tồn 10
3010 | Gạo ST25 5kg | tồn 5
4500 | Dầu ăn Neptune 1L | tồn 8

[menu chính]
Chọn chức năng (1-5): 3
1001 | Mì Hảo Hảo | còn 47
1002 | Sữa TH 180ml | còn 0
2005 | Nước mắm Nam Ngư | còn 0
3010 | Gạo ST25 5kg | còn 0
4500 | Dầu ăn Neptune 1L | còn 8
Giao dịch bị từ chối: 3, 4, 5

[menu chính]
Chọn chức năng (1-5): 2
Mã hàng: 4500
Số lượng: 3
Đã ghi giao dịch 8: 4500 x 3.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | bản cũ (ms) | bản mới (ms)
500 | 7.0 | 0.1
1000 | 28.8 | 0.1
2000 | 115.7 | 0.3
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ.** Xét theo thứ tự: `3010` bán 6 bị từ chối (tồn 5), bán 5 sau đó vẫn hợp lệ.

**Bẫy 2 — Biên.** Mã `0000` và `9999`; bán đúng bằng tồn là hợp lệ; danh mục rỗng thì mọi giao dịch bị từ chối.

**Bẫy 3 — Ràng buộc.** Không gọi bản cũ, không `dict`, `set`, không làm đổi dữ liệu vào; 10.000 mặt hàng và 200.000 giao dịch trong 1 giây.

**Bẫy 4 — Dữ liệu sai.** Mã sai dạng; số lượng 0, âm, thập phân.

**Bẫy 5 — Menu sai.** `Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.`

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Phân tích `close_slow`: số lần so sánh mã theo số mặt hàng n và số giao dịch m; Big-O; vì sao danh mục 10.000 hàng và 200.000 giao dịch không xong.
- Thiết kế `close_fast`: dựa vào điều gì của mã hàng; Big-O thời gian và bộ nhớ phụ; bảng số đo chức năng 4 trên máy bạn.

**(3) Nghiên cứu mở rộng (mục cuối `PHAN_TICH.md`, được hỏi AI, phải ghi nguồn)**

- Tìm hiểu "địa chỉ trực tiếp" (direct addressing): khi nào dùng được; nếu mã hàng là mã vạch 13 chữ số thì cách của bạn cần bao nhiêu bộ nhớ; bảng băm (Session 13) giải quyết điều đó thế nào (chỉ nêu ý tưởng).
- Tạo `nghien_cuu.py`: in `sys.getsizeof` của list `[-1] * 10**4` và `[-1] * 10**6`, ước lượng (không tạo) cho `10**13` ô; với 6 mã vạch tự chọn, in phần dư khi chia cho 10.007 và chỉ ra nếu có hai mã cùng phần dư.

**(2) Triển khai code**

- Viết các hàm trong `chot_ca.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session06_TH10`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-06-thuc-hanh-cli/bai-10 rồi chép các tệp vào kho: `chot_ca.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`, `nghien_cuu.py (tự tạo)`.
2. Mức AI: AI-0 cho phân tích và mã; AI-1 cho nghiên cứu mở rộng (ghi nguồn, tự kiểm chứng).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
