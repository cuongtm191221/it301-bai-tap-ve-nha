# Tóm tắt lịch sử nạp tiền điện thoại tự động trên MoMo

### 1. Bối cảnh & Vấn đề

![Lịch sử 500 lần nạp tự động dài cả màn hình; người dùng chỉ cần biết các đoạn thành công, thất bại và lúc nào cần chú ý.](minh_hoa.png)

*Lịch sử 500 lần nạp tự động dài cả màn hình; người dùng chỉ cần biết các đoạn thành công, thất bại và lúc nào cần chú ý.*

Ví MoMo có tính năng **nạp tiền điện thoại tự động**: mỗi ngày hệ thống thử nạp một lần và ghi trạng thái `OK`, `FAIL` hoặc `PENDING`. Sau một năm, lịch sử dài vài trăm dòng, đọc trên điện thoại rất mệt. Nhóm sản phẩm muốn **gộp các trạng thái giống nhau liền nhau** thành một nhóm:

```plaintext
["OK", "OK", "FAIL", "OK"]  ->  OK x2, FAIL x1, OK x1
```

Ngoài ra, nếu có **3 lần thất bại liên tiếp trở lên** (thường do thẻ ngân hàng hết hạn), dòng tóm tắt phải kèm cảnh báo để người dùng kiểm tra nguồn tiền.

Trạng thái do nhiều phiên bản ứng dụng ghi lại nên có chỗ viết thường, có chỗ thừa khoảng trắng. Hàm `clean(status)` (có sẵn) chuẩn hóa một trạng thái. Nhóm muốn hàm nén viết bằng đệ quy theo ý: nén **phần còn lại** trước, rồi xét **trạng thái đầu**: giống nhóm đầu của kết quả thì tăng số đếm của nhóm đó, khác thì thêm nhóm mới ở đầu.

Dòng tóm tắt hiện ở đầu màn hình "Nạp tự động" và được gửi kèm thông báo đẩy mỗi tháng. Người dùng phản ánh rằng khi thẻ hết hạn, họ chỉ phát hiện sau cả tuần vì lịch sử quá dài để đọc hết.

Bạn được giao viết ba hàm trong `nen_trang_thai.py`.

### 2. Yêu cầu nghiệp vụ

**2.1. `compress(statuses)`**

- Trả về list các cặp `(trạng thái đã chuẩn hóa, số lần liên tiếp)` theo đúng thứ tự thời gian.

**2.2. `longest_fail_streak(statuses)`**

- Trả về số lần `FAIL` liên tiếp dài nhất; không có `FAIL` thì 0.

**2.3. `summary(statuses)`**

- Trả về dòng tóm tắt các nhóm dạng `OK x2, FAIL x1, OK x1`. Nếu chuỗi `FAIL` dài nhất từ 3 trở lên, nối thêm ` | Cảnh báo: 3 lần thất bại liên tiếp`.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Chữ thường, khoảng trắng.** `["ok ", " OK", "Ok"]` là một nhóm `("OK", 3)`.

**Bẫy 2 — Chỉ gộp các trạng thái liền nhau.** `["OK", "FAIL", "OK"]` có ba nhóm, không phải `OK x2, FAIL x1`.

**Bẫy 3 — Cảnh báo.** `["OK", "FAIL", "fail", "FAIL ", "OK"]`:

```plaintext
OK x1, FAIL x3, OK x1 | Cảnh báo: 3 lần thất bại liên tiếp
```

Còn `["FAIL", "OK", "FAIL", "FAIL"]` có 3 lần `FAIL` nhưng không liên tiếp: chuỗi dài nhất là 2, không cảnh báo.

**Bẫy 4 — Chưa có giao dịch.** List rỗng: `compress` trả về `[]`, `summary` trả về `Chưa có giao dịch`.

**Bẫy 5 — Lịch sử dài.** 504 trạng thái (300 `OK`, 4 `FAIL`, 200 `OK`) nén thành ba nhóm, không báo `RecursionError`, không sửa list đầu vào.

**Kịch bản chạy thử.** Chạy `python nen_trang_thai.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
OK x2, FAIL x1, OK x1
OK x3
OK x1, FAIL x3, OK x1, FAIL x1 | Cảnh báo: 3 lần thất bại liên tiếp
PENDING x1
Chưa có giao dịch
FAIL dài nhất: 2
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng hàm, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Với mỗi hàm đệ quy, trả lời ba câu hỏi kiểm tra (Lesson 01): trường hợp cơ sở là gì, phần ghép từ kết quả nhỏ hơn ra sao, mỗi lần gọi tiến về cơ sở thế nào.
- Thiết kế giải pháp: chạy tay `compress(["OK", "ok", "FAIL"])`: ghi kết quả nén của phần còn lại ở mỗi tầng và kết quả sau khi ghép trạng thái đầu.
- Phần ghép của `compress` có hai trường hợp (gộp vào nhóm đầu, thêm nhóm mới). Mỗi trường hợp tạo list mới thế nào, có sửa list của tầng dưới không?
- `longest_fail_streak` có thể viết thẳng trên `statuses` hoặc dựa trên kết quả `compress`. Chọn cách nào, vì sao?
- Lịch sử 3 năm có khoảng 1.100 dòng. Thiết kế của bạn có chạy được không? Nếu không, sửa thế nào (Lesson 03)?
- Bộ dữ liệu thử: lập bảng ít nhất 6 đầu vào phủ đủ 5 bẫy ở mục 3, mỗi dòng ghi kết quả mong đợi (tính tay trước khi chạy) và kết quả chạy thật của bài làm.
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của `compress` theo n (số trạng thái), tính cả chi phí cắt list và nối list ở mỗi tầng.

**(2) Triển khai code**

- Viết thân các hàm còn trống trong `nen_trang_thai.py`. Không đổi tên hàm, tham số; hàm ghi "Có sẵn" giữ nguyên.
- `compress` viết bằng đệ quy: không dùng vòng lặp. Không sửa list đầu vào.
- Xử lý đủ 5 bẫy ở mục 3; `python nen_trang_thai.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 6 mục.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở trường hợp cơ sở và phần ghép.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex12`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-12 rồi chép các tệp vào kho: `nen_trang_thai.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `nen_trang_thai.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
