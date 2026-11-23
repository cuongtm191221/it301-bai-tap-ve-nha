# Phân loại độ phức tạp của báo cáo từ số đo cho nhóm hiệu năng Shopee

### 1. Bối cảnh & Vấn đề

![Nhóm hiệu năng có bảng số đo của hàng trăm báo cáo và cần biết báo cáo nào đang tăng theo n² trước đợt sale.](minh_hoa.png)

*Nhóm hiệu năng có bảng số đo của hàng trăm báo cáo và cần biết báo cáo nào đang tăng theo n² trước đợt sale.*

Trước mỗi đợt sale lớn, **nhóm hiệu năng** của Shopee chạy thử hàng trăm báo cáo với n = 1.000, 2.000, 4.000, 8.000 đơn và ghi **số bước** của từng lần chạy. Từ số đo, nhóm cần biết mỗi báo cáo thuộc lớp độ phức tạp nào để loại các báo cáo O(n²) khỏi lịch chạy ngày sale. Làm tay với hàng trăm báo cáo là không thể, nên bạn được giao viết công cụ tự phân loại.

Mỗi báo cáo có một list số đo, mỗi số đo là một bộ `(n, số bước)`:

```plaintext
[(1000, 1002), (2000, 2002), (4000, 4002), (8000, 8002)]
```

Ý tưởng dựa trên Lesson 02 và 03: khi **n tăng gấp đôi**, số bước của O(n) tăng khoảng **2 lần**, của O(n²) tăng khoảng **4 lần**, của O(1) không đổi, của O(log n) chỉ thêm một chút. Công cụ tính **tỉ lệ** số bước giữa hai lần đo liên tiếp rồi so với bảng quy tắc.

### 2. Yêu cầu nghiệp vụ

**2.1. `check_measurements(measurements)`**: kiểm tra số đo và trả về một **bản sao** đã xếp theo n tăng dần (số đo có thể được nhập không theo thứ tự). Số đo không hợp lệ thì báo `ValueError` với một trong ba thông báo ở mục 3.

**2.2. `growth_ratios(measurements)`**: trả về list tỉ lệ `số bước lần sau / số bước lần trước`, làm tròn 2 chữ số, theo n tăng dần.

**2.3. `classify(measurements)`**: áp dụng bảng quy tắc theo đúng thứ tự từ trên xuống, gặp dòng nào đúng thì dừng (r là trung bình cộng các tỉ lệ):

| Thứ tự | Điều kiện | Kết quả |
|---|---|---|
| 1 | Mọi lần đo có cùng số bước | `O(1)` |
| 2 | Có tỉ lệ nhỏ hơn 1 (số bước giảm) | `Không xác định` |
| 3 | r < 1,5 | `O(log n)` |
| 4 | r < 2,15 | `O(n)` |
| 5 | r < 3 | `O(n log n)` |
| 6 | r < 5 | `O(n^2)` |
| 7 | Còn lại | `Không xác định` |

**2.4. `report_line(name, measurements)`**: trả về một dòng của bảng hiệu năng, r in 2 chữ số thập phân:

```plaintext
tong_doanh_thu: O(n) (tỉ lệ trung bình 2.00)
thieu_so_do: số đo không hợp lệ - Cần ít nhất 3 lần đo.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Quá ít lần đo:** ít hơn 3 lần đo thì báo `Cần ít nhất 3 lần đo.`

**Bẫy 2 — n không tăng gấp đôi:** ví dụ 1.000, 3.000, 9.000: báo `Các lần đo phải có n tăng gấp đôi.`

**Bẫy 3 — Số bước không dương:** báo `Số bước phải lớn hơn 0.` (tránh chia cho 0).

**Bẫy 4 — Số đo không theo thứ tự:** `[(4000, ...), (1000, ...), (2000, ...)]` vẫn phân loại đúng, và list số đo của người gọi **không bị đổi thứ tự**.

**Bẫy 5 — Số bước giảm hoặc tăng quá nhanh:** cả hai đều ra `Không xác định`, không được xếp nhầm vào lớp nào.

**Kịch bản chạy thử.** Chạy `python do_tang.py` (đoạn chạy thử có sẵn ở cuối tệp, gồm số đo của 8 báo cáo) phải in ra đúng:

```plaintext
in_tieu_de: O(1) (tỉ lệ trung bình 1.00)
tim_don: O(log n) (tỉ lệ trung bình 1.09)
tong_doanh_thu: O(n) (tỉ lệ trung bình 2.00)
xep_hang: O(n log n) (tỉ lệ trung bình 2.18)
don_trung: O(n^2) (tỉ lệ trung bình 4.00)
do_nham: số đo không hợp lệ - Các lần đo phải có n tăng gấp đôi.
thieu_so_do: số đo không hợp lệ - Cần ít nhất 3 lần đo.
giam_dan: Không xác định (tỉ lệ trung bình 0.58)
Tỉ lệ của don_trung: [4.0, 4.0]
Số đo don_trung giữ nguyên thứ tự: (4000, 7998000)
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, trong trường hợp thường và trong từng bẫy.
- Với mỗi lớp độ phức tạp, tính tỉ lệ số bước khi n tăng từ 1.000 lên 2.000 (dùng số bước ước lượng của Lesson 02) và giải thích vì sao các ngưỡng 1,5; 2,15; 3; 5 trong bảng quy tắc tách được các lớp.
- Vì sao `check_measurements` phải trả về bản sao chứ không sắp xếp list được truyền vào?
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của bốn hàm theo m (số lần đo).

**(2) Triển khai code**

- Viết mã trong `do_tang.py`; được thêm hàm phụ; không đổi tên và tham số đã có trong khung.
- Dùng lại `check_measurements` và `growth_ratios` trong các hàm sau, không viết lặp phần kiểm tra.
- Xử lý đủ 5 bẫy; `python do_tang.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 5 mục.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu `timeit` và `time.perf_counter`: khác nhau thế nào, vì sao khi đo nên chạy lặp nhiều lần và lấy **thời gian nhỏ nhất**.
- Tạo `nghien_cuu.py`: đo **thời gian** (thay cho số bước) của hai hàm bạn tự viết, một hàm O(n) và một hàm O(n²), với n = 1.000, 2.000, 4.000, 8.000; đưa kết quả vào `classify`. Kết quả có luôn đúng lớp không? Giải thích vì sao phân loại bằng thời gian kém ổn định hơn bằng số bước.
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session01_Ex17`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-01-tong-quan-do-phuc-tap/bai-17 rồi chép các tệp vào kho: `do_tang.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Viết mã trong `do_tang.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần đo thời gian.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
