# Hiện hoạt động mới nhất trước trên ứng dụng Grab

### 1. Bối cảnh & Vấn đề

![Màn hình "Hoạt động gần đây" phải hiện sự kiện mới nhất trước; với tài khoản có hàng trăm nghìn sự kiện, màn hình mở rất chậm.](minh_hoa.png)

*Màn hình "Hoạt động gần đây" phải hiện sự kiện mới nhất trước; với tài khoản có hàng trăm nghìn sự kiện, màn hình mở rất chậm.*

Màn hình **"Hoạt động gần đây"** của ứng dụng Grab liệt kê các sự kiện của người dùng (đặt xe, thanh toán, đánh giá...). Nhật ký sự kiện được lưu theo thứ tự **từ cũ tới mới**, nhưng màn hình phải hiện **mới nhất trước**:

```plaintext
Nhật ký: ["Đặt GrabBike", "Thanh toán 25.000đ", "Đánh giá 5 sao", "Đặt GrabFood", "Nhận ưu đãi"]
Hiển thị: Nhận ưu đãi, Đặt GrabFood, Đánh giá 5 sao, ...
```

Màn hình chỉ cần vài sự kiện đầu, nhưng thiết kế của nhóm yêu cầu hàm đảo thứ tự trả về **toàn bộ** nhật ký theo thứ tự mới nhất trước, vì cùng kết quả còn được dùng cho trang "Tải lịch sử" (xuất toàn bộ) và cho bộ lọc theo loại sự kiện. Vì vậy chi phí của việc đảo toàn bộ là điều cần so sánh.

Nhật ký còn được dùng cho đối soát nên **không được sửa**; hàm phải trả về list mới. Tài khoản doanh nghiệp có tới **200.000 sự kiện**, màn hình phải mở trong 1 giây. Bản đầu tiên của nhóm đọc từng sự kiện và chèn vào **đầu** list kết quả: đúng thứ tự nhưng chậm dần khi nhật ký dài. Trưởng nhóm yêu cầu bạn đề xuất ít nhất hai giải pháp, đo, so sánh rồi mới chọn.

### 2. Yêu cầu nghiệp vụ

**2.1. `latest_first_v1(events)` và `latest_first_v2(events)`**: mỗi hàm cài một giải pháp, trả về **list mới** các sự kiện theo thứ tự mới nhất trước. Hai hàm cho cùng kết quả nhưng **khác nhau về cách làm**.

**2.2. `recent_message(events, k)`**: dùng giải pháp bạn chọn, hiện k sự kiện mới nhất:

```plaintext
3 hoạt động gần nhất: Nhận ưu đãi, Đặt GrabFood, Đánh giá 5 sao
Chưa có hoạt động nào.
Số sự kiện cần hiện phải lớn hơn 0.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Nhật ký rỗng hoặc một sự kiện.**

**Bẫy 2 — k lớn hơn số sự kiện.** Hiện tất cả, số đếm đúng số sự kiện thật (`5 hoạt động gần nhất: ...`).

**Bẫy 3 — k không dương.** Thông báo lỗi như trên.

**Bẫy 4 — Không sửa nhật ký, luôn trả list mới.** Kể cả khi nhật ký rỗng.

**Bẫy 5 — 200.000 sự kiện.** `recent_message` trả lời trong 1 giây. Lưu ý: giải pháp chậm vẫn phải cho kết quả đúng với dữ liệu nhỏ, vì các test có sẵn so sánh hai giải pháp trên nhiều nhật ký ngẫu nhiên; với dữ liệu lớn chỉ giải pháp bạn chọn được dùng.

**Kịch bản chạy thử.** Chạy `python moi_nhat.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
['Nhận ưu đãi', 'Đặt GrabFood', 'Đánh giá 5 sao', 'Thanh toán 25.000đ', 'Đặt GrabBike']
3 hoạt động gần nhất: Nhận ưu đãi, Đặt GrabFood, Đánh giá 5 sao
5 hoạt động gần nhất: Nhận ưu đãi, Đặt GrabFood, Đánh giá 5 sao, Thanh toán 25.000đ, Đặt GrabBike
Chưa có hoạt động nào.
Số sự kiện cần hiện phải lớn hơn 0.
2 hoạt động gần nhất: SK199999, SK199998 | nhật ký gốc giữ nguyên: SK0
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ ba phần sau:

**(1) Đề xuất và phân tích nhiều giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output của các hàm: kiểu dữ liệu đầu vào, giá trị trả về trong trường hợp thường và trong từng bẫy.
- Đề xuất **ít nhất hai giải pháp** khác nhau về cách làm cho việc đảo thứ tự hiển thị. Với mỗi giải pháp: mô tả ý tưởng trong 2–3 câu, minh họa trên ví dụ ở mục 1, viết mã giả.
- Đo thời gian hai giải pháp bằng `timeit` với n = 25.000, 50.000, 100.000 sự kiện; ghi bảng số đo, phiên bản Python và máy đo. Đếm thêm số phép cộng hoặc số tham chiếu phải dịch bằng một biến đếm.
- So sánh các giải pháp theo bảng 5 tiêu chí: thời gian (Big-O), bộ nhớ phụ (Big-O), kết quả đo, độ dễ đọc và dễ bảo trì, mức phù hợp với bối cảnh của bài.
- Chọn giải pháp dùng cho `recent_message` và nêu lý do dựa trên bảng so sánh. Lựa chọn không có lý do không được tính điểm.

**(2) Chạy tay**

- Với mỗi giải pháp, chạy tay nhật ký `["A", "B", "C", "D"]`: ghi list kết quả sau mỗi bước và số tham chiếu phải dịch.

**(3) Triển khai code**

- Viết thân ba hàm trong `moi_nhat.py`. Không đổi tên hàm, tham số.
- Không sửa list `events`; không dùng `reversed()`, `[::-1]` hay `list.reverse()` trong cả hai giải pháp (để tự đếm được chi phí)
- Xử lý đủ 5 bẫy ở mục 3; `python moi_nhat.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 6 test có sẵn (các test về giải pháp chạy trên cả hai hàm `_v1`, `_v2`).
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích nêu ý tưởng và độ phức tạp ở đầu mỗi hàm.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex14`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-14 rồi chép các tệp vào kho: `moi_nhat.py`, `test_moi_nhat.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `moi_nhat.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
