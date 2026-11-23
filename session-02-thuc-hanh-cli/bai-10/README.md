# Tối ưu bảng xếp hạng giải Liên Quân Mobile của Garena

### 1. Bối cảnh & Vấn đề

![Ban tổ chức Garena cập nhật bảng xếp hạng sau mỗi trận](minh_hoa.png)

*Ban tổ chức Garena cập nhật bảng xếp hạng sau mỗi trận*

Giải đấu cộng đồng **Liên Quân Mobile** do **Garena** tổ chức lưu danh sách đăng ký, mỗi người chơi là `[tên trong game, điểm xếp hạng]`. Bảng xếp hạng: **điểm cao trước; bằng điểm thì ai đăng ký trước xếp trước**. Sau mỗi trận, điểm được cộng hoặc trừ và người chơi mở ứng dụng xem hạng của mình.

Hai hàm `top_slow` và `rank_slow` (có sẵn, **không được sửa**) là bản đang chạy: đúng, nhưng mùa giải có hàng trăm nghìn người chơi; mỗi lần tra hạng, `rank_slow` dựng lại cả bảng xếp hạng và máy chủ quá tải giờ cao điểm. Bạn viết `top_fast`, `rank_fast` cho **kết quả giống hệt**, đưa vào ứng dụng, chứng minh bằng số đo, rồi tìm hiểu cách Python sắp xếp.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_players()` trả về bản sao 6 người chơi (xem `xep_hang.py`).

**Chức năng 1 — Xem top k.** In `<hạng>. <tên> - <điểm> điểm`.

**Chức năng 2 — Cập nhật điểm sau trận.** Nhập tên (không phân biệt hoa thường) và điểm trận từ -100 đến 100 (`+25`, `-40`); điểm không xuống dưới 0; in điểm mới và hạng mới.

**Chức năng 3 — Tra cứu hạng.** In `Hạng của <tên>: <h>/<n> (<điểm> điểm).`

**Chức năng 4 — Đo so sánh** thời gian tra hạng của bản cũ và bản mới với n = 500, 1.000, 2.000 (danh sách giả lập `make_big_players`, có sẵn).

**Chức năng 5 — Thoát.** In `Đã khóa bảng xếp hạng. GG!`.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== GARENA LIÊN QUÂN - BẢNG XẾP HẠNG MÙA 30 =====
1. Xem top k
2. Cập nhật điểm sau trận
3. Tra cứu hạng
4. Đo so sánh bản cũ và bản mới
5. Thoát
Chọn chức năng (1-5): 1
Số người: 6
1. ShadowFox - 2350 điểm
2. KiraVN - 2350 điểm
3. Tí Nị - 2100 điểm
4. Bông - 1980 điểm
5. Zed99 - 1980 điểm
6. MèoMun - 1520 điểm

[menu chính]
Chọn chức năng (1-5): 3
Tên người chơi: kiravn
Hạng của KiraVN: 2/6 (2350 điểm).

[menu chính]
Chọn chức năng (1-5): 2
Tên người chơi: zed99
Điểm trận (+/-): +25
Zed99 có 2005 điểm, hạng 4/6.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in bảng dạng sau (số đo trên máy soạn đề, Python 3.10):

```plaintext
n | bản cũ (ms) | bản mới (ms)
500 | 4.9 | 0.04
1000 | 19.6 (x4.0) | 0.08 (x2.0)
2000 | 78.8 (x4.0) | 0.17 (x2.1)
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Bằng điểm.** `ShadowFox` và `KiraVN` cùng 2350 điểm: ShadowFox hạng 1 vì đăng ký trước.

**Bẫy 2 — Khớp bản cũ.** Kiểm tra so sánh hai bản trên 200 danh sách ngẫu nhiên có rất nhiều người bằng điểm; top k với k lớn hơn số người, danh sách rỗng.

**Bẫy 3 — Ràng buộc.** Bản mới không gọi bản cũ; `rank_fast` không sắp xếp; không làm đổi danh sách đăng ký; 200.000 người chơi trong 2 giây.

**Bẫy 4 — Điểm không âm.** Trừ quá số điểm hiện có thì điểm về 0.

**Bẫy 5 — Nhập sai.** Tên không có, điểm trận ngoài -100..100 hoặc không phải số nguyên, k không phải số nguyên dương, menu sai: đúng thông báo của đề.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Phân tích `top_slow`, `rank_slow`: số bước theo n, Big-O; vì sao tra hạng một người lại tốn như dựng cả bảng.
- Thiết kế `top_fast`, `rank_fast` (giải thích vì sao bằng điểm vẫn đúng thứ tự); Big-O hai bản; bảng số đo chức năng 4 trên máy bạn.

**(3) Nghiên cứu mở rộng (mục cuối `PHAN_TICH.md`, được hỏi AI, phải ghi nguồn)**

- Tìm hiểu thuật toán sắp xếp của Python (Timsort): **tính ổn định** là gì, vì sao `top_fast` cần nó; vì sao Timsort chạy rất nhanh trên dữ liệu gần như đã xếp.
- Tạo `nghien_cuu.py`: đo `sorted` trên 200.000 số ngẫu nhiên, đã xếp, xếp ngược, đã xếp nhưng đảo 1% vị trí; minh họa tính ổn định bằng một ví dụ bằng điểm.

**(2) Triển khai code**

- Viết các hàm trong `xep_hang.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 8 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session02_TH10`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-02-thuc-hanh-cli/bai-10 rồi chép các tệp vào kho: `xep_hang.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`, `nghien_cuu.py (tự tạo)`.
2. Mức AI: AI-0 cho phân tích và mã; AI-1 cho nghiên cứu mở rộng (ghi nguồn, tự kiểm chứng).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
