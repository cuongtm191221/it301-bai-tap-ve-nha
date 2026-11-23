# Hàng chờ phát nhạc của Zing MP3

### 1. Bối cảnh & Vấn đề

![Hàng chờ phát: thêm bài ở cuối, lấy bài ở đầu để phát, bỏ một bài bất kỳ, cùng năm bẫy dữ liệu phải xử lý.](minh_hoa.png)

*Hàng chờ phát: thêm bài ở cuối, lấy bài ở đầu để phát, bỏ một bài bất kỳ, cùng năm bẫy dữ liệu phải xử lý.*

Trong ứng dụng nghe nhạc Zing MP3, mỗi người nghe có một **hàng chờ phát**: các bài sẽ lần lượt được phát sau bài hiện tại.

- Mỗi bài trong hàng chờ được lưu dưới dạng chuỗi:

```plaintext
"MÃ_BÀI - TÊN_BÀI"
```

- Ví dụ một hàng chờ có ba bài:

```plaintext
ZM001 - Bình minh trên phố  ->  ZM002 - Mưa đêm  ->  ZM003 - Đường về nhà  ->  None
```

Người nghe liên tục thêm bài vào cuối hàng chờ, ứng dụng liên tục lấy bài ở đầu ra để phát, và người nghe có thể bỏ một bài bất kỳ. Nếu lưu bằng list Python thì mỗi lần lấy bài ở đầu phải dời mọi phần tử còn lại (Session 05). Vì vậy nhóm quyết định lưu hàng chờ bằng **danh sách liên kết đơn có `head`, `tail`, `size`**: `head` là bài sẽ phát tiếp theo, `tail` là bài cuối hàng chờ, `size` là số bài đang chờ.

Bạn được giao viết lớp `PlayQueue` cho hàng chờ này.

### 2. Yêu cầu nghiệp vụ

Lớp `PlayQueue` (khung có sẵn trong `hang_cho.py`) cần bốn chức năng. Mỗi chức năng **trả về** thông báo đúng từng chữ như mô tả; phần giao diện của ứng dụng sẽ hiển thị thông báo đó.

**2.1. Thêm bài vào cuối hàng chờ: `add_song(code, title)`**

Hệ thống cần:

- Xóa khoảng trắng hai đầu của mã bài và tên bài.
- Chuyển mã bài thành chữ hoa.
- Ghép thành chuỗi `"MÃ_BÀI - TÊN_BÀI"` và thêm vào **cuối** hàng chờ trong O(1).
- Trả về:

```plaintext
Đã thêm: ZM001 - Bình minh trên phố
```

**2.2. Phát bài tiếp theo: `play_next()`**

Hệ thống cần lấy bài ở **đầu** hàng chờ ra khỏi hàng chờ trong O(1) và trả về:

```plaintext
Đang phát: ZM001 - Bình minh trên phố
```

**2.3. Bỏ một bài khỏi hàng chờ: `remove_song(code)`**

Người nghe nhập mã bài cần bỏ. Hệ thống chuẩn hóa mã (xóa khoảng trắng, chữ hoa), tìm bài có mã đó, gỡ node khỏi hàng chờ và trả về:

```plaintext
Đã bỏ: ZM003 - Đường về nhà
```

**2.4. Hiển thị hàng chờ: `to_lines()`**

Trả về một list các dòng, đánh số từ 1 theo thứ tự sẽ phát:

```plaintext
1. ZM001 - Bình minh trên phố
2. ZM002 - Mưa đêm
3. ZM004 - Phố cũ
```

Nếu hàng chờ không có bài nào, trả về list chỉ có một dòng:

```plaintext
Hàng chờ đang trống.
```

Sau mọi chức năng, `size` phải bằng đúng số bài đang chờ, `tail` phải là node cuối (hoặc `None` khi hàng chờ rỗng).

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Mã bài hoặc tên bài bị thừa khoảng trắng, mã viết thường**

- Gọi `add_song("  zm002 ", " Mưa đêm ")`, hệ thống vẫn phải lưu và trả về đúng chuẩn:

```plaintext
Đã thêm: ZM002 - Mưa đêm
```

**Bẫy 2 — Thêm bài đã có trong hàng chờ**

- Hàng chờ đã có `ZM001`. Gọi `add_song("zm001", "Bình minh trên phố")`, hệ thống không thêm và trả về:

```plaintext
Bài ZM001 đã có trong hàng chờ.
```

**Bẫy 3 — Phát khi hàng chờ đã hết bài**

- Hệ thống không được báo lỗi mà trả về:

```plaintext
Hàng chờ đang trống, không có bài để phát.
```

- Sau khi phát bài cuối cùng, `head` và `tail` đều phải là `None`.

**Bẫy 4 — Bỏ một bài không có trong hàng chờ**

- Gọi `remove_song("ZM999")`, hàng chờ giữ nguyên và hệ thống trả về:

```plaintext
Không tìm thấy bài ZM999 trong hàng chờ.
```

**Bẫy 5 — Bỏ bài đang đứng cuối, rồi thêm bài mới**

- Hàng chờ có `ZM001`, `ZM002`, `ZM003`. Bỏ `ZM003` rồi thêm `ZM004`. Nếu `tail` không lùi về `ZM002` khi bỏ bài cuối, bài `ZM004` sẽ bị nối vào một node đã bị gỡ và biến mất khỏi hàng chờ. Kết quả hiển thị đúng:

```plaintext
1. ZM001 - Bình minh trên phố
2. ZM002 - Mưa đêm
3. ZM004 - Phố cũ
```

**Kịch bản chạy thử.** Chạy `python hang_cho.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Đã thêm: ZM001 - Bình minh trên phố
Đã thêm: ZM002 - Mưa đêm
Đã thêm: ZM003 - Đường về nhà
Bài ZM001 đã có trong hàng chờ.
Không tìm thấy bài ZM999 trong hàng chờ.
Đã bỏ: ZM003 - Đường về nhà
Đã thêm: ZM004 - Phố cũ
1. ZM001 - Bình minh trên phố
2. ZM002 - Mưa đêm
3. ZM004 - Phố cũ
Số bài đang chờ: 3
Đang phát: ZM001 - Bình minh trên phố
Đang phát: ZM002 - Mưa đêm
Đang phát: ZM004 - Phố cũ
Hàng chờ đang trống, không có bài để phát.
Hàng chờ đang trống.
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng chức năng, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Đề xuất giải pháp: với `remove_song`, cần theo dõi những node nào khi duyệt? Khi nào phải sửa `head`, khi nào phải sửa `tail`? Vẽ hình cho ba trường hợp: bỏ bài đầu, bỏ bài giữa, bỏ bài cuối.
- Thiết kế thuật toán: viết mã giả hoặc mô tả các bước của `add_song` và `remove_song`.
- Chi phí: ghi Big-O thời gian của bốn chức năng, n là số bài đang chờ.

**(2) Triển khai code**

- Viết thân bốn phương thức trong `hang_cho.py`. Không đổi tên lớp, tên phương thức, tham số.
- Không dùng list Python để lưu hàng chờ (list chỉ dùng cho giá trị trả về của `to_lines`).
- Xử lý đủ 5 bẫy ở mục 3; `python hang_cho.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 7 test.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ nối lại liên kết.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex09`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-09 rồi chép các tệp vào kho: `hang_cho.py`, `test_hang_cho.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `hang_cho.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
