# Giải nén chuỗi lệnh di chuyển cho robot kho Tiki

### 1. Bối cảnh & Vấn đề

![Robot xếp hàng nhận chuỗi lệnh nén như 2[L3[R]]D; bộ giải nén phải đúng, từ chối chuỗi sai và chịu được chuỗi lồng rất sâu.](minh_hoa.png)

*Robot xếp hàng nhận chuỗi lệnh nén như 2[L3[R]]D; bộ giải nén phải đúng, từ chối chuỗi sai và chịu được chuỗi lồng rất sâu.*

Robot xếp hàng trong kho Tiki di chuyển theo chuỗi lệnh `L` (trái), `R` (phải), `U` (lên), `D` (xuống). Để gửi qua mạng không dây cho nhanh, hệ thống điều khiển **nén** đoạn lặp: `k[...]` nghĩa là lặp k lần phần trong ngoặc, có thể lồng nhau:

```plaintext
3[R]U      -> RRRU
2[L3[R]]D  -> LRRRLRRRD
10[U]      -> UUUUUUUUUU
```

Bộ điều khiển trên robot phải **giải nén** trước khi chạy. Chuỗi sai cú pháp (thiếu ngoặc, ngoặc thừa, số 0, số không có ngoặc đi kèm, ký tự lạ) phải bị **từ chối**, vì robot chạy sai lệnh có thể đâm vào kệ. Do lỗi của phần mềm sinh lệnh cũ, đôi khi chuỗi gửi tới có tới **3.000 tầng ngoặc lồng nhau**.

Robot có bộ nhớ hạn chế và phải bắt đầu chạy ngay sau khi nhận lệnh; nếu bộ giải nén báo lỗi giữa chừng vì chuỗi lồng quá sâu, robot đứng yên và chặn lối đi của các robot khác, cả dãy kệ phải dừng chờ kỹ thuật viên. Nhóm vận hành yêu cầu: hoặc giải nén đúng, hoặc từ chối ngay với thông báo rõ ràng, không bao giờ dừng giữa chừng vì lỗi của chính bộ giải nén.

Cấu trúc lồng nhau gợi ý hai hướng rất khác nhau. Trưởng nhóm yêu cầu bạn đề xuất ít nhất hai giải pháp, đo, so sánh rồi mới chọn cách cho robot.

### 2. Yêu cầu nghiệp vụ

**2.1. `decode_v1(commands)` và `decode_v2(commands)`**: mỗi hàm cài một giải pháp, trả về chuỗi lệnh đầy đủ; số lần lặp là số nguyên dương, có thể nhiều chữ số; `k[]` là chuỗi rỗng; chỉ được có các ký tự `L`, `R`, `U`, `D`, chữ số và hai dấu ngoặc vuông; chuỗi sai báo `ValueError("Chuỗi lệnh không hợp lệ")`. Hai hàm cho cùng kết quả nhưng **khác nhau về cách làm**.

**2.2. `route_message(commands)`**: dùng giải pháp bạn chọn; chuỗi dài quá 12 bước thì chỉ in 12 bước đầu và dấu `...`:

```plaintext
9 bước: LRRRLRRRD
20 bước: RRRRRRRRRRRR...
Từ chối: Chuỗi lệnh không hợp lệ
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Số nhiều chữ số, ngoặc rỗng.** `10[U]`; `R2[]L` là `RL`; chuỗi rỗng là chuỗi rỗng.

**Bẫy 2 — Ngoặc sai.** `3[R` (thiếu đóng), `2]R` (đóng thừa), `R][`.

**Bẫy 3 — Số sai chỗ.** `[R]` (thiếu số), `0[R]`, `3R` (số không có ngoặc), `2[R]3` (số ở cuối).

**Bẫy 4 — Ký tự lạ.** `2[x]`.

**Bẫy 5 — Lồng 3.000 tầng.** `1[1[...1[R]...]]` với 3.000 tầng: `route_message` trả `1 bước: R` trong 2 giây, không báo `RecursionError`. Hai giải pháp vẫn phải cho cùng kết quả trên 200 chuỗi ngẫu nhiên lồng tối đa 3 tầng; chỉ giải pháp bạn chọn cho `route_message` phải chịu được chuỗi lồng sâu.

**Kịch bản chạy thử.** Chạy `python lenh_robot.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
'3[R]U'      -> 4 bước: RRRU
'2[L3[R]]D'  -> 9 bước: LRRRLRRRD
'10[U]'      -> 10 bước: UUUUUUUUUU
'R2[]L'      -> 2 bước: RL
'3[R'        -> Từ chối: Chuỗi lệnh không hợp lệ
'2]R'        -> Từ chối: Chuỗi lệnh không hợp lệ
'0[R]'       -> Từ chối: Chuỗi lệnh không hợp lệ
'2[x]'       -> Từ chối: Chuỗi lệnh không hợp lệ
Lồng 3.000 tầng: 1 bước: R
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ ba phần sau:

**(1) Đề xuất và phân tích nhiều giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output của các hàm: kiểu dữ liệu đầu vào, giá trị trả về trong trường hợp thường và trong từng bẫy.
- Đề xuất **ít nhất hai giải pháp** khác nhau về cách làm cho việc giải nén chuỗi lệnh. Với mỗi giải pháp: mô tả ý tưởng trong 2–3 câu, minh họa trên ví dụ ở mục 1, viết mã giả.
- Đo thời gian hai giải pháp bằng `timeit` với chuỗi có 1.000, 2.000, 4.000 tầng `1[...]` và chuỗi phẳng 100.000 ký tự; ghi bảng số đo, phiên bản Python và máy đo. Đếm thêm số phép cộng hoặc số tham chiếu phải dịch bằng một biến đếm.
- So sánh các giải pháp theo bảng 5 tiêu chí: thời gian (Big-O), bộ nhớ phụ (Big-O), kết quả đo, độ dễ đọc và dễ bảo trì, mức phù hợp với bối cảnh của bài.
- Chọn giải pháp dùng cho `route_message` và nêu lý do dựa trên bảng so sánh. Lựa chọn không có lý do không được tính điểm.

**(2) Chạy tay**

- Với mỗi giải pháp, chạy tay `2[L3[R]]D`: ghi dữ liệu trung gian (cấu trúc phụ hoặc các lời gọi và giá trị trả về) theo từng ký tự.

**(3) Triển khai code**

- Viết thân ba hàm trong `lenh_robot.py`. Không đổi tên hàm, tham số.
- Không dùng `eval`, `re`
- Xử lý đủ 5 bẫy ở mục 3; `python lenh_robot.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 6 test có sẵn (các test về giải pháp chạy trên cả hai hàm `_v1`, `_v2`).
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích nêu ý tưởng và độ phức tạp ở đầu mỗi hàm.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex16`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-16 rồi chép các tệp vào kho: `lenh_robot.py`, `test_lenh_robot.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `lenh_robot.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
