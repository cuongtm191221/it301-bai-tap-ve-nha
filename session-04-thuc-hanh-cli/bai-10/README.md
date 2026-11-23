# Tối ưu tách chuỗi tìm kiếm cho Điện Máy Xanh

### 1. Bối cảnh & Vấn đề

![Kỹ sư tìm kiếm Điện Máy Xanh xem chuỗi khách gõ liền](minh_hoa.png)

*Kỹ sư tìm kiếm Điện Máy Xanh xem chuỗi khách gõ liền*

Trên website **Điện Máy Xanh**, khách hay gõ liền không dấu: `tainghebluetooth`, `sacduphongkhongday`. Hệ thống tách chuỗi thành **dãy từ khóa** có trong từ điển để tìm sản phẩm. Một chuỗi có thể có nhiều cách tách (`tai nghe bluetooth`, `tainghe blue tooth`...); hệ thống cần **đếm số cách tách** (để đánh giá độ mơ hồ của từ điển) và **gợi ý cách tách ít từ nhất**.

Hàm `count_slow` (có sẵn, **không được sửa**) đệ quy thử từng từ khóa ở đầu chuỗi: chuỗi ngắn chạy tức thì, nhưng khách dán một chuỗi dài lặp lại (`sacduphongsacduphong...`) làm máy chủ treo. Bạn viết `count_fast`, `best_split` cho kết quả đúng và nhanh, đưa vào ứng dụng, chứng minh bằng số đo, rồi tìm hiểu kỹ `functools.lru_cache`.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_keywords()` trả về 18 từ khóa (xem `tach_tu_khoa.py`); `normalize` có sẵn bỏ khoảng trắng, đổi chữ thường.

**Chức năng 1 — Tách chuỗi tìm kiếm.** In `Có <k> cách tách. Gợi ý: <từ> <từ> ...` hoặc `Không tách được: có đoạn chưa có trong từ điển.` Gợi ý là cách ít từ nhất; cùng số từ thì lấy cách nhỏ nhất khi so hai list theo thứ tự chữ cái.

**Chức năng 2 — Thêm từ khóa** (2–20 chữ cái a-z, chưa có). **Chức năng 3 — Xem từ điển** (xếp theo chữ cái). **Chức năng 4 — Đo** bản cũ và bản mới với chuỗi `sacduphong` lặp 6, 8, 10 lần. **Chức năng 5 — Thoát.**

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== ĐIỆN MÁY XANH - TÁCH CHUỖI TÌM KIẾM =====
1. Tách chuỗi tìm kiếm
2. Thêm từ khóa
3. Xem từ điển
4. Đo bản cũ và bản mới
5. Thoát
Chọn chức năng (1-5): 1
Chuỗi tìm kiếm: tai nghe Bluetooth
Có 4 cách tách. Gợi ý: tainghe bluetooth

[menu chính]
Chọn chức năng (1-5): 1
Chuỗi tìm kiếm: sacduphongkhongday
Có 6 cách tách. Gợi ý: sacduphong khongday

[menu chính]
Chọn chức năng (1-5): 1
Chuỗi tìm kiếm: maytinhbang
Không tách được: có đoạn chưa có trong từ điển.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
số lần lặp | bản cũ (ms) | bản mới (ms)
6 | 1.0 | 0.03
8 | 8.7 | 0.04
10 | 78.2 | 0.06
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ.** Kiểm tra trên 100 chuỗi ngẫu nhiên với từ điển có nhiều từ chồng lấn (`a`, `ab`, `ba`, `aba`...).

**Bẫy 2 — Không tách được.** Số cách 0; gợi ý `None`.

**Bẫy 3 — Chuỗi dài.** `sacduphong` lặp 30 lần (300 ký tự) có 3^30 cách: đếm và gợi ý trong 1 giây, không `RecursionError`, không đổi giới hạn đệ quy, không gọi bản cũ.

**Bẫy 4 — Cùng số từ.** `abab` với từ điển `ab, a, b, ba, aba, bab`: gợi ý `a bab` (vì `["a", "bab"]` nhỏ hơn `["ab", "ab"]` và `["aba", "b"]`).

**Bẫy 5 — Nhập sai.** Chuỗi có ký tự ngoài a-z, từ khóa sai hoặc trùng, menu sai: đúng thông báo của đề.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Vẽ cây lời gọi của `count_slow("sacduphong", ...)`; với chuỗi lặp k lần, bản cũ gọi bao nhiêu lần (theo k), Big-O? Những lời gọi nào lặp lại?
- Thiết kế `count_fast`, `best_split`: mỗi vị trí trong chuỗi được tính mấy lần; Big-O theo độ dài chuỗi n và số từ khóa m; bảng số đo chức năng 4 trên máy bạn.

**(3) Nghiên cứu mở rộng (mục cuối `PHAN_TICH.md`, được hỏi AI, phải ghi nguồn)**

- Tìm hiểu `functools.lru_cache`: `cache_info()` (hits, misses), `maxsize`, vì sao tham số phải "băm được" (hashable), bộ nhớ của cache.
- Tạo `nghien_cuu.py`: cho thấy lỗi khi đặt `@lru_cache` lên hàm nhận list từ khóa và cách sửa bằng tuple; in `cache_info()` khi đếm `sacduphong` lặp 10 lần; so thời gian với `maxsize=None` và `maxsize=2`.

**(2) Triển khai code**

- Viết các hàm trong `tach_tu_khoa.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 8 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session04_TH10`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-04-thuc-hanh-cli/bai-10 rồi chép các tệp vào kho: `tach_tu_khoa.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`, `nghien_cuu.py (tự tạo)`.
2. Mức AI: AI-0 cho phân tích và mã; AI-1 cho nghiên cứu mở rộng (ghi nguồn, tự kiểm chứng).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
