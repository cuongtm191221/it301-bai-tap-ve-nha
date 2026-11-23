# Sắp xếp lại danh sách phát trên Zing MP3

### 1. Bối cảnh & Vấn đề

![Người nghe chèn một bài vào giữa danh sách phát và đưa bài yêu thích lên đầu.](minh_hoa.png)

*Người nghe chèn một bài vào giữa danh sách phát và đưa bài yêu thích lên đầu.*

Trong ứng dụng nghe nhạc Zing MP3, người nghe thường xuyên **sắp xếp lại** danh sách phát của mình: chèn một bài mới vào ngay sau bài đang nghe, hoặc đưa một bài yêu thích lên đầu danh sách.

- Mỗi bài trong danh sách phát được lưu dưới dạng chuỗi:

```plaintext
"MÃ_BÀI - TÊN_BÀI"
```

- Ví dụ một danh sách phát có ba bài:

```plaintext
ZM001 - Bình minh trên phố  ->  ZM002 - Mưa đêm  ->  ZM003 - Đường về nhà  ->  None
```

Nếu lưu bằng list Python, mỗi lần chèn vào giữa hay đưa một bài lên đầu đều phải dời hàng loạt phần tử (Session 05). Với **danh sách liên kết đơn có `head`, `tail`, `size`**, khi đã đứng ở đúng node thì chèn hay gỡ chỉ là sửa vài liên kết. Đổi lại, người viết phải tự giữ cho `head`, `tail`, `size` luôn đúng, và phải sửa liên kết **đúng thứ tự** để không làm rơi mất phần sau của danh sách.

Bạn được giao viết lớp `EditablePlaylist` cho tính năng này.

### 2. Yêu cầu nghiệp vụ

Lớp `EditablePlaylist` (khung có sẵn trong `sap_xep.py`) cần bốn chức năng. Mỗi chức năng **trả về** thông báo đúng từng chữ như mô tả. Mọi mã bài nhận vào đều phải được xóa khoảng trắng hai đầu và chuyển thành chữ hoa; tên bài được xóa khoảng trắng hai đầu.

**2.1. Thêm bài vào cuối: `add_song(code, title)`**

Thêm bài vào **cuối** danh sách phát trong O(1) và trả về:

```plaintext
Đã thêm: ZM001 - Bình minh trên phố
```

Nếu mã bài đã có trong danh sách phát, không thêm và trả về:

```plaintext
Bài ZM001 đã có trong danh sách phát.
```

**2.2. Chèn bài mới sau một bài: `insert_after(after_code, code, title)`**

Tìm bài có mã `after_code` (gọi là bài mốc), chèn bài mới vào **ngay sau** bài mốc và trả về:

```plaintext
Đã chèn: ZM004 - Phố cũ (sau ZM001)
```

Sau lệnh trên, danh sách ở ví dụ mục 1 trở thành `ZM001`, `ZM004`, `ZM002`, `ZM003`.

**2.3. Đưa một bài lên đầu: `move_to_top(code)`**

Tìm bài có mã `code`, gỡ node của bài đó khỏi vị trí hiện tại rồi nối **chính node đó** vào đầu danh sách (không tạo node mới), trả về:

```plaintext
Đã đưa lên đầu: ZM002 - Mưa đêm
```

Số bài không đổi sau thao tác này.

**2.4. Hiển thị danh sách phát: `to_lines()`**

Trả về một list các dòng, đánh số từ 1:

```plaintext
1. ZM001 - Bình minh trên phố
2. ZM004 - Phố cũ
3. ZM002 - Mưa đêm
```

Nếu danh sách phát không có bài nào, trả về list chỉ có một dòng:

```plaintext
Danh sách phát đang trống.
```

Sau mọi chức năng, `size` phải bằng đúng số bài, `tail` phải là node cuối và `tail.next` phải là `None`.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Chèn một bài đã có trong danh sách phát**

- Danh sách đã có `ZM003`. Gọi `insert_after("ZM001", "zm003", "Đường về nhà")`, hệ thống không chèn và trả về:

```plaintext
Bài ZM003 đã có trong danh sách phát.
```

- Việc kiểm tra trùng được làm **trước** việc tìm bài mốc: nếu vừa trùng mã vừa không có bài mốc thì vẫn trả về thông báo trùng.

**Bẫy 2 — Không có bài mốc**

- Gọi `insert_after("ZM999", "ZM004", "Phố cũ")`, danh sách giữ nguyên và hệ thống trả về:

```plaintext
Không tìm thấy bài ZM999 để chèn sau.
```

- Danh sách đang trống cũng thuộc trường hợp này; hệ thống không được báo lỗi.

**Bẫy 3 — Chèn sau bài cuối, rồi thêm bài mới**

- Danh sách có `ZM001`, `ZM002`, `ZM003`. Chèn `ZM004` sau `ZM003`, rồi gọi `add_song("ZM005", "Gió qua thềm")`. Nếu `tail` không được dời sang `ZM004` khi chèn, bài `ZM005` sẽ được nối vào sau `ZM003` và làm `ZM004` biến mất. Thứ tự đúng: `ZM001`, `ZM002`, `ZM003`, `ZM004`, `ZM005`.

**Bẫy 4 — Đưa bài cuối lên đầu, rồi thêm bài mới**

- Danh sách có `ZM001`, `ZM002`, `ZM003`. Đưa `ZM003` lên đầu, rồi thêm `ZM004`. Khi gỡ node cuối, `tail` phải lùi về `ZM002` và `tail.next` phải là `None`. Nếu quên, `tail` vẫn chỉ vào `ZM003` (lúc này đang ở đầu) và bài `ZM004` sẽ chen vào giữa, làm mất các bài phía sau. Thứ tự đúng: `ZM003`, `ZM001`, `ZM002`, `ZM004`.

**Bẫy 5 — Bài đã ở đầu, bài không có, danh sách trống**

- Đưa lên đầu đúng bài đang đứng đầu (kể cả khi danh sách chỉ có một bài): danh sách giữ nguyên, trả về:

```plaintext
Bài ZM001 đã ở đầu danh sách phát.
```

- Đưa lên đầu một bài không có, hoặc gọi trên danh sách trống: hệ thống không được báo lỗi mà trả về:

```plaintext
Không tìm thấy bài ZM999 trong danh sách phát.
```

**Kịch bản chạy thử.** Chạy `python sap_xep.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Đã thêm: ZM001 - Bình minh trên phố
Đã thêm: ZM002 - Mưa đêm
Đã thêm: ZM003 - Đường về nhà
Đã chèn: ZM004 - Phố cũ (sau ZM001)
Không tìm thấy bài ZM999 để chèn sau.
Bài ZM004 đã có trong danh sách phát.
Đã chèn: ZM005 - Gió qua thềm (sau ZM003)
Đã thêm: ZM006 - Ngày nắng
1. ZM001 - Bình minh trên phố
2. ZM004 - Phố cũ
3. ZM002 - Mưa đêm
4. ZM003 - Đường về nhà
5. ZM005 - Gió qua thềm
6. ZM006 - Ngày nắng
Bài ZM001 đã ở đầu danh sách phát.
Không tìm thấy bài ZM999 trong danh sách phát.
Đã đưa lên đầu: ZM006 - Ngày nắng
Đã thêm: ZM007 - Đêm thành phố
1. ZM006 - Ngày nắng
2. ZM001 - Bình minh trên phố
3. ZM004 - Phố cũ
4. ZM002 - Mưa đêm
5. ZM003 - Đường về nhà
6. ZM005 - Gió qua thềm
7. ZM007 - Đêm thành phố
Số bài: 7 | bài cuối: ZM007 - Đêm thành phố
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng chức năng, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Đề xuất giải pháp cho `insert_after`: có hai liên kết phải gán (của node mới và của node mốc). Gán theo thứ tự nào? Vẽ hình cho thấy chuyện gì xảy ra nếu gán ngược thứ tự.
- Đề xuất giải pháp cho `move_to_top`: để gỡ một node trong danh sách liên kết đơn, cần giữ node nào khi duyệt? Vẽ hình hai trường hợp: bài cần đưa lên nằm ở giữa, nằm ở cuối; ghi rõ liên kết nào phải sửa.
- Thiết kế thuật toán: viết mã giả hoặc mô tả các bước của `insert_after` và `move_to_top`.
- Chi phí: ghi Big-O thời gian của bốn chức năng, n là số bài. Trong `move_to_top`, phần tìm tốn bao nhiêu, phần gỡ và nối tốn bao nhiêu? So với list Python thì khác ở phần nào?

**(2) Triển khai code**

- Viết thân bốn phương thức trong `sap_xep.py`. Được viết thêm phương thức phụ. Không đổi tên lớp, tên phương thức, tham số.
- Không dùng list Python để lưu danh sách phát (list chỉ dùng cho giá trị trả về của `to_lines`).
- Xử lý đủ 5 bẫy ở mục 3; `python sap_xep.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ sửa liên kết.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex11`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-11 rồi chép các tệp vào kho: `sap_xep.py`, `test_sap_xep.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `sap_xep.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
