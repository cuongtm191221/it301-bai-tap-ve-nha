# Hệ thống sắp xếp lộ trình giao hàng của tài xế Ahamove

### 1. Bối cảnh & Vấn đề

![Tài xế Ahamove sắp lại các điểm dừng trong ngày](minh_hoa.png)

*Tài xế Ahamove sắp lại các điểm dừng trong ngày*

Mỗi sáng, tài xế **Ahamove** nhận một **lộ trình**: list tên các điểm dừng theo thứ tự đi. Trong ngày, điều phối thường chèn thêm điểm (đơn gấp), xóa điểm (khách hủy), và có khi đảo ngược lộ trình hoặc cho tài xế **bắt đầu từ điểm thứ k** (các điểm trước đó dời xuống cuối).

Để thấy rõ chi phí, nhóm phát triển tự cài các thao tác bằng vòng lặp và **đếm số điểm phải dịch**: chèn ở đầu phải dịch cả lộ trình, chèn ở cuối không dịch gì. Xoay lộ trình phải làm **tại chỗ** (lộ trình của tài xế chạy xe tải liên tỉnh có hàng trăm nghìn điểm quét mã), không cắt lát, không tạo list mới.

Bạn xây dựng module **"Ahamove Route CLI"**.

### 2. Yêu cầu nghiệp vụ

Dữ liệu mẫu: `make_route()` trả về 5 điểm dừng; `check_name` có sẵn (xem `lo_trinh.py`).

**Chức năng 1 — Xem lộ trình** dạng `1. Kho Quận 1 -> 2. Chợ Bến Thành -> ...`

**Chức năng 2 — Chèn điểm dừng** (vị trí 1 đến n + 1): in `Đã chèn vào vị trí <i> (dịch <k> điểm).`

**Chức năng 3 — Xóa điểm dừng** (vị trí 1 đến n): in `Đã xóa <tên> (dịch <k> điểm).`

**Chức năng 4 — Sắp lại lộ trình** (menu phụ): `1` đảo ngược; `2` bắt đầu từ điểm thứ k; in số lần đổi chỗ. **Chức năng 5 — Thoát.**

Các hàm `insert_stop`, `remove_stop`, `reverse_range`, `reverse_route`, `rotate_route` tự dịch, đổi chỗ bằng chỉ số; không dùng `insert`, `pop(i)`, `reverse()`, `[::-1]`, `reversed()`, cắt lát. `rotate_route` dùng ba lần đảo đoạn (gợi ý trong docstring).

Màn hình mẫu (đoạn đầu; phím gõ vào hiện sau dấu hai chấm, `[menu chính]` là menu được in lại):

```plaintext
===== AHAMOVE - LỘ TRÌNH HÔM NAY =====
1. Xem lộ trình
2. Chèn điểm dừng
3. Xóa điểm dừng
4. Sắp lại lộ trình
5. Thoát
Chọn chức năng (1-5): 1
1. Kho Quận 1 -> 2. Chợ Bến Thành -> 3. Nhà thờ Đức Bà -> 4. Landmark 81 -> 5. Thảo Điền

[menu chính]
Chọn chức năng (1-5): 2
Vị trí chèn: 2
Tên điểm dừng: Vincom Đồng Khởi
Đã chèn vào vị trí 2 (dịch 4 điểm).

[menu chính]
Chọn chức năng (1-5): 2
Vị trí chèn: 9
Tên điểm dừng: X
Lỗi: Vị trí phải từ 1 đến 7

[... các lượt sau: thêm dữ liệu sai, nhập menu sai, thoát ...]
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Chèn, xóa ở hai đầu.** Chèn ở cuối dịch 0 điểm, chèn ở đầu dịch n điểm; xóa điểm cuối dịch 0 điểm.

**Bẫy 2 — Vòng dịch đúng chiều.** Dịch từ cuối về khi chèn, từ trước ra sau khi xóa; đi sai chiều sẽ ghi đè mất điểm dừng.

**Bẫy 3 — Xoay ở biên.** Bắt đầu từ điểm 1: giữ nguyên; từ điểm cuối: điểm cuối lên đầu.

**Bẫy 4 — Lộ trình dài.** Xoay 200.000 điểm trong 2 giây.

**Bẫy 5 — Nhập sai.** Vị trí ngoài khoảng hoặc không phải số nguyên, tên trống, lộ trình rỗng khi xóa, menu phụ và menu chính sai: đúng thông báo của đề.

### 4. Yêu cầu

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy; luồng chương trình (mã giả hoặc các bước).
- Bảng số điểm phải dịch khi chèn, xóa ở vị trí 1, giữa, cuối với n điểm; Big-O.
- Chạy tay `rotate_route` trên 5 điểm mẫu với k = 3 (list sau mỗi lần đảo đoạn); vì sao ba lần đảo cho đúng kết quả; số lần đổi chỗ theo n; bộ nhớ phụ so với cách cắt lát.

**(2) Triển khai code**

- Viết các hàm trong `lo_trinh.py` (giữ tên, tham số; hàm "Có sẵn" giữ nguyên) và chương trình menu trong `main.py`. Hàm nghiệp vụ không gọi `input()`, `print()`.
- Thông báo đúng từng chữ như đề; không dừng vì lỗi ở bất kỳ thao tác nào; tên biến snake_case, có chú thích.
- `python kiem_tra.py` đạt cả 6 mục (mục cuối tự chạy `main.py`, gõ một loạt lựa chọn có cả dữ liệu sai, và kiểm tra các thông báo của đề).

### 5. Quy định nộp bài

1. Tạo kho GitHub riêng, đặt tên `[Tên Lớp]_IT301_Session06_TH04`. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-06-thuc-hanh-cli/bai-04 rồi chép các tệp vào kho: `lo_trinh.py`, `main.py`, `kiem_tra.py`, `PHAN_TICH.md`.
2. Mức AI: AI-0 (tự làm, không dùng AI).
3. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
