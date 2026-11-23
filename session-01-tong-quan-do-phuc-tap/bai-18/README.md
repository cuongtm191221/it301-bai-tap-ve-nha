# Báo cáo tồn kho cuối ngày cho người bán Shopee

### 1. Bối cảnh & Vấn đề

![Cuối ngày người bán cần một dòng tóm tắt tồn kho và danh sách cần nhập thêm; gian hàng lớn có 200.000 sản phẩm.](minh_hoa.png)

*Cuối ngày người bán cần một dòng tóm tắt tồn kho và danh sách cần nhập thêm; gian hàng lớn có 200.000 sản phẩm.*

Cuối mỗi ngày, ứng dụng người bán của Shopee gửi **báo cáo tồn kho**: tổng quan gian hàng và danh sách sản phẩm cần nhập thêm. Dữ liệu là list sản phẩm theo thứ tự đăng bán:

```plaintext
{"code": "SP04", "price": 99000, "stock": -2}
```

Dữ liệu được đồng bộ từ phần mềm kho của người bán nên có **dòng lỗi**: giá bằng 0, giá âm, giá là số thực. Tồn kho âm là hàng đã bán vượt.

Báo cáo chạy cho mọi gian hàng cùng lúc, có gian hàng tới 200.000 sản phẩm, nên nhóm đặt yêu cầu bộ nhớ khác nhau cho từng phần:

- **Tóm tắt**: chỉ cần vài con số, nên phải tính trong **một lượt duyệt**, bộ nhớ phụ **O(1)**: không tạo list, không sắp xếp.
- **Danh sách cần nhập thêm**: cần xếp theo tồn kho, được tạo bản sao (O(n) bộ nhớ phụ), nhưng **không được đổi thứ tự** list sản phẩm.

Bạn được giao viết bốn hàm trong `ton_kho.py` (hàm `format_money` có sẵn).

### 2. Yêu cầu nghiệp vụ

**2.1. `is_valid(product)`**: sản phẩm hợp lệ khi giá là **số nguyên lớn hơn 0**. Mọi hàm sau chỉ xét sản phẩm hợp lệ.

**2.2. `inventory_summary(products)`**: trả về dict sáu khóa:

| Khóa | Ý nghĩa |
|---|---|
| `valid` | số sản phẩm hợp lệ |
| `out_of_stock` | số sản phẩm hết hàng (tồn kho từ 0 trở xuống) |
| `stock_value` | tổng giá × tồn kho của các sản phẩm còn hàng |
| `cheapest`, `priciest` | mã sản phẩm rẻ nhất, đắt nhất (`None` nếu không có) |
| `skipped` | số dòng lỗi |

**2.3. `restock_list(products, k)`**: list mã k sản phẩm hợp lệ có **tồn kho thấp nhất**, thấp nhất đứng trước.

**2.4. `summary_message(products)`**: thông báo một dòng, tiền viết bằng `format_money`:

```plaintext
5 sản phẩm, 2 hết hàng. Giá trị tồn kho: 9.873.000đ. Rẻ nhất: SP03, đắt nhất: SP02. Bỏ qua 1 dòng lỗi.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Dòng lỗi:** giá 0, giá -5, giá 99.5 đều bị bỏ qua và đếm vào `skipped`.

**Bẫy 2 — Tồn kho âm:** tính là hết hàng, **không** làm giảm giá trị tồn kho.

**Bẫy 3 — Bằng giá, bằng tồn kho:** sản phẩm đứng trước được chọn (rẻ nhất `SP03` chứ không phải `SP04`; trong danh sách nhập thêm, sản phẩm đứng trước xếp trên).

**Bẫy 4 — k ngoài khoảng:** k lớn hơn số sản phẩm hợp lệ thì trả về tất cả; k không dương thì trả về `[]`.

**Bẫy 5 — Không có sản phẩm hợp lệ:**

```plaintext
Chưa có sản phẩm hợp lệ. Bỏ qua 1 dòng lỗi.
```

**Kịch bản chạy thử.** Chạy `python ton_kho.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
{'valid': 5, 'out_of_stock': 2, 'stock_value': 9873000, 'cheapest': 'SP03', 'priciest': 'SP02', 'skipped': 1}
5 sản phẩm, 2 hết hàng. Giá trị tồn kho: 9.873.000đ. Rẻ nhất: SP03, đắt nhất: SP02. Bỏ qua 1 dòng lỗi.
Cần nhập thêm (3 sản phẩm): ['SP04', 'SP03', 'SP02']
Cần nhập thêm (10 sản phẩm): ['SP04', 'SP03', 'SP02', 'SP06', 'SP01']
Thứ tự gốc giữ nguyên: ['SP01', 'SP02', 'SP03', 'SP04', 'SP05', 'SP06']
Chưa có sản phẩm hợp lệ. Bỏ qua 1 dòng lỗi.
Chưa có sản phẩm hợp lệ. Bỏ qua 0 dòng lỗi.
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, trong trường hợp thường và trong từng bẫy.
- Liệt kê các biến `inventory_summary` cần giữ trong một lượt duyệt; lập bảng chạy tay trên 6 sản phẩm của kịch bản chạy thử.
- Vì sao `restock_list` được tạo bản sao còn `inventory_summary` thì không? Viết mã giả của `restock_list`.
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của bốn hàm theo n (số sản phẩm).

**(2) Triển khai code**

- Viết mã trong `ton_kho.py`; được thêm hàm phụ; không đổi tên và tham số đã có trong khung.
- `inventory_summary` duyệt đúng một vòng `for`, không dùng `sort`, `sorted`, `min`, `max` và không tạo list.
- Xử lý đủ 5 bẫy; `python ton_kho.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 5 mục.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu mô-đun `tracemalloc` (đo bộ nhớ đỉnh khi chạy một hàm) và so với `sys.getsizeof` ở Lesson 04: mỗi công cụ đo được gì.
- Tạo `nghien_cuu.py`: với 200.000 sản phẩm, đo bộ nhớ đỉnh của `inventory_summary` và của một cách viết khác dùng list trung gian (ví dụ tạo list giá hợp lệ rồi gọi `min`, `max`, `sum`). Thử thêm biểu thức sinh (generator expression) `sum(p["price"] for p in ...)`. Lập bảng số đo và giải thích bằng Big-O bộ nhớ phụ.
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session01_Ex18`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-01-tong-quan-do-phuc-tap/bai-18 rồi chép các tệp vào kho: `ton_kho.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Viết mã trong `ton_kho.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần đo bộ nhớ.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
