# Đối soát đơn hàng giữa Shopee và đơn vị vận chuyển

### 1. Bối cảnh & Vấn đề

![Cuối ngày sale, hai bên phải xác nhận cùng một danh sách 50.000 đơn trước 23 giờ để thanh toán phí giao hàng.](minh_hoa.png)

*Cuối ngày sale, hai bên phải xác nhận cùng một danh sách 50.000 đơn trước 23 giờ để thanh toán phí giao hàng.*

Cuối mỗi ngày, Shopee **đối soát** với đơn vị vận chuyển: hai bên gửi cho nhau danh sách mã các đơn đã giao trong ngày. Nếu hai danh sách **khớp**, phí giao hàng được thanh toán tự động; nếu **lệch**, kế toán phải kiểm tra thủ công.

Hai danh sách thường **không cùng thứ tự** (mỗi bên xếp theo giờ quét của mình), và danh sách của đơn vị vận chuyển được nhân viên bưu cục nhập tay nên có mã viết thường hoặc thừa khoảng trắng. Hàm `normalize_code` có sẵn để chuẩn hóa một mã.

Hai danh sách **khớp** khi có cùng các mã sau khi chuẩn hóa, **mỗi mã xuất hiện cùng số lần** ở hai bên, không kể thứ tự. Một đơn có thể được giao hai lần (giao lại sau khi khách vắng nhà) nên một mã có thể xuất hiện nhiều lần.

Ngày sale, mỗi bên có tới **50.000 đơn**, và kết quả đối soát phải có trong **3 giây**. Hai danh sách còn được dùng để lưu trữ nên **không được sửa**. Trưởng nhóm yêu cầu bạn đề xuất ít nhất hai giải pháp, đo, so sánh rồi mới chọn.

### 2. Yêu cầu nghiệp vụ

Tệp `doi_soat.py` có sẵn hàm `normalize_code`. Bạn viết ba hàm.

**2.1. Hai hàm đối soát: `same_orders_v1(ours, carrier)` và `same_orders_v2(ours, carrier)`**

Mỗi hàm cài một giải pháp của bạn, trả về `True` nếu hai list khớp, ngược lại `False`. Hai hàm cho cùng kết quả với mọi dữ liệu nhưng **khác nhau về cách làm**.

**2.2. Thông báo: `reconcile_message(ours, carrier)`**

Dùng giải pháp bạn chọn, trả về một trong các thông báo:

```plaintext
Khớp 5 đơn.
Lệch: số đơn khác nhau (5 và 4).
Lệch: có mã đơn không khớp.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khác thứ tự, khác cách viết**

- `["DH9001", "DH9002", ...]` và `["DH9003", " dh9001", ...]` vẫn khớp nếu cùng các mã.

**Bẫy 2 — Cùng các mã nhưng khác số lần**

- `["DH9001", "DH9001", "DH9002"]` và `["DH9001", "DH9002", "DH9002"]` **không** khớp, dù cả hai đều chỉ chứa `DH9001` và `DH9002`. Cách làm "mỗi mã bên này đều có ở bên kia" sẽ kết luận sai.

**Bẫy 3 — Khác số đơn**

- Kiểm tra số đơn trước: khác nhau thì lệch ngay, không cần so từng mã. Thông báo ghi rõ số đơn hai bên.

**Bẫy 4 — Hai bên chưa có đơn**

- Hai hàm đối soát trả về `True`; thông báo:

```plaintext
Chưa có đơn để đối soát.
```

**Bẫy 5 — 50.000 đơn mỗi bên, không sửa dữ liệu**

- `reconcile_message` trả lời trong 3 giây với 50.000 đơn mỗi bên; sau khi đối soát, hai list vẫn giữ nguyên thứ tự và cách viết.

**Kịch bản chạy thử.** Chạy `python doi_soat.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Ngày 11/11: True True | Khớp 5 đơn.
Thiếu một đơn: Lệch: số đơn khác nhau (5 và 4).
Trùng số lần khác nhau: False False
Sai một mã: Lệch: có mã đơn không khớp.
Hai bên chưa có đơn: Chưa có đơn để đối soát.
List của đơn vị vận chuyển giữ nguyên: ['DH9003', ' dh9001', 'DH9005', 'DH9002', 'DH9004 ']
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ ba phần sau:

**(1) Đề xuất và phân tích nhiều giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output của các hàm: kiểu dữ liệu đầu vào, giá trị trả về trong trường hợp thường và trong từng bẫy.
- Đề xuất **ít nhất hai giải pháp** khác nhau về cách làm cho việc đối soát hai danh sách. Với mỗi giải pháp: mô tả ý tưởng trong 2–3 câu, minh họa trên ví dụ ở mục 1, viết mã giả.
- Đo thời gian hai giải pháp bằng `timeit` (như bài đọc Lesson 03, mục 3.3) với n = 1.000, 2.000 và 4.000 đơn mỗi bên, hai bên khớp nhưng khác thứ tự (trường hợp xấu nhất); ghi bảng số đo, phiên bản Python và máy đo.
- So sánh các giải pháp theo bảng 5 tiêu chí: thời gian (Big-O), bộ nhớ phụ (Big-O), kết quả đo, độ dễ đọc và dễ bảo trì, mức phù hợp với bối cảnh của bài.
- Chọn giải pháp dùng cho `reconcile_message` và nêu lý do dựa trên bảng so sánh. Lựa chọn không có lý do không được tính điểm.

**(2) Chạy tay**

- Với mỗi giải pháp, chạy tay trên hai list ở bẫy 2: ghi các bước cho tới khi hàm trả về `False`.

**(3) Triển khai code**

- Viết thân ba hàm trong `doi_soat.py`. Không đổi tên hàm, tham số.
- Không dùng `set`, `dict` hay `collections` (sẽ học ở buổi bảng băm); không sửa hai list đầu vào.
- Xử lý đủ 5 bẫy ở mục 3; `python doi_soat.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 7 mục (mỗi mục về hai giải pháp chạy trên cả hai hàm).
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích nêu ý tưởng và độ phức tạp ở đầu mỗi hàm.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session01_Ex16`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-01-tong-quan-do-phuc-tap/bai-16 rồi chép các tệp vào kho: `doi_soat.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `doi_soat.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
