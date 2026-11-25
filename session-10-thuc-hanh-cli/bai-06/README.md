# Hệ thống màn hình bếp của Jollibee

### 1. Bối cảnh & Vấn đề

![Đầu bếp Jollibee theo dõi màn hình đơn hàng](minh_hoa.png)

*Đầu bếp Jollibee theo dõi màn hình đơn hàng*

Màn hình bếp của **Jollibee** chỉ hiện **6 đơn gần nhất** (mã `JBxxx`, món). Đơn mới vào khi màn hình đã đủ thì đơn cũ nhất rời màn hình; bếp làm xong đơn nào thì bấm để bỏ đơn đó, nhường chỗ.

Hệ thống báo cáo của chuỗi cũng cần giữ "N sự kiện gần nhất" với N hàng nghìn. Bản cũ giữ bằng list: hoặc `del items[0]` khi đầy, hoặc cắt lấy N phần tử cuối sau mỗi lần thêm. Đội kỹ thuật đề xuất `deque(maxlen=N)` và cần **số đo thật** ba cách.

Bạn xây dựng module **"Jollibee Kitchen Display CLI"**.

### 2. Yêu cầu nghiệp vụ

Màn hình mẫu: `make_board()` có 5 đơn. `Board` (`orders` là `deque(maxlen=6)`), `keep_last_del`, `keep_last_slice` có sẵn.

**Chức năng 1 — Xem màn hình** và `Đang hiện <k>/6 đơn`. **Chức năng 2 — Thêm đơn**: đơn bị đẩy ra thì in `<mã> rời màn hình.` **Chức năng 3 — Bếp làm xong đơn.**

**Chức năng 4 — Đo** ba cách giữ N phần tử gần nhất khi thêm 20.000 phần tử (N = 1.000, 2.000, 4.000). **Chức năng 5 — Thoát.**

`keep_last_deque` dùng `maxlen`, không tự xóa phần tử.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== JOLLIBEE - MÀN HÌNH BẾP =====
1. Xem màn hình
2. Thêm đơn
3. Bếp làm xong đơn
4. Đo ba cách giữ N đơn gần nhất
5. Thoát
Chọn chức năng (1-5): 1
JB001 | Gà giòn 2 miếng
JB002 | Mì Ý sốt bò
JB003 | Burger tôm
JB004 | Gà giòn 1 miếng
JB005 | Kem sundae
Đang hiện 5/6 đơn

[menu chính]
Chọn chức năng (1-5): 2
Món: Cơm gà sốt cay
Đã thêm JB006: Cơm gà sốt cay.

[menu chính]
Chọn chức năng (1-5): 2
Món: Khoai tây chiên
Đã thêm JB007: Khoai tây chiên.
JB001 rời màn hình.

[menu chính]
Chọn chức năng (1-5): 1
JB002 | Mì Ý sốt bò
JB003 | Burger tôm
JB004 | Gà giòn 1 miếng
JB005 | Kem sundae
JB006 | Cơm gà sốt cay
JB007 | Khoai tây chiên
Đang hiện 6/6 đơn

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

Chức năng 4 in dạng sau (máy soạn đề, Python 3.10):

```plaintext
n | del items[0] (ms) | cắt lát (ms) | deque (ms)
1000 | 3.5 | 17.9 | 0.5
2000 | 5.5 | 32.3 | 0.5
4000 | 8.7 | 85.6 | 0.5
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Đơn rời màn hình.** Chỉ khi màn hình đã đủ 6 đơn; báo đúng đơn cũ nhất.

**Bẫy 2 — Làm xong rồi thêm.** Sau khi bỏ một đơn, màn hình còn chỗ: đơn mới không đẩy đơn nào ra.

**Bẫy 3 — Ít hơn N.** Thêm ít hơn N phần tử thì giữ tất cả, đúng thứ tự.

**Bẫy 4 — Nhập sai.** Tên món trống hoặc dài; mã không có trên màn hình (gõ thường hợp lệ); menu sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Big-O mỗi lần thêm của ba cách theo N; tổng cho m lần thêm; bảng số đo chức năng 4 trên máy bạn (N gấp đôi thì mỗi cột tăng mấy lần).
- Vì sao `finish` dùng `remove` trên deque vẫn chấp nhận được với màn hình 6 đơn; nếu N là 100.000 thì sao. Kết luận cho Jollibee.

**(2) Triển khai code**

- Viết các hàm trong `man_hinh_bep.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 5 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session10_TH06`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-10-thuc-hanh-cli/bai-06 rồi chép các tệp vào kho: `man_hinh_bep.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
