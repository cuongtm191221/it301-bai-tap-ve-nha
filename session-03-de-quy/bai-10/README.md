# Định dạng số tiền trên biên lai chuyển tiền MoMo

### 1. Bối cảnh & Vấn đề

![Biên lai phải hiện 1.005.000đ, nhưng cách định dạng đơn giản lại cho ra 1.5.0đ.](minh_hoa.png)

*Biên lai phải hiện 1.005.000đ, nhưng cách định dạng đơn giản lại cho ra 1.5.0đ.*

Sau mỗi lần chuyển tiền, ví MoMo hiện **biên lai** cho người gửi. Số tiền phải có **dấu chấm ngăn cách hàng nghìn** theo cách viết của Việt Nam:

```plaintext
Chuyển tiền cho Nguyễn Văn An: 1.005.000đ
```

Nhóm biên lai không được dùng các cách định dạng có sẵn của Python (`f"{amount:,}"`, `format()`), vì biên lai còn được sinh trên thiết bị đọc thẻ đời cũ chạy một bản Python rút gọn không có các hàm đó; mã của bạn sẽ được chuyển sang thiết bị này.

Nhóm muốn viết bằng đệ quy theo ý: số tiền có từ bốn chữ số trở lên = **phần đầu** (bỏ ba chữ số cuối, tức `amount // 1000`) đã định dạng, nối dấu chấm, nối **ba chữ số cuối** (`amount % 1000`). Một lập trình viên đã thử viết nhanh và nhận được `1.5.0` cho số 1.005.000; nhóm cần một bản đúng với mọi số tiền.

Cùng hàm này còn được dùng cho màn hình lịch sử giao dịch, thông báo đẩy và sao kê tháng gửi qua email, nên chỉ cần sai ở một nhóm chữ số là khách hàng thấy số tiền khác nhau trên ba nơi. Bộ phận chăm sóc khách hàng ghi nhận nhiều cuộc gọi hỏi vì sao biên lai ghi "1.5.0đ" trong khi tài khoản bị trừ 1.005.000đ; vài khách còn nghi ngờ bị trừ tiền hai lần.

Tên người nhận lấy từ danh bạ của người gửi nên thường thừa dấu cách ở đầu, ở cuối hoặc giữa họ và tên; có trường hợp danh bạ chỉ lưu số điện thoại, tên để trống.

Bạn được giao viết hai hàm trong `dinh_dang_tien.py`.

### 2. Yêu cầu nghiệp vụ

**2.1. `format_money(amount)`**

- Nhận số nguyên `amount`, trả về chuỗi có dấu chấm ngăn cách mỗi nhóm ba chữ số tính từ phải sang: `1234567` thành `"1.234.567"`, `45000` thành `"45.000"`.
- Số âm (hoàn tiền, điều chỉnh) có dấu `-` ở đầu.

**2.2. `receipt_line(name, amount)`**

- Trả về dòng biên lai `Chuyển tiền cho <tên>: <số tiền>đ`.
- Tên người nhận được bỏ khoảng trắng thừa ở hai đầu và giữa các từ (chỉ giữ một dấu cách giữa hai từ).

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Số dưới 1.000.** `0`, `7`, `950` giữ nguyên, không có dấu chấm.

**Bẫy 2 — Nhóm có chữ số 0 ở đầu.** `1005` phải thành `"1.005"`, không phải `"1.5"`; `1000005` thành `"1.000.005"`. Mọi nhóm sau nhóm đầu luôn đủ ba chữ số.

**Bẫy 3 — Số âm.** `-1500000` thành `"-1.500.000"`; `-999` thành `"-999"`. Dấu chấm không được chen giữa dấu `-` và chữ số.

**Bẫy 4 — Số rất lớn.** Tổng chuyển khoản của doanh nghiệp tới hàng tỷ: `2500000000` thành `"2.500.000.000"`.

**Bẫy 5 — Tên người nhận trống.** Tên chỉ gồm dấu cách thì ghi `Không rõ người nhận`:

```plaintext
Chuyển tiền cho Không rõ người nhận: 20.000đ
```

**Kịch bản chạy thử.** Chạy `python dinh_dang_tien.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
0
950
1.000
1.005
45.000
1.234.567
1.000.005
2.500.000.000
-1.500.000
Chuyển tiền cho Nguyễn Văn An: 1.005.000đ
Chuyển tiền cho Không rõ người nhận: 20.000đ
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng hàm, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Với mỗi hàm đệ quy, trả lời ba câu hỏi kiểm tra (Lesson 01): trường hợp cơ sở là gì, phần ghép từ kết quả nhỏ hơn ra sao, mỗi lần gọi tiến về cơ sở thế nào.
- Thiết kế giải pháp: chạy tay `format_money(1005000)`: ghi `amount` ở mỗi lời gọi, phần đầu, ba chữ số cuối và chuỗi trả về khi quay lên. Chỉ ra bước làm cách viết nhanh ra `1.5.0`.
- Số âm nên xử lý ở đâu: trong trường hợp cơ sở, trong phần ghép, hay trước khi đệ quy? Vì sao?
- Một số tiền có d chữ số cần bao nhiêu lời gọi đệ quy? Có cần lo `RecursionError` không?
- Nhóm biên lai định đổi sang cách viết `str(amount)` rồi chèn dấu chấm từ phải sang. Cách đó có cần đệ quy không? Nêu một ưu điểm và một nhược điểm so với cách chia cho 1000.
- Bộ dữ liệu thử: lập bảng ít nhất 6 đầu vào phủ đủ 5 bẫy ở mục 3, mỗi dòng ghi kết quả mong đợi (tính tay trước khi chạy) và kết quả chạy thật của bài làm.
- Độ phức tạp: ghi Big-O thời gian theo d (số chữ số của số tiền) và theo giá trị n của số tiền. Vì sao hai cách ghi đều đúng?

**(2) Triển khai code**

- Viết thân các hàm còn trống trong `dinh_dang_tien.py`. Không đổi tên hàm, tham số; hàm ghi "Có sẵn" giữ nguyên.
- `format_money` viết bằng đệ quy: không dùng vòng lặp, không dùng `f"{amount:,}"`, `format()` hay `replace()`.
- Xử lý đủ 5 bẫy ở mục 3; `python dinh_dang_tien.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 6 mục.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở trường hợp cơ sở và phần ghép.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex10`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-10 rồi chép các tệp vào kho: `dinh_dang_tien.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `dinh_dang_tien.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
