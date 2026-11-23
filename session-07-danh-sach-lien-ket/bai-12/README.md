# Bỏ mọi bài của một ca sĩ khỏi danh sách phát Zing MP3

### 1. Bối cảnh & Vấn đề

![Người nghe bấm "Không phát ca sĩ này": mọi bài của ca sĩ đó phải rời khỏi danh sách phát.](minh_hoa.png)

*Người nghe bấm "Không phát ca sĩ này": mọi bài của ca sĩ đó phải rời khỏi danh sách phát.*

Trong ứng dụng nghe nhạc Zing MP3, khi đang nghe một danh sách phát, người nghe có thể bấm **"Không phát ca sĩ này"**. Hệ thống phải bỏ **mọi bài** của ca sĩ đó khỏi danh sách phát, các bài còn lại giữ nguyên thứ tự.

- Mỗi bài trong danh sách phát được lưu dưới dạng chuỗi:

```plaintext
"MÃ_BÀI - TÊN_BÀI - CA_SĨ"
```

- Ví dụ một danh sách phát có sáu bài (tên ca sĩ trong bài là tên giả định):

```plaintext
ZM001 - Bình minh trên phố - Hoàng Lan
ZM002 - Mưa đêm - Hoàng Lan
ZM003 - Đường về nhà - Minh Khôi
ZM004 - Phố cũ - Hoàng Lan
ZM005 - Gió qua thềm - Thu An
ZM006 - Ngày nắng - Thu An
```

Danh sách phát được lưu bằng **danh sách liên kết đơn có `head`, `tail`, `size`**. Bỏ một bài thì các buổi học đã làm; khó ở đây là bỏ **nhiều bài trong một lần duyệt**: các bài của cùng một ca sĩ có thể đứng liền nhau, đứng ngay đầu, đứng ở cuối, hoặc chiếm cả danh sách.

Bạn được giao viết lớp `ArtistPlaylist` cho tính năng này.

### 2. Yêu cầu nghiệp vụ

Lớp `ArtistPlaylist` (khung có sẵn trong `loc_ca_si.py`) cần bốn chức năng.

**2.1. Thêm bài vào cuối: `add_song(code, title, artist)`**

Hệ thống cần:

- Xóa khoảng trắng hai đầu của mã bài, tên bài, tên ca sĩ.
- Chuyển mã bài thành chữ hoa; chuyển tên ca sĩ về dạng viết hoa chữ cái đầu mỗi từ (phương thức `title()` của chuỗi).
- Ghép thành chuỗi `"MÃ_BÀI - TÊN_BÀI - CA_SĨ"`, thêm vào **cuối** danh sách phát trong O(1) và trả về:

```plaintext
Đã thêm: ZM001 - Bình minh trên phố - Hoàng Lan
```

**2.2. Đếm số bài của một ca sĩ: `count_by_artist(artist)`**

Chuẩn hóa tên ca sĩ như mục 2.1 rồi trả về **một số nguyên**: số bài của ca sĩ đó trong danh sách phát. Với ví dụ ở mục 1, `count_by_artist("Hoàng Lan")` trả về `3`. Ca sĩ không có bài nào, hoặc danh sách trống, trả về `0`.

Gợi ý về dữ liệu: tên ca sĩ là phần thứ ba khi tách chuỗi của node theo `" - "`.

**2.3. Bỏ mọi bài của một ca sĩ: `remove_by_artist(artist)`**

Chuẩn hóa tên ca sĩ, gỡ mọi node có ca sĩ đó **trong một lần duyệt** (O(n)), giữ nguyên thứ tự các bài còn lại và trả về:

```plaintext
Đã bỏ 3 bài của Hoàng Lan.
```

**2.4. Hiển thị danh sách phát: `to_lines()`**

Trả về một list các dòng, đánh số từ 1:

```plaintext
1. ZM003 - Đường về nhà - Minh Khôi
2. ZM005 - Gió qua thềm - Thu An
3. ZM006 - Ngày nắng - Thu An
```

Nếu danh sách phát không có bài nào, trả về list chỉ có một dòng:

```plaintext
Danh sách phát đang trống.
```

Sau mọi chức năng, `size` phải bằng đúng số bài, `tail` phải là node cuối (hoặc `None` khi danh sách rỗng) và `tail.next` phải là `None`.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Tên ca sĩ viết không thống nhất**

- Gọi `add_song("  zm002 ", " Mưa đêm ", "  hoàng lan ")`, hệ thống vẫn phải lưu và trả về đúng chuẩn:

```plaintext
Đã thêm: ZM002 - Mưa đêm - Hoàng Lan
```

- Khi đếm và khi bỏ, `" HOÀNG LAN "`, `"hoàng lan"` và `"Hoàng Lan"` đều là cùng một ca sĩ. Thông báo trả về luôn dùng tên đã chuẩn hóa.

**Bẫy 2 — Nhiều bài liền nhau, kể cả ở đầu danh sách**

- Với ví dụ ở mục 1, hai bài đầu `ZM001`, `ZM002` đều của Hoàng Lan. Sau khi bỏ, `head` phải là `ZM003`. Lỗi thường gặp: vừa gỡ một node xong lại bước tiếp sang node sau, nên bài đứng liền sau bài vừa bỏ không được kiểm tra và còn sót lại.

**Bẫy 3 — Bài bị bỏ nằm ở cuối, rồi thêm bài mới**

- Với ví dụ ở mục 1, bỏ các bài của Thu An (`ZM005`, `ZM006`) thì `tail` phải lùi về `ZM004`. Sau đó gọi `add_song("ZM007", "Đêm thành phố", "Minh Khôi")`, bài `ZM007` phải nằm ngay sau `ZM004`.

**Bẫy 4 — Mọi bài trong danh sách đều của ca sĩ đó**

- Danh sách chỉ có hai bài của Hoàng Lan. Sau khi bỏ, hệ thống không được báo lỗi; `head` và `tail` đều là `None`, `size` là 0, và thêm bài mới sau đó vẫn hoạt động. Hệ thống trả về:

```plaintext
Đã bỏ 2 bài của Hoàng Lan.
```

**Bẫy 5 — Ca sĩ không có bài nào**

- Gọi `remove_by_artist("Lê Vy")` (kể cả khi danh sách trống), danh sách giữ nguyên và hệ thống trả về:

```plaintext
Không có bài nào của Lê Vy.
```

**Kịch bản chạy thử.** Chạy `python loc_ca_si.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Đã thêm: ZM001 - Bình minh trên phố - Hoàng Lan
Đã thêm: ZM002 - Mưa đêm - Hoàng Lan
Đã thêm: ZM003 - Đường về nhà - Minh Khôi
Đã thêm: ZM004 - Phố cũ - Hoàng Lan
Đã thêm: ZM005 - Gió qua thềm - Thu An
Đã thêm: ZM006 - Ngày nắng - Thu An
Số bài của Hoàng Lan: 3
Đã bỏ 3 bài của Hoàng Lan.
1. ZM003 - Đường về nhà - Minh Khôi
2. ZM005 - Gió qua thềm - Thu An
3. ZM006 - Ngày nắng - Thu An
Không có bài nào của Hoàng Lan.
Đã bỏ 2 bài của Thu An.
Số bài: 1 | bài cuối: ZM003 - Đường về nhà - Minh Khôi
Đã thêm: ZM007 - Đêm thành phố - Minh Khôi
Đã bỏ 2 bài của Minh Khôi.
Danh sách phát đang trống.
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng chức năng, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Đề xuất giải pháp cho `remove_by_artist`: khi duyệt cần giữ node nào? Sau khi gỡ một node, con trỏ duyệt có bước tiếp không, vì sao? Các bài ở đầu danh sách được xử lý thế nào? `tail` được xác định lại ở đâu?
- Chạy tay giải pháp của bạn trên ví dụ ở mục 1 khi bỏ các bài của Hoàng Lan: lập bảng ghi lại, sau từng bước, con trỏ duyệt đang ở node nào và danh sách đang ra sao.
- Thiết kế thuật toán: viết mã giả hoặc mô tả các bước của `remove_by_artist`.
- Chi phí: ghi Big-O thời gian của bốn chức năng, n là số bài. Nếu gọi nhiều lần thao tác "tìm và bỏ một bài" thì tốn bao nhiêu trong trường hợp xấu nhất?

**(2) Triển khai code**

- Viết thân bốn phương thức trong `loc_ca_si.py`. Được viết thêm phương thức phụ. Không đổi tên lớp, tên phương thức, tham số.
- Không dùng list Python để lưu danh sách phát, không tạo danh sách liên kết mới để chép các bài được giữ lại: phải gỡ node ngay trên danh sách đang có.
- Xử lý đủ 5 bẫy ở mục 3; `python loc_ca_si.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ sửa liên kết.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex12`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-12 rồi chép các tệp vào kho: `loc_ca_si.py`, `test_loc_ca_si.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `loc_ca_si.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
