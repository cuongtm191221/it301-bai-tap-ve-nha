# Sổ giá vốn hàng tồn kho theo lô cho người bán trên Tiki

### 1. Bối cảnh & Vấn đề

![Người bán nhập hàng nhiều đợt với giá khác nhau; báo cáo lãi lỗ cần biết mỗi sản phẩm xuất ra mang giá vốn của lô nào.](minh_hoa.png)

*Người bán nhập hàng nhiều đợt với giá khác nhau; báo cáo lãi lỗ cần biết mỗi sản phẩm xuất ra mang giá vốn của lô nào.*

Người bán trên Tiki nhập hàng nhiều đợt, mỗi đợt một **lô** với đơn giá khác nhau (giá nhà cung cấp tăng, giảm theo mùa). Khi đơn hàng được giao, hệ thống phải ghi **giá vốn** của số sản phẩm xuất kho để báo cáo lãi lỗ: bán được 180.000đ một tai nghe, nhưng tai nghe đó nhập giá 100.000đ hay 130.000đ thì lãi rất khác nhau.

Hai cách tính giá xuất kho mà nhóm kế toán của người bán đưa ra để so sánh:

- **FIFO** (nhập trước, xuất trước): sản phẩm xuất ra lấy từ lô nhập **sớm nhất** còn hàng. Các lô xếp hàng như một **queue**.
- **LIFO** (nhập sau, xuất trước): lấy từ lô nhập **muộn nhất** còn hàng. Các lô chồng lên nhau như một **stack**.

Một lần xuất có thể lấy hết một lô rồi lấy **một phần** lô kế tiếp. Ví dụ FIFO: tồn 10 sản phẩm giá 100.000đ và 5 sản phẩm giá 120.000đ, xuất 12 thì giá vốn là 10 × 100.000 + 2 × 120.000 = 1.240.000đ, còn lại 3 sản phẩm giá 120.000đ.

Người bán lớn có hàng trăm nghìn lô nhỏ (mỗi lô vài sản phẩm, hàng ký gửi nhập theo ngày), và trang tổng quan gọi `stock_value()` sau **mỗi** lần nhập, xuất để hiện giá trị tồn kho. Bản thử đầu tiên lưu lô trong list, lấy lô đầu bằng `pop(0)` và tính lại giá trị tồn bằng vòng lặp qua mọi lô: tài khoản lớn mở trang là treo.

Bài này tổng hợp kiến thức cả buổi: queue và stack trên cùng một tập dữ liệu, deque dùng được cả hai đầu, chi phí `pop(0)`, giữ bất biến khi thao tác thất bại.

### 2. Yêu cầu nghiệp vụ

**2.1. `StockLedger(method)`**: `method` là `"FIFO"` hoặc `"LIFO"`, khác báo `ValueError("Phương pháp không hỗ trợ")`. Bạn tự chọn cách lưu các lô.

**2.2. `receive(qty, unit_cost)`, `issue(qty)`**: nhập một lô; xuất và trả về giá vốn (đồng). Thông báo lỗi đúng như trong docstring.

**2.3. `on_hand()`, `stock_value()`, `lots()`**: tổng số lượng tồn; giá trị tồn; list bộ `(số lượng còn, đơn giá)` theo thứ tự nhập.

**2.4. `cost_report(method, events)`**: chạy một chuỗi sự kiện, trả về một dòng:

```plaintext
FIFO: giá vốn 1990000đ, tồn 5 sp trị giá 650000đ
FIFO: lỗi ở bước 2: Không đủ hàng: còn 3
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Lấy một phần lô.** Lô bị lấy một phần vẫn ở đúng vị trí với số lượng còn lại; lô bị lấy hết thì biến mất khỏi `lots()`.

**Bẫy 2 — Thiếu hàng.** Xuất nhiều hơn số tồn báo lỗi và sổ **giữ nguyên**: không lô nào bị trừ dở dang.

**Bẫy 3 — Dữ liệu sai.** Số lượng, đơn giá bằng 0, âm, số thực, chuỗi, `True`; phương pháp viết thường `"fifo"`.

**Bẫy 4 — Hai phương pháp, cùng sự kiện.** Với chuỗi sự kiện của kịch bản chạy thử, FIFO và LIFO cho giá vốn và giá trị tồn khác nhau; tổng giá vốn cộng giá trị tồn của hai cách phải bằng nhau (bằng tổng tiền nhập).

**Bẫy 5 — 100.000 lô nhỏ.** Nhập 100.000 lô một sản phẩm rồi xuất từng sản phẩm một, gọi `stock_value()` sau mỗi lần, xong trong 2 giây; xuất 100.000 sản phẩm trong một lần cũng vậy. Không dùng `pop(0)`, `insert(0, ...)`.

**Kịch bản chạy thử.** Chạy `python gia_von.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
FIFO: giá vốn 1990000đ, tồn 5 sp trị giá 650000đ
LIFO: giá vốn 2080000đ, tồn 5 sp trị giá 560000đ
Xuất 12, giá vốn: 1240000 | lô còn lại: [(3, 120000)]
FIFO: lỗi ở bước 2: Không đủ hàng: còn 3
FIFO: lỗi ở bước 1: Số lượng và đơn giá phải là số nguyên dương
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, phương thức, trong trường hợp thường và trong từng bẫy.
- Chạy tay chuỗi sự kiện của kịch bản chạy thử với FIFO và với LIFO: sau mỗi sự kiện, các lô còn lại và giá vốn của lần xuất.
- Chọn cấu trúc lưu các lô sao cho cả FIFO và LIFO đều lấy lô cần thiết trong O(1); giải thích vì sao list với `pop(0)` không đạt.
- Bẫy 2: thiết kế `issue` để khi thiếu hàng không có lô nào bị trừ dở dang; vì sao kiểm tra trước rẻ hơn "trừ rồi hoàn lại"?
- Bẫy 5: làm sao `stock_value()` không phải duyệt mọi lô?
- Độ phức tạp: ghi Big-O thời gian của `receive`, `issue` (theo số lô bị chạm tới), `stock_value`, `lots`, và tổng thời gian của n lần nhập rồi n lần xuất.

**(2) Triển khai code**

- Viết mã trong `gia_von.py`; được thêm thuộc tính, hàm phụ; không đổi tên và tham số đã có trong khung; hàm ghi "Có sẵn" giữ nguyên.
- Không dùng `pop(0)`, `insert(0, ...)` trên list; `stock_value` và `on_hand` không duyệt các lô.
- Xử lý đủ 5 bẫy; `python gia_von.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test có sẵn.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu quy định kế toán Việt Nam về phương pháp tính giá trị hàng xuất kho: Chuẩn mực kế toán số 02 (VAS 02, Hàng tồn kho) và Thông tư 200/2014/TT-BTC. Những phương pháp nào được dùng? LIFO còn được phép không, từ văn bản nào? Chuẩn mực quốc tế IAS 2 nói gì về LIFO?
- Tạo `nghien_cuu.py`: dùng `StockLedger` của bạn cho 12 tháng, mỗi tháng nhập 100 sản phẩm giá tăng 5.000đ so với tháng trước và bán 80 sản phẩm giá 180.000đ. In giá vốn, lợi nhuận gộp, giá trị tồn của FIFO và LIFO. Dựa trên số liệu, giải thích vì sao khi giá tăng, LIFO làm báo cáo lợi nhuận và giá trị tồn kho kém phản ánh thực tế.
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex18`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-18 rồi chép các tệp vào kho: `gia_von.py`, `test_gia_von.py`, `PHAN_TICH.md`.
3. Viết mã trong `gia_von.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần nghiên cứu.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
