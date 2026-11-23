# Tính giá khuyến mãi theo công thức hậu tố cho Tiki

### 1. Bối cảnh & Vấn đề

![Bộ phận marketing nhập công thức giá khuyến mãi dạng hậu tố; hệ thống phải tính đúng hoặc từ chối rõ ràng trước khi giá lên sàn.](minh_hoa.png)

*Bộ phận marketing nhập công thức giá khuyến mãi dạng hậu tố; hệ thống phải tính đúng hoặc từ chối rõ ràng trước khi giá lên sàn.*

Bộ phận marketing của Tiki tạo **giá khuyến mãi** bằng công thức trên một công cụ nội bộ. Để công cụ không phải xử lý dấu ngoặc và thứ tự ưu tiên phép tính, công thức được viết ở dạng **hậu tố** (postfix): mỗi phép tính đứng **sau** hai số của nó. Các phần tử cách nhau bằng dấu cách:

```plaintext
120000 2 * 15000 -        nghĩa là (120000 × 2) − 15000 = 225000
500000 500000 10 * 100 / -   nghĩa là 500000 − (500000 × 10 / 100) = 450000
```

Cách tính bằng **ngăn xếp**: đọc từ trái sang phải; gặp số thì `push`; gặp phép tính thì `pop` hai số (số lấy ra **trước** là số **bên phải**), tính, rồi `push` kết quả. Hết công thức, ngăn xếp phải còn **đúng một** số: đó là kết quả.

Công thức do người nhập tay nên hay sai. Ví dụ, nhập nhầm `120000 * 2` (dạng thông thường) vào công cụ hậu tố phải bị từ chối, không được ra một con số nào đó. Giá sai lên sàn có thể làm Tiki bán lỗ hàng trăm triệu đồng trong vài phút, nên mọi công thức sai phải bị từ chối với thông báo rõ ràng. Hàm `money(amount)` (có sẵn) in số tiền có dấu chấm.

### 2. Yêu cầu nghiệp vụ

**2.1. `evaluate(formula)`**: trả về giá trị số nguyên của công thức. Số là số nguyên, có thể có dấu `-` đứng liền trước (số âm). Phép tính: `+`, `-`, `*`, `/` (chia lấy phần nguyên, làm tròn xuống). Công thức sai báo `ValueError` với một trong các thông báo:

```plaintext
Công thức rỗng
Thiếu số cho phép tính *
Thừa số, công thức chưa hoàn chỉnh
Chia cho 0
Ký hiệu không hợp lệ: x
```

**2.2. `price_message(formula)`**: trả về `Giá: 225.000đ` hoặc `Lỗi công thức: <thông báo>`.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Thứ tự hai số.** `10 3 -` là 7, `10 3 /` là 3, không phải −7 hay 0.

**Bẫy 2 — Khoảng trắng thừa và số âm.** `"   7   -2   * "` là −14; dấu `-` đứng riêng là phép trừ, dính liền chữ số là số âm.

**Bẫy 3 — Thiếu số, thừa số.** `120000 * 2` (phép tính khi ngăn xếp chưa đủ hai số); `120000 2 3 *` (hết công thức còn hai số).

**Bẫy 4 — Chia cho 0, ký hiệu lạ.** `100000 0 /`; `120000 2 x`, `12a`, `1.5`, `^` đều là ký hiệu không hợp lệ.

**Bẫy 5 — Công thức dài.** Công thức 100.001 phần tử vẫn tính đúng (không dùng đệ quy).

**Kịch bản chạy thử.** Chạy `python cong_thuc_gia.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
'120000 2 * 15000 -'             -> Giá: 225.000đ
'500000 500000 10 * 100 / -'     -> Giá: 450.000đ
'  99000   '                     -> Giá: 99.000đ
'120000 * 2'                     -> Lỗi công thức: Thiếu số cho phép tính *
'120000 2 3 *'                   -> Lỗi công thức: Thừa số, công thức chưa hoàn chỉnh
'100000 0 /'                     -> Lỗi công thức: Chia cho 0
'120000 2 x'                     -> Lỗi công thức: Ký hiệu không hợp lệ: x
''                               -> Lỗi công thức: Công thức rỗng
'5000 8000 -'                    -> Giá: -3.000đ
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng hàm hoặc phương thức, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Thiết kế giải pháp: chạy tay `500000 500000 10 * 100 / -`, ghi ngăn xếp sau mỗi phần tử.
- Chỉ ra vị trí trong thuật toán phát hiện từng loại lỗi (thiếu số, thừa số, chia cho 0, ký hiệu lạ, rỗng).
- Vì sao số lấy ra trước là số bên phải? Điều gì xảy ra với phép trừ và chia nếu nhầm thứ tự?
- Chuyển `(120000 - 15000) * 2` sang dạng hậu tố và kiểm tra bằng hàm của bạn.
- Bộ dữ liệu thử: lập bảng ít nhất 6 đầu vào phủ đủ 5 bẫy ở mục 3, mỗi dòng ghi kết quả mong đợi (tính tay trước khi chạy) và kết quả chạy thật của bài làm.
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của `evaluate` theo n (số phần tử của công thức), trường hợp xấu nhất của độ cao ngăn xếp.

**(2) Triển khai code**

- Viết thân các hàm, phương thức còn trống trong `cong_thuc_gia.py`. Không đổi tên, tham số, thông báo lỗi; hàm ghi "Có sẵn" giữ nguyên; được thêm thuộc tính và hàm phụ.
- Dùng ngăn xếp (list với `append`, `pop`); không dùng `eval`, không đệ quy.
- Xử lý đủ 5 bẫy ở mục 3; `python cong_thuc_gia.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test có sẵn.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ quyết định độ phức tạp.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex09`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-09 rồi chép các tệp vào kho: `cong_thuc_gia.py`, `test_cong_thuc_gia.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `cong_thuc_gia.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
