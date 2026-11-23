# Máy tính công thức giá cho người bán trên Tiki

### 1. Bối cảnh & Vấn đề

![Người bán gõ công thức giá có ngoặc; bản cũ đưa thẳng chuỗi vào eval, vừa tính sai quy tắc vừa chạy được mã lạ.](minh_hoa.png)

*Người bán gõ công thức giá có ngoặc; bản cũ đưa thẳng chuỗi vào eval, vừa tính sai quy tắc vừa chạy được mã lạ.*

Trên trang quản lý của người bán Tiki, ô **giá bán** cho phép gõ công thức thay vì một con số, ví dụ `(199000 - 20000) * 90 / 100` nghĩa là giá gốc trừ phí vận chuyển hỗ trợ rồi giảm 10%. Người bán quen dùng công thức vì một mã hàng có thể có hàng chục biến thể, mỗi biến thể đổi một vài con số. Hệ thống tính công thức, hiện giá kết quả và lưu cả công thức để lần sau người bán sửa.

Bản thử đầu tiên đưa thẳng chuỗi vào hàm `eval` của Python. Nhóm bảo mật chặn lại ngay: ô nhập là dữ liệu do người ngoài gõ, `eval` sẽ chạy bất kỳ đoạn mã Python nào được gõ vào. Nhóm sản phẩm cũng không hài lòng: `eval("1000 / 3")` ra số thực `333.333...`, trong khi giá trên Tiki là số nguyên đồng.

Bài 09 của buổi này đã có hàm tính biểu thức **hậu tố**. Người bán thì không gõ hậu tố; họ gõ **trung tố** có ngoặc như trên giấy. Bạn viết phần còn thiếu: tách chuỗi thành token, chuyển trung tố sang hậu tố bằng stack (thuật toán thường gọi là shunting-yard, "sân dồn toa"), rồi dùng hàm tính hậu tố **có sẵn** `evaluate_postfix`.

Quy tắc tính giá của Tiki:

- Chỉ có số nguyên không âm, bốn phép `+ - * /`, ngoặc tròn và khoảng trắng. Không có số âm đứng một mình (`-5`), không có dấu phẩy thập phân.
- `*` và `/` tính trước `+` và `-`; các phép **cùng mức** tính **từ trái sang phải**: `100000 - 20000 - 10000` là 70000, không phải 90000.
- `/` là chia lấy phần nguyên (như `//`); chia cho 0 báo `ZeroDivisionError("Chia cho 0")` (đã có trong `evaluate_postfix`).

Bài này tổng hợp kiến thức cả buổi: stack (LIFO) cho toán tử và ngoặc, kiểm tra ngoặc cân bằng, tính biểu thức hậu tố, xử lý dữ liệu do người dùng nhập.

### 2. Yêu cầu nghiệp vụ

**2.1. `tokenize(expr)`**: trả về list token; số là `int`, toán tử và ngoặc là chuỗi một ký tự; ký tự khác báo `ValueError("Ký tự không hợp lệ: <ký tự>")`.

**2.2. `to_postfix(tokens)`**: trả về list token hậu tố. Ngoặc không khớp báo `ValueError("Ngoặc không khớp")`; thiếu số, thừa toán tử, hai số liền nhau, ngoặc rỗng, biểu thức rỗng báo `ValueError("Biểu thức sai cú pháp")`.

**2.3. `calculate(expr)`, `price_message(name, expr)`**: tính công thức; trả về dòng hiển thị cho người bán:

```plaintext
Giá tai nghe: 161100đ
Lỗi công thức sạc: Ngoặc không khớp
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Cùng mức, tính từ trái.** `100000 - 20000 - 10000` là 70000; `1000 / 10 / 2` là 50. Đây là chỗ sai hay gặp nhất khi tự viết thuật toán chuyển hậu tố.

**Bẫy 2 — Ngoặc không khớp.** `(150000 + 5000`, `1 + 2)`, `((1)`, `)1 + 2(`.

**Bẫy 3 — Sai cú pháp.** `300000 +`, `+ 5`, `2 3`, `2 * * 3`, `()`, `-5 + 2`, `(2)(3)`, chuỗi rỗng hoặc chỉ có khoảng trắng. Một số trường hợp vẫn chuyển được thành hậu tố nhìn có vẻ hợp lệ nếu bạn không kiểm tra; hãy tìm cách phát hiện **ngay trong lúc chuyển**.

**Bẫy 4 — Ký tự lạ.** `50000 * 0,9` báo lỗi ở dấu phẩy; chuỗi có chữ cái, dấu gạch dưới, dấu chấm đều bị từ chối, không bao giờ được chạy như mã.

**Bẫy 5 — Ngoặc sâu và công thức dài.** 3.000 tầng ngoặc lồng nhau và công thức 50.000 phép nhân cộng nối tiếp phải tính xong trong 2 giây; không dùng `eval`, `exec`, không dùng đệ quy theo độ sâu ngoặc.

**Kịch bản chạy thử.** Chạy `python may_tinh_gia.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
['(', 199000, '-', 20000, ')', '*', 90, '/', 100]
[199000, 20000, '-', 90, '*', 100, '/']
Giá tai nghe: 161100đ
Giá ốp lưng: 70000đ
Lỗi công thức sạc: Ngoặc không khớp
Lỗi công thức cáp: Ký tự không hợp lệ: ,
Lỗi công thức pin: Chia cho 0
Lỗi công thức loa: Biểu thức sai cú pháp
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, phương thức, trong trường hợp thường và trong từng bẫy.
- Lập bảng chạy tay việc chuyển `(199000 - 20000) * 90 / 100` sang hậu tố: mỗi token, stack toán tử và danh sách kết quả sau bước đó.
- Chạy tay `100000 - 20000 - 10000` với điều kiện lấy toán tử ra khỏi stack là "mức của đỉnh **lớn hơn** mức toán tử mới" và với "**lớn hơn hoặc bằng**": mỗi cách cho hậu tố nào, kết quả bao nhiêu? Cách nào đúng quy tắc của Tiki?
- Mô tả cách bạn phát hiện sai cú pháp (bẫy 3): ở mỗi vị trí, token nào được phép xuất hiện? Vì sao `(2)(3)` và `2 3` bị từ chối?
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của `tokenize`, `to_postfix`, `calculate` theo n (độ dài công thức), và độ sâu lớn nhất của stack toán tử theo số tầng ngoặc.

**(2) Triển khai code**

- Viết mã trong `may_tinh_gia.py`; được thêm thuộc tính, hàm phụ; không đổi tên và tham số đã có trong khung; hàm ghi "Có sẵn" giữ nguyên.
- Không dùng `eval`, `exec`; giữ nguyên `evaluate_postfix` và `OPERATORS`.
- Xử lý đủ 5 bẫy; `python may_tinh_gia.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test có sẵn.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu vì sao không nên dùng `eval` cho dữ liệu người dùng nhập (tài liệu Python về `eval`, `ast.literal_eval`; các bài viết về lỗ hổng chèn mã, code injection).
- Tạo `nghien_cuu.py`: minh họa một chuỗi mà `eval` chạy như mã còn `calculate` của bạn từ chối (chọn lệnh vô hại, ví dụ in thư mục hiện tại); so sánh kết quả `eval("1000 / 3")` với `calculate`; thử `ast.literal_eval("2 * 3")`; đo thời gian `calculate` và `eval` trên một công thức 1.000 phép bằng `timeit`. Kết luận: bạn trả lời nhóm bảo mật thế nào khi có người đề xuất "dùng eval cho nhanh"?
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex17`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-17 rồi chép các tệp vào kho: `may_tinh_gia.py`, `test_may_tinh_gia.py`, `PHAN_TICH.md`.
3. Viết mã trong `may_tinh_gia.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần nghiên cứu.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
