# Lỗi tính điểm thưởng chuỗi ngày điểm danh trên ví MoMo

### 1. Bối cảnh nghiệp vụ

![Người dùng điểm danh 7 ngày liền chỉ được 27 điểm, chưa điểm danh ngày nào thì ứng dụng báo lỗi.](minh_hoa.png)

*Người dùng điểm danh 7 ngày liền chỉ được 27 điểm, chưa điểm danh ngày nào thì ứng dụng báo lỗi.*

Bạn là kỹ sư phần mềm trong nhóm chương trình khách hàng thân thiết của ví điện tử MoMo.

Người dùng **điểm danh** mỗi ngày trên ứng dụng để nhận điểm thưởng. Chuỗi càng dài thì điểm mỗi ngày càng cao: **ngày thứ k của chuỗi được 100 × k điểm**. Ví dụ chuỗi 3 ngày được 100 + 200 + 300 = 600 điểm. Người dùng chưa điểm danh ngày nào (chuỗi 0 ngày) được 0 điểm.

Nhóm viết hàm `streak_points(n)` theo cách đệ quy: tổng điểm của chuỗi n ngày bằng tổng điểm của chuỗi n - 1 ngày cộng điểm của ngày thứ n.

Cùng tệp có hàm `count_digits(n)` đếm số chữ số của một số tiền nguyên dương, dùng để căn lề cột số tiền trên sao kê: 7 có 1 chữ số, 45000 có 5 chữ số. Cách đệ quy: bỏ chữ số cuối (`n // 10`) thì được số ngắn hơn một chữ số.

Điểm thưởng được cộng vào ví ngay khi người dùng điểm danh, nên sai một con số là sai tiền thật của hàng trăm nghìn người dùng mỗi ngày. Bộ phận chăm sóc khách hàng đã nhận nhiều phản ánh và cần bản sửa trước đợt khuyến mãi cuối tuần.

Kịch bản kiểm tra (đoạn cuối tệp): đếm chữ số của ba số tiền, rồi tính điểm của chuỗi 1, 3, 7 và 0 ngày.

Kết quả đúng cần hiển thị:

```plaintext
Số chữ số của 7: 1
Số chữ số của 45000: 5
Số chữ số của 1250000: 7
Chuỗi 1 ngày: 100 điểm
Chuỗi 3 ngày: 600 điểm
Chuỗi 7 ngày: 2800 điểm
Chuỗi 0 ngày: 0 điểm
```

### 2. Vấn đề hiện tại

Người dùng phản ánh:

- Điểm danh **7 ngày** liền chỉ được **27 điểm**, trong khi bảng quy định ghi 2.800 điểm.
- Người dùng mới, chưa điểm danh ngày nào, mở màn hình điểm thưởng thì ứng dụng báo lỗi.
- Cột số tiền trên sao kê bị lệch: số 7 được coi là có 0 chữ số.

Nhắc lại kiến thức (Lesson 01, Lesson 03):

- Mỗi hàm đệ quy phải trả lời đúng **ba câu hỏi** (Lesson 01): (1) trường hợp cơ sở trả đúng chưa; (2) từ kết quả của bài toán nhỏ hơn, phần ghép ra kết quả lớn đúng chưa; (3) mỗi lần gọi có tiến về trường hợp cơ sở không.
- Trường hợp cơ sở phải bao phủ **đầu vào hợp lệ nhỏ nhất**. Nếu cơ sở bỏ sót một đầu vào hợp lệ, lời gọi với đầu vào đó không bao giờ gặp cơ sở, cứ gọi tiếp mãi cho tới khi Python báo `RecursionError`.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `diem_thuong.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
def streak_points(n):
    # Tổng điểm thưởng của chuỗi n ngày điểm danh liên tiếp: ngày thứ k được 100 x k điểm.
    # n = 0 (chưa điểm danh) thì được 0 điểm.
    if n == 1:
        return 0
    return streak_points(n - 1) + n


def count_digits(n):
    # Số chữ số của số nguyên dương n (dùng để căn lề cột số tiền trên sao kê).
    if n < 10:
        return 0
    return 1 + count_digits(n // 10)


for amount in [7, 45000, 1250000]:
    print(f"Số chữ số của {amount}:", count_digits(amount))
for n in [1, 3, 7, 0]:
    print(f"Chuỗi {n} ngày:", streak_points(n), "điểm")
```

Kết quả hiển thị trên Console:

```plaintext
Số chữ số của 7: 0
Số chữ số của 45000: 4
Số chữ số của 1250000: 6
Chuỗi 1 ngày: 0 điểm
Chuỗi 3 ngày: 5 điểm
Chuỗi 7 ngày: 27 điểm
Traceback (most recent call last):
  ...
    if n == 1:
RecursionError: maximum recursion depth exceeded in comparison
```

Đối chiếu với kết quả đúng: số chữ số đều thiếu 1; chuỗi 1, 3, 7 ngày ra 0, 5, 27 điểm thay vì 100, 600, 2.800; chuỗi 0 ngày gây `RecursionError`.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Trả lời ba câu hỏi kiểm tra cho `streak_points` của mã hiện tại. Câu nào sai, sai ở dòng nào?
- Chạy tay `streak_points(3)` của mã hiện tại: ghi từng lời gọi và giá trị trả về khi quay lên. Vì sao ra 5?
- Với `streak_points(0)`, lời gọi tiếp theo là gì? Vì sao không bao giờ gặp trường hợp cơ sở? Sửa trường hợp cơ sở thế nào?
- Phần ghép `+ n` sai với quy định điểm ở chỗ nào? Viết lại phần ghép.
- Trả lời ba câu hỏi kiểm tra cho `count_digits`. Số có một chữ số phải trả về bao nhiêu?
- Với chuỗi n ngày, `streak_points(n)` gọi đệ quy bao nhiêu lần? Ghi Big-O thời gian.
- Ghi ba bộ dữ liệu thử (gồm đầu vào nhỏ nhất) bạn dùng để khẳng định mỗi hàm đã đúng, kèm kết quả mong đợi.

**(2) Sửa lỗi**

- Sửa hai hàm trong `diem_thuong.py`, giữ cách viết đệ quy. Không đổi tên hàm, tham số; không dùng vòng lặp, `sum()` hay `len(str(n))`.
- Chạy `python diem_thuong.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `python kiem_tra.py` phải đạt cả 4 mục.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex01`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-01 rồi chép các tệp vào kho: `diem_thuong.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `diem_thuong.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
