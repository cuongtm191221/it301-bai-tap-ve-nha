# Đếm số cách chọn ô quà trong trò chơi "Mở hộp may mắn" của MoMo

### 1. Bối cảnh & Vấn đề

![Trò chơi cho chọn k hộp trong n hộp; nhóm thiết kế cần số cách chọn để tính xác suất trúng giải, nhưng bản đồ lớn làm màn hình đứng yên.](minh_hoa.png)

*Trò chơi cho chọn k hộp trong n hộp; nhóm thiết kế cần số cách chọn để tính xác suất trúng giải, nhưng bản đồ lớn làm màn hình đứng yên.*

Trò chơi **"Mở hộp may mắn"** của ví MoMo bày `n` hộp quà, người chơi được chọn `k` hộp khác nhau cùng lúc (không kể thứ tự chọn). Để tính **xác suất trúng giải** hiện trên màn hình, nhóm thiết kế cần biết **số cách chọn k hộp trong n hộp**. Ví dụ 5 hộp chọn 2 có 10 cách.

Một bạn trong nhóm viết bằng đệ quy theo ý: xét hộp cuối cùng, hoặc chọn nó (còn phải chọn `k - 1` hộp trong `n - 1` hộp còn lại), hoặc không chọn (chọn `k` hộp trong `n - 1` hộp). Cách viết rất ngắn và đúng với trò chơi nhỏ, nhưng màn hình **đứng yên** khi nhóm thử bản đồ 40 hộp chọn 20. Sự kiện cuối năm có bản đồ tới **300 hộp chọn 150**, và con số phải có trong **2 giây**.

Nhóm không được dùng `math.comb` hay `math.factorial` vì cùng thư viện sẽ được chuyển sang thiết bị chạy bản Python rút gọn. Trưởng nhóm yêu cầu bạn đề xuất ít nhất hai giải pháp, đo, so sánh rồi mới chọn.

### 2. Yêu cầu nghiệp vụ

Bạn viết ba hàm trong `chon_qua.py`.

**2.1. Hai hàm đếm: `choose_count_v1(n, k)` và `choose_count_v2(n, k)`**

Mỗi hàm cài một giải pháp, trả về số cách chọn `k` hộp trong `n` hộp. Hai hàm cho cùng kết quả với mọi dữ liệu nhưng **khác nhau về cách làm**.

**2.2. `prize_message(n, k)`**

Dùng giải pháp bạn chọn, trả về một trong ba thông báo:

```plaintext
Có 10 cách chọn 2 ô trong 5 ô.
Không đủ ô: cần chọn 6 ô nhưng chỉ có 4 ô.
Dữ liệu trò chơi không hợp lệ.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Chọn hết hoặc không chọn.** Chọn `n` hộp trong `n` hộp, hoặc chọn 0 hộp: đúng 1 cách (hai hàm đếm).

**Bẫy 2 — k ngoài khoảng.** `k > n` hoặc `k < 0`: hai hàm đếm trả về 0; thông báo với `k > n` là "Không đủ ô...".

**Bẫy 3 — Dữ liệu trò chơi sai.** `n` hoặc `k` từ 0 trở xuống: "Dữ liệu trò chơi không hợp lệ."

**Bẫy 4 — Kết quả rất lớn.** 300 hộp chọn 150 cho một số có 89 chữ số; Python lưu được số nguyên lớn, nhưng giải pháp không được đi qua số thực (sai số làm tròn).

**Bẫy 5 — Bản đồ lớn.** 40 chọn 20 và 300 chọn 150: thông báo trong 2 giây, không báo `RecursionError`.

**Kịch bản chạy thử.** Chạy `python chon_qua.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Có 10 cách chọn 2 ô trong 5 ô.
Có 1 cách chọn 10 ô trong 10 ô.
Không đủ ô: cần chọn 6 ô nhưng chỉ có 4 ô.
Dữ liệu trò chơi không hợp lệ.
Có 137846528820 cách chọn 20 ô trong 40 ô.
Có 118264581564861424 cách chọn 30 ô trong 60 ô.
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ ba phần sau:

**(1) Đề xuất và phân tích nhiều giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output của các hàm: kiểu dữ liệu đầu vào, giá trị trả về trong trường hợp thường và trong từng bẫy.
- Đề xuất **ít nhất hai giải pháp** khác nhau về cách làm cho việc đếm số cách chọn. Với mỗi giải pháp: mô tả ý tưởng trong 2–3 câu, minh họa trên ví dụ ở mục 1, viết mã giả. Nếu giải pháp là đệ quy, trả lời ba câu hỏi kiểm tra (Lesson 01) và ghi độ sâu call stack lớn nhất.
- Đo thời gian hai giải pháp bằng `timeit` với n = 16, 18, 20, 22 và k = n / 2; ghi bảng số đo, phiên bản Python và máy đo. Với giải pháp đệ quy, đếm thêm số lời gọi bằng một biến đếm (hoặc `cache_info()` nếu dùng `lru_cache`).
- So sánh các giải pháp theo bảng 5 tiêu chí: thời gian (Big-O), bộ nhớ phụ kể cả call stack (Big-O), kết quả đo, độ dễ đọc và dễ bảo trì, mức phù hợp với bối cảnh của bài.
- Chọn giải pháp dùng cho `prize_message` và nêu lý do dựa trên bảng so sánh. Lựa chọn không có lý do không được tính điểm.

**(2) Chạy tay**

- Với mỗi giải pháp, chạy tay 5 hộp chọn 2: vẽ cây lời gọi (hoặc bảng giá trị được điền), đánh dấu các bài toán con bị tính lặp lại, và đếm tổng số lời gọi hoặc số ô được tính.

**(3) Triển khai code**

- Viết thân ba hàm trong `chon_qua.py`. Không đổi tên hàm, tham số.
- Không dùng `math.comb`, `math.factorial` hay số thực; được dùng `functools.lru_cache`.
- Xử lý đủ 5 bẫy ở mục 3; `python chon_qua.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 6 mục (các mục về giải pháp chạy trên cả hai hàm `_v1`, `_v2`).
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích nêu ý tưởng và độ phức tạp ở đầu mỗi hàm.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex16`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-16 rồi chép các tệp vào kho: `chon_qua.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `chon_qua.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
