# Sinh mã xác thực theo bộ đếm cho thiết bị thanh toán MoMo

### 1. Bối cảnh & Vấn đề

![Thiết bị tại cửa hàng phải tính mã xác thực cho lần thanh toán thứ một tỷ trong chớp mắt, trên bộ xử lý rất yếu.](minh_hoa.png)

*Thiết bị tại cửa hàng phải tính mã xác thực cho lần thanh toán thứ một tỷ trong chớp mắt, trên bộ xử lý rất yếu.*

Thiết bị thanh toán MoMo đặt tại cửa hàng tạo **mã xác thực 6 chữ số** cho mỗi lần thanh toán. Đề dùng một **mô hình đơn giản hóa** của cách sinh mã theo bộ đếm: mỗi thiết bị có một số bí mật `seed` và một số `mod` (không quá 1.000.000); lần thanh toán thứ `counter` có mã là:

```plaintext
seed mũ counter, lấy phần dư khi chia cho mod, in đủ 6 chữ số (thêm số 0 ở đầu)
```

Ví dụ `seed = 7`, `counter = 3`, `mod = 1000000`: 7 × 7 × 7 = 343, mã là `000343`. Máy chủ phải tính lại đúng mã đó để đối chiếu.

Hai ràng buộc từ phía phần cứng:

- Thiết bị chạy bản Python rút gọn **không có** `pow()` và toán tử `**`.
- Bộ đếm tăng liên tục, thiết bị chạy nhiều năm nên `counter` có thể lên tới **1 tỷ**; mã phải có ngay khi khách quét (dưới 2 giây cho cả hai lần tính trong kiểm tra).

Lưu ý: chỉ cần giữ phần dư ở mỗi bước nhân, vì phần dư của một tích bằng phần dư của tích các phần dư; nhờ vậy các số trung gian không bao giờ vượt quá mod × mod. Một bạn trong nhóm viết bằng đệ quy "giảm bộ đếm đi 1": đúng với bộ đếm nhỏ, nhưng thiết bị báo lỗi từ lần thanh toán thứ khoảng 1.000. Trưởng nhóm yêu cầu bạn đề xuất ít nhất hai giải pháp, đo, so sánh rồi mới chọn.

### 2. Yêu cầu nghiệp vụ

Bạn viết ba hàm trong `ma_xac_thuc.py`.

**2.1. Hai hàm tính: `otp_value_v1(seed, counter, mod)` và `otp_value_v2(seed, counter, mod)`**

Mỗi hàm cài một giải pháp, trả về `seed` mũ `counter` chia lấy dư cho `mod` (với `counter >= 0`, `mod >= 1`). Hai hàm cho cùng kết quả nhưng **khác nhau về cách làm**.

**2.2. `otp_message(seed, counter, mod)`**

Dùng giải pháp bạn chọn, trả về một trong ba thông báo:

```plaintext
Mã xác thực lần 3: 000343
Bộ đếm không hợp lệ.
Cấu hình thiết bị không hợp lệ.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Bộ đếm 0.** Mũ 0 là 1, nên mã là `000001` (với mod lớn hơn 1).

**Bẫy 2 — mod bằng 1.** Mọi số chia cho 1 đều dư 0, kể cả khi bộ đếm là 0: hai hàm tính trả về 0.

**Bẫy 3 — seed lớn hơn mod.** `seed = 1999998`, `mod = 999983` vẫn phải đúng.

**Bẫy 4 — Dữ liệu sai.** Bộ đếm âm: "Bộ đếm không hợp lệ."; mod nhỏ hơn 1 hoặc lớn hơn 1.000.000: "Cấu hình thiết bị không hợp lệ."

**Bẫy 5 — Bộ đếm lớn.** Bộ đếm 5.000 và 1.000.000.000 phải có mã trong 2 giây, không báo `RecursionError`.

**Kịch bản chạy thử.** Chạy `python ma_xac_thuc.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Mã xác thực lần 3: 000343
Mã xác thực lần 10: 091131
Mã xác thực lần 0: 000001
Mã xác thực lần 4: 000000
Bộ đếm không hợp lệ.
Mã xác thực lần 5000: 492548
Mã xác thực lần 1000000000: 450434
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ ba phần sau:

**(1) Đề xuất và phân tích nhiều giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output của các hàm: kiểu dữ liệu đầu vào, giá trị trả về trong trường hợp thường và trong từng bẫy.
- Đề xuất **ít nhất hai giải pháp** khác nhau về cách làm cho việc tính seed mũ counter chia lấy dư. Với mỗi giải pháp: mô tả ý tưởng trong 2–3 câu, minh họa trên ví dụ ở mục 1, viết mã giả. Nếu giải pháp là đệ quy, trả lời ba câu hỏi kiểm tra (Lesson 01) và ghi độ sâu call stack lớn nhất.
- Đo thời gian hai giải pháp bằng `timeit` với bộ đếm 100, 200, 400, 800 (giải pháp chậm) và thêm 10⁶, 10⁹ cho giải pháp nhanh; ghi bảng số đo, phiên bản Python và máy đo. Với giải pháp đệ quy, đếm thêm số lời gọi bằng một biến đếm (hoặc `cache_info()` nếu dùng `lru_cache`).
- So sánh các giải pháp theo bảng 5 tiêu chí: thời gian (Big-O), bộ nhớ phụ kể cả call stack (Big-O), kết quả đo, độ dễ đọc và dễ bảo trì, mức phù hợp với bối cảnh của bài.
- Chọn giải pháp dùng cho `otp_message` và nêu lý do dựa trên bảng so sánh. Lựa chọn không có lý do không được tính điểm.

**(2) Chạy tay**

- Với mỗi giải pháp, chạy tay `seed = 3`, `counter = 13`, `mod = 1000`: ghi bộ đếm ở mỗi lời gọi (hoặc mỗi vòng), giá trị trả về khi quay lên, và tổng số phép nhân.

**(3) Triển khai code**

- Viết thân ba hàm trong `ma_xac_thuc.py`. Không đổi tên hàm, tham số.
- Không dùng `pow()` hay toán tử `**` trong hai hàm tính.
- Xử lý đủ 5 bẫy ở mục 3; `python ma_xac_thuc.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 6 mục (các mục về giải pháp chạy trên cả hai hàm `_v1`, `_v2`).
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích nêu ý tưởng và độ phức tạp ở đầu mỗi hàm.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex14`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-14 rồi chép các tệp vào kho: `ma_xac_thuc.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `ma_xac_thuc.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
