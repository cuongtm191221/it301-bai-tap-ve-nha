# Dọn danh sách đơn của nhà hàng GrabFood tại chỗ

### 1. Bối cảnh & Vấn đề

![Cuối ngày, danh sách đơn của nhà hàng phải bỏ đơn hủy và chỉ giữ các đơn mới nhất, mà không làm mất danh sách đang hiển thị.](minh_hoa.png)

*Cuối ngày, danh sách đơn của nhà hàng phải bỏ đơn hủy và chỉ giữ các đơn mới nhất, mà không làm mất danh sách đang hiển thị.*

Ứng dụng **GrabMerchant** của nhà hàng giữ một list đơn trong ngày, mỗi đơn là bộ `(mã, trạng thái)`. Cuối ngày, ứng dụng **dọn danh sách**: bỏ mọi đơn đã hủy, rồi chỉ giữ `k` đơn mới nhất (ở cuối list) để màn hình nhẹ.

List này đang được **màn hình và bộ đếm doanh thu cùng tham chiếu**, nên phải sửa **tại chỗ** (cùng một list), không được tạo list mới rồi trả về. Trạng thái do nhiều phiên bản ứng dụng ghi nên có dạng `"CANCELLED"`, `" cancelled "`, `"Cancelled"`; hàm `is_cancelled(status)` (có sẵn) đã xử lý việc này.

Ví dụ trong kịch bản chạy thử có 7 đơn, trong đó ba đơn đã hủy (hai đơn đứng liền nhau); sau khi bỏ đơn hủy và giữ 3 đơn mới nhất, màn hình chỉ còn `GF4`, `GF5`, `GF7`. Số đơn bị xóa còn được gửi về bộ phận chất lượng để theo dõi tỉ lệ hủy của nhà hàng, nên con số trả về phải chính xác.

Một nhà hàng lớn có **200.000 đơn** trong đợt khuyến mãi. Bản cũ duyệt list và gọi `remove` mỗi khi gặp đơn hủy: vừa bỏ sót đơn hủy đứng liền nhau, vừa chậm vì mỗi lần `remove` phải tìm lại từ đầu và dồn phần sau. Nhóm yêu cầu cả thao tác dọn chạy trong **1 giây**.

### 2. Yêu cầu nghiệp vụ

**2.1. `remove_cancelled(orders)`**: xóa tại chỗ mọi đơn đã hủy, giữ thứ tự các đơn còn lại; trả về số đơn đã xóa.

**2.2. `keep_last(orders, k)`**: chỉ giữ tại chỗ `k` đơn cuối list theo đúng thứ tự; trả về số đơn đã bỏ.

**2.3. `cleanup_message(orders, k)`**: chạy hai bước trên, trả về:

```plaintext
Đã xóa 3 đơn hủy, bỏ 1 đơn cũ, còn 3 đơn.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Đơn hủy đứng liền nhau.** Ví dụ trong kịch bản có `GF2`, `GF3` cùng hủy liền nhau; không được bỏ sót.

**Bẫy 2 — Không có đơn hủy, hoặc toàn bộ đều hủy.** Trả 0 và list giữ nguyên; hoặc list thành rỗng.

**Bẫy 3 — k ở biên.** `k` lớn hơn hoặc bằng số đơn: giữ nguyên, trả 0; `k` bằng 0 hoặc âm: list thành rỗng.

**Bẫy 4 — Sửa tại chỗ.** Sau khi gọi, biến giữ list ban đầu vẫn trỏ tới chính list đã được dọn (`is`).

**Bẫy 5 — 200.000 đơn trong 1 giây.** Không gọi `remove`, `pop`, `insert` trong hai hàm dọn.

**Kịch bản chạy thử.** Chạy `python loc_don.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Xóa đơn hủy: 3 | [('GF1', 'DONE'), ('GF4', 'DONE'), ('GF5', 'PENDING'), ('GF7', 'DONE')]
Giữ 3 đơn mới nhất: 1 | [('GF4', 'DONE'), ('GF5', 'PENDING'), ('GF7', 'DONE')]
Vẫn là cùng một list: True
Đã xóa 66667 đơn hủy, bỏ 132333 đơn cũ, còn 1000 đơn. | đơn đầu: GF198500
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng hàm hoặc phương thức, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Thiết kế giải pháp: chạy tay bản cũ (duyệt và `remove`) trên ví dụ để chỉ ra vì sao bỏ sót đơn hủy liền nhau, và đếm số tham chiếu phải dịch.
- Mô tả cách dọn chỉ duyệt mỗi đơn một lần mà vẫn sửa tại chỗ (cần những biến chỉ số nào, mỗi bước làm gì, cuối cùng xử lý phần thừa ở đuôi thế nào). Chạy tay trên ví dụ.
- `keep_last` dời k đơn cuối lên đầu: có bị ghi đè đơn chưa kịp dời không? Vì sao?
- Một bạn đề xuất viết `orders = [o for o in orders if not is_cancelled(o[1])]` bên trong hàm. Cách này có đáp ứng yêu cầu sửa tại chỗ không? Kiểm chứng bằng `is` và giải thích.
- Lệnh cắt đuôi cuối cùng (xóa phần thừa sau chỉ số ghi) tốn bao nhiêu thao tác? Vì sao không làm thay đổi Big-O của cả hàm?
- Bộ dữ liệu thử: lập bảng ít nhất 6 đầu vào phủ đủ 5 bẫy ở mục 3, mỗi dòng ghi kết quả mong đợi (tính tay trước khi chạy) và kết quả chạy thật của bài làm.
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của bản cũ và của hai hàm bạn viết theo n (số đơn) và k.

**(2) Triển khai code**

- Viết thân các hàm, phương thức còn trống trong `loc_don.py`. Không đổi tên, tham số, thông báo lỗi; hàm ghi "Có sẵn" giữ nguyên; được thêm thuộc tính và hàm phụ.
- Sửa tại chỗ; không gọi `remove`, `pop`, `insert` trong `remove_cancelled` và `keep_last`.
- Xử lý đủ 5 bẫy ở mục 3; `python loc_don.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 7 test có sẵn.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ quyết định độ phức tạp.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex12`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-12 rồi chép các tệp vào kho: `loc_don.py`, `test_loc_don.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `loc_don.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
