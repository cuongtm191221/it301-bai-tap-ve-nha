# Hệ thống đảo chiều hành trình nhiều chặng của Vietnam Airlines

### 1. Bối cảnh & Vấn đề

![Nhân viên Vietnam Airlines lập hành trình chiều về](minh_hoa.png)

*Nhân viên Vietnam Airlines lập hành trình chiều về*

Hệ thống đặt vé **Vietnam Airlines** lưu hành trình nhiều chặng (ví dụ `HAN -> DAD -> SGN -> PQC`) bằng **danh sách liên kết đơn có `head`, `tail`**. Khách đặt khứ hồi thì chiều về là hành trình **đảo chiều**. Hệ thống giá vé đang giữ tham chiếu tới từng node nên phải đảo **ngay trên hành trình**: không tạo node mới, không chép sang list.

Bản đầu tiên đảo đúng nhưng với các hành trình giả lập dài (kiểm thử tải) thì chạy rất lâu; bản sửa nhanh thì quên cập nhật `tail`, thêm sân bay sau khi đảo bị nối sai chỗ. Trưởng nhóm yêu cầu hai giải pháp đúng, so sánh bằng số đo và phân tích.

Bạn xây dựng module **"Vietnam Airlines Return Route CLI"**.

### 2. Yêu cầu nghiệp vụ

Hành trình mẫu: `make_route()`. Lớp `Node`, `Route` (có `add_last`, `to_text`) có sẵn.

**Chức năng 1 — Xem hành trình.** **Chức năng 2 — Thêm sân bay** vào cuối (3 chữ cái, không trùng điểm cuối). **Chức năng 3 — Đảo chiều** (menu phụ chọn giải pháp), in `Chiều về: ...`.

**Chức năng 4 — Đo** hai giải pháp với n = 1.000, 2.000, 4.000. **Chức năng 5 — Thoát.**

`reverse_v1`, `reverse_v2` cho **cùng kết quả**, **khác nhau về cách làm**, đảo ngay trên hành trình (không tạo node, không dùng list); giải pháp 2 đảo 200.000 điểm trong 1 giây.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== VIETNAM AIRLINES - HÀNH TRÌNH NHIỀU CHẶNG =====
1. Xem hành trình
2. Thêm sân bay
3. Đảo chiều hành trình
4. Đo so sánh hai giải pháp
5. Thoát
Chọn chức năng (1-5): 1
HAN -> DAD -> SGN -> PQC -> None

[menu chính]
Chọn chức năng (1-5): 3
1. Giải pháp 1  2. Giải pháp 2
Chọn giải pháp: 1
Chiều về: PQC -> SGN -> DAD -> HAN -> None

[menu chính]
Chọn chức năng (1-5): 2
Mã sân bay: cxr
Đã thêm CXR.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (máy soạn đề, Python 3.10):

```plaintext
n | giải pháp 1 (ms) | giải pháp 2 (ms)
1000 | 9.65 | 0.04
2000 | 40.92 | 0.08
4000 | 160.42 | 0.17
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — `head`, `tail` sau khi đảo.** Node đầu cũ thành `tail` với `next` là `None`; thêm sân bay sau khi đảo phải nối đúng.

**Bẫy 2 — Hành trình ngắn.** Rỗng, một điểm, hai điểm, số điểm lẻ.

**Bẫy 3 — Giữ node.** Không tạo node mới, không chép sang list; đảo hai lần về như cũ.

**Bẫy 4 — Dữ liệu lớn.** 200.000 điểm: giải pháp 2 trong 1 giây.

**Bẫy 5 — Nhập sai.** Mã không đủ 3 chữ cái (gõ thường hợp lệ), trùng điểm cuối; menu phụ và menu chính sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Đề xuất ít nhất hai giải pháp khác nhau (ý tưởng, sơ đồ trên 4 điểm mẫu, mã giả); với mỗi giải pháp, đếm số node phải đi qua khi đảo n điểm.
- Bảng so sánh 5 tiêu chí (tốc độ, bộ nhớ phụ, độ dễ đọc, dễ bảo trì, phù hợp bối cảnh) kèm số đo chức năng 4 trên máy bạn; chọn giải pháp và giải thích.

**(2) Triển khai code**

- Viết các hàm trong `hanh_trinh.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 7 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session08_TH07`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-08-thuc-hanh-cli/bai-07 rồi chép các tệp vào kho: `hanh_trinh.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
