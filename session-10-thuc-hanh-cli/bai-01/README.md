# Hệ thống soạn tin nhắn có hoàn tác của Zalo

### 1. Bối cảnh & Vấn đề

![Người dùng Zalo soạn tin nhắn và bấm hoàn tác](minh_hoa.png)

*Người dùng Zalo soạn tin nhắn và bấm hoàn tác*

Khung soạn tin của **Zalo** trên máy tính hỗ trợ **Hoàn tác** (Ctrl+Z) và **Làm lại** (Ctrl+Y). Để dễ thử nghiệm, nhóm sản phẩm mô phỏng tin nhắn ở mức **từ**: người dùng gõ thêm một từ vào cuối hoặc xóa từ cuối; hoàn tác thao tác gần nhất trước (vào sau ra trước).

Bản thử nghiệm có lỗi: hoàn tác một lần xóa thì từ không quay lại; sau khi hoàn tác rồi gõ từ mới, bấm làm lại vẫn làm lại thao tác cũ. Đội kỹ thuật yêu cầu cài lại bằng **hai ngăn xếp** (hoàn tác và làm lại), ngăn xếp cài bằng list với đỉnh ở cuối.

Bạn xây dựng module **"Zalo Draft Undo CLI"**.

### 2. Yêu cầu nghiệp vụ

Lớp `Draft` có sẵn; chương trình bắt đầu với tin nhắn đã gõ `Chào anh Hùng`.

**Chức năng 1 — Xem tin nhắn.** **Chức năng 2 — Gõ một từ** (1 đến 20 ký tự, không có khoảng trắng). **Chức năng 3 — Xóa từ cuối.**

**Chức năng 4 — Hoàn tác** thao tác gần nhất. **Chức năng 5 — Làm lại** thao tác vừa hoàn tác. **Chức năng 6 — Thoát.**

Thao tác gõ hoặc xóa mới làm mất các thao tác đang chờ làm lại. `ArrayStack` có `push`, `pop`, `peek`, `is_empty`, `size`; lấy khi rỗng báo `IndexError("ngăn xếp rỗng")`.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== ZALO - SOẠN TIN NHẮN =====
1. Xem tin nhắn
2. Gõ một từ
3. Xóa từ cuối
4. Hoàn tác
5. Làm lại
6. Thoát
Chọn chức năng (1-6): 1
Tin nhắn: Chào anh Hùng

[menu chính]
Chọn chức năng (1-6): 3
Đã xóa "Hùng". Tin nhắn: Chào anh

[menu chính]
Chọn chức năng (1-6): 2
Từ: Lan
Tin nhắn: Chào anh Lan

[menu chính]
Chọn chức năng (1-6): 4
Đã hoàn tác (gõ "Lan"). Tin nhắn: Chào anh

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Hoàn tác một lần xóa.** Từ bị xóa phải quay lại cuối tin nhắn.

**Bẫy 2 — Thao tác mới sau khi hoàn tác.** Làm lại không còn tác dụng: `Lỗi: Không có thao tác để làm lại`.

**Bẫy 3 — Hoàn tác hết.** Tin nhắn `(trống)`; hoàn tác tiếp báo `Lỗi: Không có thao tác để hoàn tác`.

**Bẫy 4 — `peek` không lấy ra.** Gọi `peek` hai lần liên tiếp vẫn cùng phần tử, `size` không đổi.

**Bẫy 5 — Nhập sai.** Từ trống, có khoảng trắng, dài hơn 20 ký tự; xóa khi trống; menu sai.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Vẽ hai ngăn xếp hoàn tác và làm lại sau từng thao tác của màn hình mẫu.
- Vì sao đỉnh ngăn xếp nên ở cuối list chứ không ở đầu (Big-O của `push`, `pop` mỗi cách).

**(2) Triển khai code**

- Viết các hàm trong `soan_tin.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 4 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session10_TH01`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-10-thuc-hanh-cli/bai-01 rồi chép các tệp vào kho: `soan_tin.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
