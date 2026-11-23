# Công cụ tra cứu đơn hàng cho bộ phận chăm sóc khách hàng Shopee

### 1. Bối cảnh & Vấn đề

![Nhân viên tổng đài gõ lệnh tra cứu trong lúc khách đang chờ máy; dữ liệu ngày sale có 200.000 đơn.](minh_hoa.png)

*Nhân viên tổng đài gõ lệnh tra cứu trong lúc khách đang chờ máy; dữ liệu ngày sale có 200.000 đơn.*

Nhân viên tổng đài chăm sóc khách hàng của Shopee cần tra cứu nhanh **trong lúc khách đang chờ máy**. Nhóm công cụ nội bộ đề nghị một **công cụ dòng lệnh**: gõ một lệnh ngắn, nhận ngay một dòng trả lời. Dữ liệu là list đơn trong ngày, mỗi đơn là một dict:

```plaintext
{"code": "DH1004", "buyer": "chi.le", "status": "Đang giao"}
```

Bốn lệnh cần có, mỗi lệnh dùng một kỹ thuật đã học trong buổi:

| Lệnh | Ý nghĩa | Ví dụ trả lời |
|---|---|---|
| `TIM <mã đơn>` | tìm kiếm tuần tự, dừng ngay khi thấy | `Đơn DH1004: Đang giao (vị trí 4, đã xét 4 đơn).` |
| `DEM <trạng thái>` | đếm số đơn có trạng thái đó | `Có 2 đơn "đang giao".` |
| `KHACH <mã khách>` | liệt kê mã đơn của một khách | `Khách an.nguyen có 3 đơn: DH1001, DH1003, DH1005.` |
| `TRUNG` | các mã đơn bị ghi trùng (lỗi đồng bộ) | `Có 1 mã đơn trùng: DH1002.` |

Ngày sale có tới 200.000 đơn, và câu trả lời phải hiện ra trong lúc khách còn chờ: lệnh `TRUNG` phải chạy xong trong **3 giây**. List đơn dùng chung cho nhiều màn hình nên **không được sửa**.

### 2. Yêu cầu nghiệp vụ

**2.1. Bốn hàm tra cứu**, mỗi hàm phục vụ một lệnh:

- `find_order(orders, code)`: trả về (vị trí tính từ 1, số đơn đã xét), không có thì (`None`, số đơn đã xét).
- `count_status(orders, status)`: số đơn có trạng thái `status`, không phân biệt hoa thường.
- `orders_of(orders, buyer)`: list mã đơn của khách, theo thứ tự trong `orders`.
- `duplicate_codes(orders)`: list các mã xuất hiện từ hai lần trở lên, **mỗi mã một lần**, xếp tăng dần.

**2.2. `handle(orders, line)`**: tách dòng lệnh theo khoảng trắng, gọi hàm phù hợp và trả về câu trả lời như bảng ở mục 1. Tên lệnh không phân biệt hoa thường; mã đơn chuyển thành chữ hoa; mã khách chuyển thành chữ thường; trạng thái là phần còn lại của dòng sau tên lệnh, các từ cách nhau một khoảng trắng.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Gõ vội:** `"TIM dh1004"`, `"  dem   đang giao "`, `"KHACH An.Nguyen"` đều hợp lệ.

**Bẫy 2 — Thiếu thông tin hoặc lệnh lạ:**

```plaintext
Thiếu thông tin. Cú pháp: TIM <mã đơn>
Lệnh không hợp lệ: XOA
Chưa nhập lệnh.
```

(`DEM` và `KHACH` thiếu thông tin thì báo cú pháp `DEM <trạng thái>`, `KHACH <mã khách>`.)

**Bẫy 3 — Không có kết quả:** `Không tìm thấy DH9999 (đã xét 6 đơn).`, `Khách dung.pham chưa có đơn.`, `Không có mã đơn trùng.`

**Bẫy 4 — Mã xuất hiện nhiều lần:** mã xuất hiện 3 lần chỉ ghi một lần trong kết quả `TRUNG`.

**Bẫy 5 — 200.000 đơn:** `TRUNG` chạy trong 3 giây và không sửa list đơn.

**Kịch bản chạy thử.** Chạy `python cskh.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
> TIM dh1004
Đơn DH1004: Đang giao (vị trí 4, đã xét 4 đơn).
> TIM DH9999
Không tìm thấy DH9999 (đã xét 6 đơn).
>   dem   đang giao 
Có 2 đơn "đang giao".
> KHACH An.Nguyen
Khách an.nguyen có 3 đơn: DH1001, DH1003, DH1005.
> KHACH dung.pham
Khách dung.pham chưa có đơn.
> TRUNG
Có 1 mã đơn trùng: DH1002.
> TIM
Thiếu thông tin. Cú pháp: TIM <mã đơn>
> XOA DH1001
Lệnh không hợp lệ: XOA
> 
Chưa nhập lệnh.
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, trong trường hợp thường và trong từng bẫy.
- Với mỗi hàm tra cứu, nêu cách làm và trường hợp tốt nhất, xấu nhất (nếu có).
- `duplicate_codes`: so sánh hai cách (so từng cặp; sắp xếp bản sao) về thời gian với 200.000 đơn; vì sao chọn cách của bạn? Viết mã giả, chỉ rõ chỗ bảo đảm mỗi mã chỉ ghi một lần.
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của bốn hàm tra cứu theo n (số đơn).

**(2) Triển khai code**

- Viết mã trong `cskh.py`; được thêm hàm phụ; không đổi tên và tham số đã có trong khung.
- Không dùng `set`, `dict`, `collections` trong `cskh.py`; không sửa list `orders`.
- Xử lý đủ 5 bẫy; `python cskh.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 5 mục.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu `dict` và `collections.Counter` của Python (sẽ học kỹ ở buổi bảng băm): vì sao tra một khóa trong `dict` thường không phải duyệt cả danh sách?
- Tạo `nghien_cuu.py`: viết lại `duplicate_codes` bằng `Counter`, đo bằng `timeit` với 200.000 đơn so với bản sắp xếp của bạn. Lập bảng số đo; kết quả có giữ được thứ tự tăng dần không, phải làm thêm gì?
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session01_Ex19`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-01-tong-quan-do-phuc-tap/bai-19 rồi chép các tệp vào kho: `cskh.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Viết mã trong `cskh.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần so sánh với `Counter`.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
