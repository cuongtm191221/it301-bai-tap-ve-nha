# Bảng điều phối cuốc xe GrabCar nhận lệnh dạng chữ

### 1. Bối cảnh & Vấn đề

![Tổng đài viên gõ lệnh để nhận, giao, hủy cuốc; giờ cao điểm hàng chờ dài và bản cũ dùng pop(0) chậm dần.](minh_hoa.png)

*Tổng đài viên gõ lệnh để nhận, giao, hủy cuốc; giờ cao điểm hàng chờ dài và bản cũ dùng pop(0) chậm dần.*

Tổng đài GrabCar nhận cuốc đặt qua điện thoại (khách lớn tuổi, khách doanh nghiệp). Tổng đài viên dùng một **bảng điều phối** gõ lệnh dạng chữ; cuốc nào vào trước được giao cho tài xế trước. Bạn viết lớp `DispatchQueue` và hàm `handle(queue, line)` xử lý một dòng lệnh:

| Lệnh | Ý nghĩa | Phản hồi |
|---|---|---|
| `ADD <mã>` | thêm cuốc vào cuối hàng | `Đã nhận GC101.` hoặc `GC101 đã có trong hàng.` |
| `NEXT` | giao cuốc đầu hàng | `Giao GC101.` hoặc `Không còn cuốc chờ.` |
| `CANCEL <mã>` | hủy cuốc đang chờ | `Đã hủy GC103.` hoặc `Không có GC999 trong hàng.` |
| `VIEW <k>` | xem tối đa k cuốc đầu hàng | `Hàng chờ: GC102, GC103` hoặc `Hàng chờ: (trống)` |
| `COUNT` | đếm cuốc đang chờ | `Đang chờ 1 cuốc.` |

Tổng đài viên gõ vội: lệnh và mã có thể viết thường, thừa khoảng trắng (mã luôn được đổi sang chữ in hoa). Bản cũ lưu hàng bằng list và lấy cuốc bằng `pop(0)`; ngày mưa, hàng có hàng chục nghìn cuốc và màn hình chậm dần. Lớp `DispatchQueue` đã có sẵn `self._items = []`; bạn tự thêm thuộc tính cần thiết.

Bài này tổng hợp kiến thức cả buổi: chọn cấu trúc cho hàng chờ theo chi phí thao tác, tìm theo giá trị, xóa ở giữa, O(1) khấu hao.

### 2. Yêu cầu nghiệp vụ

**2.1. `DispatchQueue`**: `size()`, `add(code)` (trả `False` nếu mã đang chờ), `next()` (rỗng trả `None`), `cancel(code)`, `view(k)`. `next` phải **O(1) khấu hao**, không dồn cả hàng mỗi lần lấy.

**2.2. `handle(queue, line)`**: trả về đúng dòng phản hồi trong bảng; lỗi cú pháp trả `Cú pháp: ADD <mã cuốc>`, `Cú pháp: CANCEL <mã cuốc>`, `Cú pháp: VIEW <số cuốc lớn hơn 0>`; lệnh lạ trả `Lệnh không hỗ trợ: <lệnh>`; dòng trống trả `Lệnh trống.`

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Gõ vội.** `"  add   gc7 "` là `ADD GC7`.

**Bẫy 2 — Mã trùng.** Thêm mã đang chờ bị từ chối; mã **đã giao** thì được thêm lại (khách đặt cuốc mới).

**Bẫy 3 — Hàng rỗng.** `NEXT`, `VIEW` khi rỗng trả đúng phản hồi, không báo lỗi.

**Bẫy 4 — Lệnh sai.** `ADD`, `CANCEL` thiếu mã; `VIEW 0`, `VIEW -2`, `VIEW ba`; lệnh lạ; dòng trống.

**Bẫy 5 — 200.000 lượt thêm và giao.** Xong trong 2 giây; không dùng `pop(0)`, `insert(0, ...)`.

**Kịch bản chạy thử.** Chạy `python dieu_phoi.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
'ADD gc101'      -> Đã nhận GC101.
'add GC102'      -> Đã nhận GC102.
'ADD GC103'      -> Đã nhận GC103.
'ADD GC101'      -> GC101 đã có trong hàng.
'  next  '       -> Giao GC101.
'VIEW 5'         -> Hàng chờ: GC102, GC103
'CANCEL GC103'   -> Đã hủy GC103.
'CANCEL GC999'   -> Không có GC999 trong hàng.
'COUNT'          -> Đang chờ 1 cuốc.
'NEXT'           -> Giao GC102.
'NEXT'           -> Không còn cuốc chờ.
'VIEW 0'         -> Cú pháp: VIEW <số cuốc lớn hơn 0>
'ADD'            -> Cú pháp: ADD <mã cuốc>
'PRINT'          -> Lệnh không hỗ trợ: PRINT
''               -> Lệnh trống.
Đang chờ 50 cuốc. Hàng chờ: GC199950, GC199951
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, phương thức, trong trường hợp thường và trong từng bẫy.
- Thiết kế cách lưu hàng chờ để `next` không dồn phần tử: cần thêm thông tin gì, khi nào dọn phần đã giao để bộ nhớ không tăng mãi, vì sao cách dọn đó vẫn cho O(1) khấu hao.
- Liệt kê chi phí của `add` (kiểm tra trùng), `cancel`, `view` theo số cuốc đang chờ; vì sao chấp nhận được với tổng đài.
- Vẽ trạng thái bên trong qua 6 lệnh đầu của kịch bản chạy thử.
- Độ phức tạp: ghi Big-O thời gian của năm thao tác và của `handle` theo n (số cuốc đang chờ), cả trường hợp khấu hao của `next`.

**(2) Triển khai code**

- Viết mã trong `dieu_phoi.py`; được thêm thuộc tính, hàm phụ; không đổi tên và tham số đã có trong khung; hàm ghi "Có sẵn" giữ nguyên.
- Không dùng `pop(0)`, `insert(0, ...)`; không dùng `collections` trong `dieu_phoi.py`.
- Xử lý đủ 5 bẫy; `python dieu_phoi.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test có sẵn.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu `collections.deque` của thư viện chuẩn: thao tác nào O(1) ở cả hai đầu, truy cập theo chỉ số ở giữa thì sao.
- Tạo `nghien_cuu.py`: đo bằng `timeit` thời gian lấy hết n phần tử với n = 25.000, 50.000, 100.000 bằng ba cách: `list.pop(0)`, `DispatchQueue` của bạn, `deque.popleft()`. Giải thích kết quả theo Big-O; khi nào bạn chọn `deque` cho hệ thống thật?
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex18`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-18 rồi chép các tệp vào kho: `dieu_phoi.py`, `test_dieu_phoi.py`, `PHAN_TICH.md`.
3. Viết mã trong `dieu_phoi.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần nghiên cứu.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
