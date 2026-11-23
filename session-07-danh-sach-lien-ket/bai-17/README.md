# Trình quản lý danh sách phát bằng dòng lệnh cho nhóm vận hành Zing MP3

### 1. Bối cảnh & Vấn đề

![Nhóm vận hành cần một công cụ gõ lệnh để sửa nhanh danh sách phát; người gõ lệnh thì hay gõ thiếu, gõ sai.](minh_hoa.png)

*Nhóm vận hành cần một công cụ gõ lệnh để sửa nhanh danh sách phát; người gõ lệnh thì hay gõ thiếu, gõ sai.*

Nhóm vận hành nội dung của Zing MP3 mỗi ngày phải chỉnh hàng chục danh sách phát tuyển chọn. Giao diện quản trị trên web chậm, nên nhóm đề nghị một **công cụ dòng lệnh**: gõ một lệnh ngắn, nhận ngay một dòng thông báo.

Ví dụ một phiên làm việc:

```plaintext
> THEM ZM001 | Bình minh trên phố
Đã thêm vào cuối: ZM001 - Bình minh trên phố
> DAU ZM003 | Đường về nhà
Đã thêm vào đầu: ZM003 - Đường về nhà
> XEM
1. ZM003 - Đường về nhà
2. ZM001 - Bình minh trên phố
```

Công cụ gồm hai tầng. Tầng dưới là lớp `Playlist`: một **danh sách liên kết đơn có `head`, `tail`, `size`**, mỗi node giữ chuỗi `"MÃ_BÀI - TÊN_BÀI"`. Tầng trên là hàm `handle(playlist, line)`: nhận một dòng lệnh, kiểm tra, gọi tầng dưới và **trả về** thông báo. Vòng lặp nhập lệnh `main()` (có lệnh `THOAT`) đã có sẵn.

Người vận hành gõ vội: thiếu tên bài, sai mã, thừa khoảng trắng, gõ lệnh không tồn tại. Công cụ **không được dừng vì lỗi** trong bất kỳ trường hợp nào, và dữ liệu sai không được lọt vào danh sách phát. Bạn được giao viết trọn công cụ này.

### 2. Yêu cầu nghiệp vụ

**2.1. Lớp `Playlist`** (khung có sẵn; các phương thức nhận mã và tên **đã chuẩn hóa**)

| Phương thức | Việc cần làm | Trả về |
|---|---|---|
| `add_last(code, title)` | Thêm bài vào cuối, O(1) | không |
| `add_first(code, title)` | Thêm bài vào đầu, O(1) | không |
| `find(code)` | Tìm bài theo mã | Vị trí tính từ 1; `0` nếu không có |
| `value_at(position)` | Lấy bài ở một vị trí | Chuỗi của bài; `None` nếu vị trí không có |
| `remove(code)` | Gỡ node của bài | Chuỗi của bài đã bỏ; `None` nếu không có |
| `to_lines()` | Hiển thị | List các dòng `"1. MÃ - TÊN"`; list rỗng nếu chưa có bài |

**2.2. Hàm `handle(playlist, line)`**

Tên lệnh không phân biệt hoa thường. Mã bài được xóa khoảng trắng hai đầu và chuyển thành chữ hoa; tên bài được xóa khoảng trắng hai đầu.

| Lệnh | Ý nghĩa | Thông báo khi thành công |
|---|---|---|
| `THEM <mã> \| <tên>` | Thêm vào cuối | `Đã thêm vào cuối: ZM001 - Bình minh trên phố` |
| `DAU <mã> \| <tên>` | Thêm vào đầu | `Đã thêm vào đầu: ZM003 - Đường về nhà` |
| `BO <mã>` | Bỏ một bài | `Đã bỏ: ZM002 - Mưa đêm` |
| `TIM <mã>` | Tìm vị trí | `Bài ZM002 - Mưa đêm đang ở vị trí 3.` |
| `XEM` | Hiển thị | Các dòng `1. ...`, `2. ...` nối với nhau bằng ký tự xuống dòng |
| `DEM` | Đếm | `Danh sách phát có 3 bài.` |

Dấu `|` **đầu tiên** của dòng ngăn cách mã và tên. Các trường hợp không thành công:

```plaintext
Bài ZM001 đã có trong danh sách phát.        (THEM, DAU: trùng mã)
Không tìm thấy bài ZM009.                    (BO, TIM: không có bài)
Danh sách phát đang trống.                   (XEM: chưa có bài)
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Lệnh viết thường, thừa khoảng trắng**

- `"  them   zm002 |  Mưa đêm  "` vẫn là một lệnh thêm hợp lệ:

```plaintext
Đã thêm vào cuối: ZM002 - Mưa đêm
```

**Bẫy 2 — Thiếu thông tin**

- Thiếu mã bài (`"THEM"`, `"THEM | Phố cũ"`, `"BO"`) hoặc thiếu tên bài (`"THEM ZM004"`). Thông báo nêu đúng cú pháp của lệnh đang gõ:

```plaintext
Thiếu mã bài. Cú pháp: THEM <mã bài> | <tên bài>
Thiếu tên bài. Cú pháp: DAU <mã bài> | <tên bài>
Thiếu mã bài. Cú pháp: BO <mã bài>
```

**Bẫy 3 — Lệnh không tồn tại, dòng trống**

```plaintext
Lệnh không hợp lệ: PHAT        (gõ "phat zm001")
Chưa nhập lệnh.                (dòng rỗng hoặc chỉ có khoảng trắng)
```

**Bẫy 4 — Mã bài sai định dạng**

- Mã bài hợp lệ gồm đúng 5 ký tự: `ZM` và ba chữ số. Các mã `M4`, `ZM0004`, `ZMABC`, `12345`, `ZM1` đều bị từ chối, ở mọi lệnh có mã:

```plaintext
Mã bài không hợp lệ: M4
```

- Thứ tự kiểm tra của `THEM` và `DAU`: thiếu mã, mã sai định dạng, thiếu tên, trùng mã.

**Bẫy 5 — Bỏ bài cuối rồi thêm, bỏ hết rồi thêm lại**

- Danh sách có `ZM001`, `ZM002`. Gõ `BO ZM002` rồi thêm `ZM003`: kết quả phải là `ZM001`, `ZM003`.
- Bỏ bài duy nhất: `head` và `tail` đều là `None`; thêm bài sau đó vẫn đúng.

**Kịch bản chạy thử.** Chạy `python quan_ly.py demo` phải in ra đúng:

```plaintext
> THEM ZM001 | Bình minh trên phố
Đã thêm vào cuối: ZM001 - Bình minh trên phố
>   them   zm002 |  Mưa đêm  
Đã thêm vào cuối: ZM002 - Mưa đêm
> DAU ZM003 | Đường về nhà
Đã thêm vào đầu: ZM003 - Đường về nhà
> THEM ZM001 | Bình minh trên phố
Bài ZM001 đã có trong danh sách phát.
> THEM ZM004
Thiếu tên bài. Cú pháp: THEM <mã bài> | <tên bài>
> THEM M4 | Phố cũ
Mã bài không hợp lệ: M4
> PHAT ZM001
Lệnh không hợp lệ: PHAT
> 
Chưa nhập lệnh.
> TIM zm002
Bài ZM002 - Mưa đêm đang ở vị trí 3.
> BO ZM002
Đã bỏ: ZM002 - Mưa đêm
> THEM ZM004 | Phố cũ
Đã thêm vào cuối: ZM004 - Phố cũ
> XEM
1. ZM003 - Đường về nhà
2. ZM001 - Bình minh trên phố
3. ZM004 - Phố cũ
> DEM
Danh sách phát có 3 bài.
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng chức năng, trong trường hợp thường và trong từng bẫy.
- `Playlist.remove`: vẽ hình bốn trường hợp (bỏ bài đầu, bài giữa, bài cuối, bài duy nhất) và ghi rõ liên kết phải sửa.
- `handle`: viết mã giả cho trình tự kiểm tra một dòng lệnh; giải thích vì sao việc kiểm tra dữ liệu nhập đặt ở `handle`, không đặt trong `Playlist`.
- Chi phí: Big-O thời gian của sáu phương thức của `Playlist` và của từng lệnh, n là số bài. Lệnh `TIM` của bạn duyệt danh sách mấy lượt?

**(2) Triển khai code**

- Viết mã trong `quan_ly.py`; được thêm phương thức, hàm, lớp phụ; không đổi tên và tham số đã có trong khung.
- Không dùng list, dict, set, deque của Python để lưu các bài (list chỉ dùng cho giá trị trả về khi hiển thị).
- Xử lý đủ 5 bẫy; chương trình in đúng kịch bản chạy thử; `pytest -q` xanh cả 9 test có sẵn. Mã sạch, có chú thích ở những chỗ sửa liên kết.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu `collections.deque` của Python: nó được tổ chức bên trong thế nào, thao tác nào là O(1), thao tác nào là O(n).
- Tạo `nghien_cuu.py`: dùng `timeit` đo thời gian **thêm 20.000 bài vào đầu** với list (`insert(0, ...)`), `deque` (`appendleft`) và `Playlist` của bạn (`add_first`). Ghi bảng số đo, giải thích bằng Big-O, và cho biết với công việc thật bạn chọn `deque` hay lớp tự viết, vì sao.
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex17`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-17 rồi chép các tệp vào kho: `quan_ly.py`, `test_quan_ly.py`, `PHAN_TICH.md`.
3. Viết mã trong `quan_ly.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần đo thời gian.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
