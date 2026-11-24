# Hệ thống danh sách Xem tiếp của FPT Play

### 1. Bối cảnh & Vấn đề

![Người dùng FPT Play mở danh sách Xem tiếp](minh_hoa.png)

*Người dùng FPT Play mở danh sách Xem tiếp*

Màn hình chính của **FPT Play** có hàng **Xem tiếp**: chương trình vừa mở đứng đầu, chương trình lâu không mở lại đứng cuối, tối đa **5** chương trình. Mở lại một chương trình đã có thì nó chuyển lên đầu, không xuất hiện hai lần; xem xong thì nó biến mất khỏi hàng.

Bản thử nghiệm có lỗi: chuyển chương trình ở cuối hàng lên đầu thì hàng bị cắt mất phần sau; xóa hết rồi mở chương trình mới thì ứng dụng báo lỗi. Đội kỹ thuật yêu cầu cài lại bằng **danh sách liên kết đơn có `head`, `tail`**, xử lý đúng mọi trường hợp biên.

Bạn xây dựng module **"FPT Play Continue Watching CLI"**.

### 2. Yêu cầu nghiệp vụ

Danh sách mẫu: `make_list()` có 4 chương trình. Lớp `Node` và hàm `to_text` có sẵn.

**Chức năng 1 — Xem danh sách**: chuỗi `to_text()` và `Có <n> chương trình`.

**Chức năng 2 — Mở một chương trình**: đưa lên đầu; vượt 5 chương trình thì bỏ chương trình ở cuối và in `Đã bỏ chương trình cũ nhất: <tên>.`

**Chức năng 3 — Xem tiếp**: chương trình ở đầu. **Chức năng 4 — Đánh dấu đã xem xong.** **Chức năng 5 — Thoát.**

Các phương thức của `ContinueList` không dùng list Python để lưu.

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== FPT PLAY - XEM TIẾP =====
1. Xem danh sách
2. Mở một chương trình
3. Xem tiếp
4. Đánh dấu đã xem xong
5. Thoát
Chọn chức năng (1-5): 1
Cà phê sáng -> V-League vòng 5 -> Thời sự 19h -> Phim tối thứ Bảy -> None
Có 4 chương trình

[menu chính]
Chọn chức năng (1-5): 2
Tên chương trình: Thời sự 19h
Đang xem: Thời sự 19h.

[menu chính]
Chọn chức năng (1-5): 2
Tên chương trình: Đố vui cuối tuần
Đang xem: Đố vui cuối tuần.

[menu chính]
Chọn chức năng (1-5): 2
Tên chương trình: Hoạt hình cho bé
Đang xem: Hoạt hình cho bé.
Đã bỏ chương trình cũ nhất: Phim tối thứ Bảy.

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Mở lại chương trình ở cuối.** Xóa node `tail` rồi thêm vào đầu: `tail` phải lùi về node trước.

**Bẫy 2 — Danh sách rỗng.** `add_first` vào danh sách rỗng phải đặt cả `tail`; xóa node duy nhất đưa cả hai về `None`.

**Bẫy 3 — Không trùng, đúng giới hạn.** Mở lại chương trình đang ở đầu không tạo bản thứ hai; luôn tối đa 5.

**Bẫy 4 — Nhập sai.** Tên trống hoặc dài hơn 40 ký tự; xem xong chương trình không có; menu sai: đúng thông báo của đề.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Vẽ sơ đồ `head`, `tail` trước và sau khi mở lại chương trình đang ở cuối; khi mở chương trình thứ sáu.
- Bảng trường hợp biên của `add_first` và `remove` (rỗng, một node, trúng `head`, trúng `tail`, không có); Big-O của `watch` theo số chương trình n.

**(2) Triển khai code**

- Viết các hàm trong `xem_tiep.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session08_TH02`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-08-thuc-hanh-cli/bai-02 rồi chép các tệp vào kho: `xem_tiep.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
