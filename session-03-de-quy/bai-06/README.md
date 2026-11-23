# Lỗi tìm giao dịch lớn nhất tháng trên ví MoMo

### 1. Bối cảnh nghiệp vụ

![Màn hình "Giao dịch lớn nhất tháng" báo lỗi với người dùng mới và treo với người dùng chi tiêu tăng dần.](minh_hoa.png)

*Màn hình "Giao dịch lớn nhất tháng" báo lỗi với người dùng mới và treo với người dùng chi tiêu tăng dần.*

Bạn là kỹ sư phần mềm trong nhóm tính năng "Quản lý chi tiêu" của ví MoMo.

Cuối tháng, ứng dụng hiện thẻ **"Giao dịch lớn nhất tháng"** để người dùng biết khoản chi nào đáng chú ý. Giao dịch trong tháng là một list số tiền (đồng), theo thứ tự thời gian:

```plaintext
[150000, 2500000, 49000, 1000000, 320000]
```

Hàm `largest(transactions)` được viết bằng đệ quy trên danh sách (Lesson 02): giao dịch lớn nhất của cả list là số lớn hơn giữa **giao dịch đầu** và **giao dịch lớn nhất của phần còn lại**. Quy định:

- Tháng chưa có giao dịch nào: trả về `None`, ứng dụng ẩn thẻ.
- Không được sửa list giao dịch đầu vào, vì list này còn dùng cho các thẻ thống kê khác.
- Một người dùng có tối đa vài trăm giao dịch mỗi tháng.

Nhiều người dùng mới có thói quen chi tiêu tăng dần trong tháng (đầu tháng mua nhỏ, cuối tháng mua lớn), nên list tăng dần là trường hợp gặp hằng ngày, không phải trường hợp hiếm. Thẻ thống kê được tính lại mỗi khi người dùng mở ứng dụng.

Kịch bản kiểm tra (đoạn cuối tệp): tháng 6 có 5 giao dịch, tháng có một giao dịch, tháng chưa có giao dịch, tháng có 30 giao dịch tăng dần; cuối cùng in lại số giao dịch tháng 6 để chắc list không bị sửa.

Kết quả đúng cần hiển thị:

```plaintext
Giao dịch lớn nhất tháng 6: 2500000
Một giao dịch: 75000
Tháng chưa có giao dịch: None
30 giao dịch tăng dần: 300000
Số giao dịch tháng 6 không đổi: 5
```

### 2. Vấn đề hiện tại

Người dùng và nhóm hạ tầng phản ánh:

- Người dùng mới, chưa có giao dịch, mở màn hình thống kê thì ứng dụng báo lỗi.
- Người dùng có 30 giao dịch tăng dần trong tháng mở màn hình thì **đứng yên** rất lâu; máy chủ thống kê tăng tải bất thường vào cuối tháng.
- Người dùng có giao dịch giảm dần thì vẫn thấy nhanh và đúng.

Nhắc lại kiến thức (Lesson 02, Lesson 04):

- Khuôn đệ quy trên danh sách: cơ sở là danh sách rỗng (hoặc một phần tử, nếu danh sách rỗng đã được xử lý riêng); bước đệ quy xử lý phần tử đầu và gọi lại trên `transactions[1:]`.
- Một tầng gọi đệ quy **hai lần** trên cùng phần còn lại thì số lời gọi nhân đôi sau mỗi tầng: n tầng có thể tới cỡ 2ⁿ lời gọi. Gọi một lần, lưu kết quả vào biến rồi dùng lại thì chỉ còn n lời gọi.
- Mỗi hàm đệ quy phải trả lời đúng **ba câu hỏi** (Lesson 01): (1) trường hợp cơ sở trả đúng chưa; (2) từ kết quả của bài toán nhỏ hơn, phần ghép ra kết quả lớn đúng chưa; (3) mỗi lần gọi có tiến về trường hợp cơ sở không.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `giao_dich_lon.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
def largest(transactions):
    # Số tiền lớn nhất trong list transactions. List rỗng: trả về None.
    if len(transactions) == 1:
        return transactions[0]
    if transactions[0] > largest(transactions[1:]):
        return transactions[0]
    return largest(transactions[1:])


june = [150000, 2500000, 49000, 1000000, 320000]
print("Giao dịch lớn nhất tháng 6:", largest(june))
print("Một giao dịch:", largest([75000]))
print("Tháng chưa có giao dịch:", largest([]))
growing = [10000 * k for k in range(1, 31)]
print("30 giao dịch tăng dần:", largest(growing))
print("Số giao dịch tháng 6 không đổi:", len(june))
```

Kết quả hiển thị trên Console:

```plaintext
Giao dịch lớn nhất tháng 6: 2500000
Một giao dịch: 75000
Traceback (most recent call last):
  ...
    if transactions[0] > largest(transactions[1:]):
IndexError: list index out of range
```

Hai dòng đầu đúng. Tháng chưa có giao dịch gây lỗi `IndexError`, nên dòng 30 giao dịch tăng dần không được chạy tới; khi chạy riêng dòng đó, chương trình đứng yên.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Vì sao `largest([])` gây `IndexError`? Sửa trường hợp cơ sở thế nào để vẫn đúng với list một phần tử?
- Với list `[1, 2, 3]` (tăng dần), vẽ cây lời gọi của mã hiện tại. Có bao nhiêu lời gọi? Làm lại với `[3, 2, 1]` (giảm dần).
- Đếm số lời gọi của mã hiện tại với list tăng dần dài 10, 15, 20 (dùng biến đếm toàn cục). Ghi bảng và giải thích vì sao list giảm dần lại nhanh.
- Sửa phần ghép để mỗi tầng chỉ gọi đệ quy một lần. Sau khi sửa, list dài n cần bao nhiêu lời gọi? Ghi Big-O thời gian.
- Mỗi lời gọi tạo lát cắt `transactions[1:]` dài bao nhiêu? Tổng số phần tử được sao chép với list dài n là bao nhiêu? Có ảnh hưởng gì khi n chỉ vài trăm?
- Ghi bốn bộ dữ liệu thử: list rỗng, một phần tử, tăng dần, có hai giao dịch bằng nhau và lớn nhất; kèm kết quả mong đợi.

**(2) Sửa lỗi**

- Sửa hàm `largest` trong `giao_dich_lon.py`, giữ cách viết đệ quy. Không đổi tên hàm, tham số; không dùng `max()` hay vòng lặp; không sửa list đầu vào.
- 30 giao dịch tăng dần phải có kết quả trong vòng 1 giây.
- Chạy `python giao_dich_lon.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `python kiem_tra.py` phải đạt cả 5 mục.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex06`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-06 rồi chép các tệp vào kho: `giao_dich_lon.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `giao_dich_lon.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
