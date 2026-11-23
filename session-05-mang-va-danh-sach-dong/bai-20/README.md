# Tối ưu báo cáo cuối ca của tài xế GrabBike

### 1. Bối cảnh & Vấn đề

![Báo cáo cuối ca tính tiền thu, số cuốc hủy và các cuốc gần nhất; bản cũ chậm tới mức tài xế chạy nhiều cuốc phải chờ cả phút.](minh_hoa.png)

*Báo cáo cuối ca tính tiền thu, số cuốc hủy và các cuốc gần nhất; bản cũ chậm tới mức tài xế chạy nhiều cuốc phải chờ cả phút.*

Cuối ca, ứng dụng tài xế GrabBike hiện **báo cáo ca**: tổng tiền các cuốc hoàn thành, số cuốc bị hủy, và mã của `top` cuốc hoàn thành **gần nhất** (mới nhất trước). Mỗi cuốc là bộ `(mã, trạng thái, tiền)`; trạng thái là `"DONE"`, `"CANCELLED"` hoặc trạng thái khác (vẫn được tính như cuốc hoàn thành).

Hàm `summary_slow(trips, top)` (có sẵn trong tệp, **không được sửa**) là bản đang chạy: kết quả đúng, nhưng tài xế đối tác lớn có báo cáo tháng **200.000 cuốc** thì phải chờ rất lâu. Đọc kỹ bản cũ, bạn sẽ thấy nó dùng gần như mọi thao tác "đắt" đã học trong buổi.

Nhóm sản phẩm đã nhận nhiều đánh giá một sao với nội dung "mở báo cáo là treo máy". Với 2.000 cuốc, bản cũ chỉ mất vài phần nghìn giây nên không ai phát hiện khi thử nghiệm; chỉ khi đối tác lớn chạy báo cáo tháng thì vấn đề mới lộ ra. Đây là lý do nhóm yêu cầu kèm **số đo ở nhiều kích thước dữ liệu**, không chỉ một lần chạy với dữ liệu mẫu nhỏ, và yêu cầu bản mới phải khớp bản cũ tới từng con số, vì báo cáo ca được dùng để đối soát tiền với tài xế.

Bạn viết `summary_fast(trips, top)` cho **kết quả giống hệt** `summary_slow` với mọi dữ liệu, chạy 200.000 cuốc trong **1 giây**, và dùng số đo để chứng minh với nhóm sản phẩm rằng bản mới tốt hơn cả về thời gian lẫn bộ nhớ.

Bài này tổng hợp kiến thức cả buổi: chi phí của `+` trên list, `remove`, `pop(0)`, `insert(0, ...)`; O(1) khấu hao của `append`; đọc ngược theo chỉ số.

### 2. Yêu cầu nghiệp vụ

**2.1. `summary_fast(trips, top)`**: trả về bộ `(tổng tiền, số cuốc hủy, list mã top cuốc hoàn thành mới nhất trước)` giống `summary_slow`; không sửa `trips`.

**2.2. `shift_report(trips, top)`**: dùng `summary_fast`, trả về một dòng:

```plaintext
Thu 75.000đ, hủy 2 cuốc, gần nhất: BK4, BK3
Thu 0đ, hủy 0 cuốc, gần nhất: (không có)
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ với dữ liệu ngẫu nhiên.** Test so sánh hai bản trên 200 bộ dữ liệu ngẫu nhiên.

**Bẫy 2 — top ở biên.** `top = 0`; `top` lớn hơn số cuốc hoàn thành; ca không có cuốc nào.

**Bẫy 3 — Trạng thái khác và mã trùng.** Cuốc `"PENDING"`; hai cuốc cùng mã, cùng trạng thái, cùng tiền.

**Bẫy 4 — Không sửa dữ liệu đầu vào.**

**Bẫy 5 — 200.000 cuốc trong 1 giây.** Bản cũ với cùng dữ liệu chạy rất lâu, nên đừng chạy `summary_slow` với 200.000 cuốc khi thử.

**Kịch bản chạy thử.** Chạy `python bao_cao_ca.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
(75000, 2, ['BK4', 'BK3'])
(75000, 2, ['BK4', 'BK3'])
Thu 75.000đ, hủy 2 cuốc, gần nhất: BK4, BK3
Thu 0đ, hủy 0 cuốc, gần nhất: (không có)
Thu 3.771.418.000đ, hủy 28572 cuốc, gần nhất: BK199999, BK199998, BK199996
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, phương thức, trong trường hợp thường và trong từng bẫy.
- Lập bảng các đoạn của `summary_slow`: mỗi đoạn làm gì, thao tác list nào được dùng, số tham chiếu phải chép hoặc dịch theo n, Big-O. Đoạn nào tốn nhất?
- Bản cũ dùng `done.remove(trip)` khi có hai cuốc giống hệt nhau: có làm kết quả khác đi không? Bản của bạn bảo đảm khớp ở trường hợp này thế nào?
- Thiết kế `summary_fast`: mỗi đoạn của bản cũ được thay bằng gì.
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của `summary_slow` và `summary_fast` theo n (số cuốc) và top.

**(2) Triển khai code**

- Viết mã trong `bao_cao_ca.py`; được thêm thuộc tính, hàm phụ; không đổi tên và tham số đã có trong khung; hàm ghi "Có sẵn" giữ nguyên.
- `summary_fast` không gọi `summary_slow`; không dùng `pop(0)`, `insert(0, ...)`, `remove`, `+` để nối list trong vòng lặp; không dùng `set`, `dict`.
- Xử lý đủ 5 bẫy; `python bao_cao_ca.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 7 test có sẵn.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu module `tracemalloc` (đo bộ nhớ Python cấp phát, `get_traced_memory` trả về hiện tại và đỉnh).
- Tạo `nghien_cuu.py`: với n = 2.000, 4.000, 8.000 cuốc, đo thời gian (`timeit`) và bộ nhớ đỉnh (`tracemalloc`) của hai bản. n gấp đôi thì mỗi số đo tăng bao nhiêu lần? Đối chiếu với Big-O ở phần (1) và viết đoạn giải thích gửi nhóm sản phẩm.
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex20`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-20 rồi chép các tệp vào kho: `bao_cao_ca.py`, `test_bao_cao_ca.py`, `PHAN_TICH.md`.
3. Viết mã trong `bao_cao_ca.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần nghiên cứu.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
