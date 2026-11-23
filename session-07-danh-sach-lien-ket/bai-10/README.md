# Lịch sử "Nghe gần đây" của Zing MP3

### 1. Bối cảnh & Vấn đề

![Mục Nghe gần đây: bài vừa nghe lên đầu, nghe lại không được trùng, quá giới hạn thì bỏ bài cũ nhất.](minh_hoa.png)

*Mục Nghe gần đây: bài vừa nghe lên đầu, nghe lại không được trùng, quá giới hạn thì bỏ bài cũ nhất.*

Trong ứng dụng nghe nhạc Zing MP3, màn hình chính có mục **"Nghe gần đây"**: các bài người nghe vừa mở, **bài mới nghe nhất đứng trên cùng**.

- Mỗi bài trong lịch sử được lưu dưới dạng chuỗi:

```plaintext
"MÃ_BÀI - TÊN_BÀI"
```

- Ví dụ người nghe lần lượt mở `ZM001`, `ZM002`, `ZM003` thì lịch sử là:

```plaintext
head                                                              tail
ZM003 - Đường về nhà  <->  ZM002 - Mưa đêm  <->  ZM001 - Bình minh trên phố
```

Mục này có ba đặc điểm nghiệp vụ. Bài vừa nghe luôn được đưa vào **đầu** lịch sử. Lịch sử chỉ giữ một số bài nhất định (`limit`), vượt quá thì bỏ bài **cũ nhất**, tức bài ở **cuối**. Và khi người nghe mở lại một bài đã có trong lịch sử, bài đó phải được **nhấc từ giữa lên đầu**, không được xuất hiện hai lần.

Với danh sách liên kết đơn, bỏ bài ở cuối phải duyệt từ đầu để tìm node đứng trước `tail`. Vì vậy nhóm quyết định lưu lịch sử bằng **danh sách liên kết đôi có `head`, `tail`, `size`**: mỗi node có `prev` và `next`, nên gỡ một node bất kỳ chỉ cần sửa liên kết của hai node kề nó.

Bạn được giao viết lớp `RecentHistory` cho mục này.

### 2. Yêu cầu nghiệp vụ

Lớp `RecentHistory` (khung có sẵn trong `lich_su.py`, lớp `Node` đã có `value`, `prev`, `next`) cần bốn chức năng. Mỗi chức năng **trả về** thông báo đúng từng chữ như mô tả.

**2.1. Ghi nhận một lượt nghe: `record(code, title)`**

Hệ thống cần:

- Xóa khoảng trắng hai đầu của mã bài và tên bài, chuyển mã bài thành chữ hoa.
- Nếu bài chưa có trong lịch sử: tạo node mới với chuỗi `"MÃ_BÀI - TÊN_BÀI"`, đưa vào **đầu** lịch sử trong O(1) và trả về:

```plaintext
Đã ghi: ZM001 - Bình minh trên phố
```

- Các trường hợp còn lại: xem bẫy 2, 3, 4 ở mục 3.

**2.2. Xóa một bài khỏi lịch sử: `remove_song(code)`**

Người nghe không muốn một bài hiện trong lịch sử. Hệ thống chuẩn hóa mã, tìm node của bài đó, gỡ node và trả về:

```plaintext
Đã xóa khỏi lịch sử: ZM002 - Mưa đêm
```

**2.3. Hiển thị từ mới đến cũ: `to_lines()`**

Đi từ `head` theo `next`, trả về list các dòng đánh số từ 1:

```plaintext
1. ZM003 - Đường về nhà
2. ZM002 - Mưa đêm
3. ZM001 - Bình minh trên phố
```

**2.4. Hiển thị từ cũ đến mới: `to_lines_oldest_first()`**

Đi từ `tail` theo `prev`, trả về list các dòng đánh số từ 1:

```plaintext
1. ZM001 - Bình minh trên phố
2. ZM002 - Mưa đêm
3. ZM003 - Đường về nhà
```

Nếu lịch sử chưa có bài nào, cả hai chức năng hiển thị trả về list chỉ có một dòng:

```plaintext
Chưa có lịch sử nghe.
```

Sau mọi chức năng: `size` bằng số bài trong lịch sử; `head.prev` và `tail.next` là `None`; đi xuôi theo `next` và đi ngược theo `prev` gặp đúng các node đó.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Mã bài hoặc tên bài bị thừa khoảng trắng, mã viết thường**

- Gọi `record("  zm002 ", " Mưa đêm ")`, hệ thống vẫn phải lưu và trả về đúng chuẩn:

```plaintext
Đã ghi: ZM002 - Mưa đêm
```

**Bẫy 2 — Nghe lại một bài đã có trong lịch sử**

- Lịch sử đang là `ZM003`, `ZM002`, `ZM001`. Gọi `record("zm001", "Bình minh trên phố")`. Hệ thống **không tạo node mới** mà gỡ node của `ZM001` khỏi vị trí cũ rồi đưa chính node đó lên đầu; `size` vẫn là 3. Trả về:

```plaintext
Đã đưa lên đầu: ZM001 - Bình minh trên phố
```

- Ở ví dụ này `ZM001` đang là `tail`, nên `tail` phải lùi về `ZM002`.

**Bẫy 3 — Nghe lại đúng bài đang đứng đầu lịch sử**

- Lịch sử giữ nguyên, hệ thống trả về:

```plaintext
Bài ZM003 đang ở đầu lịch sử.
```

**Bẫy 4 — Lịch sử vượt quá giới hạn**

- Lịch sử có `limit` là 3 và đang giữ `ZM003`, `ZM002`, `ZM001`. Gọi `record("ZM004", "Phố cũ")`: bài mới vào đầu, bài cũ nhất `ZM001` bị bỏ khỏi cuối trong O(1), `tail` lùi về `ZM002`. Trả về:

```plaintext
Đã ghi: ZM004 - Phố cũ (bỏ bài cũ nhất: ZM001 - Bình minh trên phố)
```

**Bẫy 5 — Xóa bài không có, xóa bài ở hai đầu, xóa bài duy nhất**

- Gọi `remove_song("ZM999")`, lịch sử giữ nguyên và hệ thống trả về:

```plaintext
Không tìm thấy bài ZM999 trong lịch sử.
```

- Xóa bài đang đứng đầu thì `head` phải dời và `head.prev` phải là `None`. Xóa bài đang đứng cuối thì `tail` phải lùi và `tail.next` phải là `None`. Xóa bài duy nhất thì `head` và `tail` đều là `None`; sau đó ghi một lượt nghe mới vẫn phải hoạt động.

**Kịch bản chạy thử.** Chạy `python lich_su.py` (đoạn chạy thử có sẵn ở cuối tệp, lịch sử có `limit` là 4) phải in ra đúng:

```plaintext
Đã ghi: ZM001 - Bình minh trên phố
Đã ghi: ZM002 - Mưa đêm
Đã ghi: ZM003 - Đường về nhà
Đã đưa lên đầu: ZM001 - Bình minh trên phố
Bài ZM001 đang ở đầu lịch sử.
Đã ghi: ZM004 - Phố cũ
Đã ghi: ZM005 - Gió qua thềm (bỏ bài cũ nhất: ZM002 - Mưa đêm)
1. ZM005 - Gió qua thềm
2. ZM004 - Phố cũ
3. ZM001 - Bình minh trên phố
4. ZM003 - Đường về nhà
Từ cũ đến mới:
1. ZM003 - Đường về nhà
2. ZM001 - Bình minh trên phố
3. ZM004 - Phố cũ
4. ZM005 - Gió qua thềm
Số bài trong lịch sử: 4
Không tìm thấy bài ZM999 trong lịch sử.
Đã xóa khỏi lịch sử: ZM003 - Đường về nhà
Đã xóa khỏi lịch sử: ZM005 - Gió qua thềm
1. ZM004 - Phố cũ
2. ZM001 - Bình minh trên phố
Bài cũ nhất: ZM001 - Bình minh trên phố
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng chức năng, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Đề xuất giải pháp: `record` và `remove_song` đều phải gỡ một node, `record` có hai chỗ phải đưa một node vào đầu. Bạn tổ chức mã thế nào để không viết lặp các đoạn sửa liên kết? Vẽ hình bốn trường hợp gỡ node: node ở đầu, ở giữa, ở cuối, node duy nhất; ghi rõ những liên kết nào (`prev`, `next`, `head`, `tail`) phải sửa trong từng trường hợp.
- Thiết kế thuật toán: viết mã giả hoặc mô tả các bước của `record`, đủ bốn nhánh (bài mới, nghe lại, đang ở đầu, vượt giới hạn).
- Chi phí: ghi Big-O thời gian của bốn chức năng, n là số bài trong lịch sử. Trong `record`, bước nào là O(n), bước nào là O(1)?

**(2) Triển khai code**

- Viết thân bốn phương thức trong `lich_su.py`. Được viết thêm phương thức phụ. Không đổi tên lớp, tên phương thức, tham số.
- Không dùng list Python để lưu lịch sử (list chỉ dùng cho giá trị trả về của hai chức năng hiển thị).
- Xử lý đủ 5 bẫy ở mục 3; `python lich_su.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ sửa liên kết.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex10`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-10 rồi chép các tệp vào kho: `lich_su.py`, `test_lich_su.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `lich_su.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
