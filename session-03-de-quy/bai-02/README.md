# Lỗi thống kê chi tiêu tháng trên ví MoMo

### 1. Bối cảnh nghiệp vụ

![Màn hình thống kê báo tổng chi tiêu thấp hơn thực tế, bỏ sót giao dịch lớn, và báo lỗi với người dùng mới.](minh_hoa.png)

*Màn hình thống kê báo tổng chi tiêu thấp hơn thực tế, bỏ sót giao dịch lớn, và báo lỗi với người dùng mới.*

Bạn là kỹ sư phần mềm trong nhóm tính năng "Quản lý chi tiêu" của ví MoMo.

Cuối tháng, ứng dụng hiện **tổng số tiền đã chi** và **số giao dịch lớn** (từ 1.000.000đ trở lên) để nhắc người dùng kiểm soát chi tiêu. Giao dịch trong tháng là một list số tiền (đồng):

```plaintext
[150000, 2500000, 49000, 1000000, 320000]
```

Nhóm viết hai hàm bằng đệ quy trên danh sách, theo khuôn của Lesson 02: tách **phần tử đầu** `transactions[0]` và **phần còn lại** `transactions[1:]`, giải bài toán trên phần còn lại rồi ghép với phần tử đầu.

- `total_amount(transactions)`: tổng số tiền. Tháng chưa có giao dịch thì tổng là 0.
- `count_large(transactions, limit)`: số giao dịch có số tiền **từ `limit` trở lên**.

Con số này được dùng để gửi thông báo nhắc chi tiêu và để gợi ý hạn mức. Tổng sai làm người dùng mất niềm tin vào ứng dụng; báo lỗi với người dùng mới thì họ gỡ ứng dụng ngay trong tuần đầu. Nhóm sản phẩm yêu cầu sửa cả hai hàm và giữ cách viết đệ quy để thống nhất với các hàm thống kê khác của nhóm.

Kịch bản kiểm tra (đoạn cuối tệp): tháng có 5 giao dịch, tháng có một giao dịch, tháng chưa có giao dịch nào.

Kết quả đúng cần hiển thị:

```plaintext
Tổng chi tiêu tháng: 4019000
Số giao dịch từ 1.000.000đ: 2
Một giao dịch: 75000 0
Tháng chưa có giao dịch: 0 0
```

### 2. Vấn đề hiện tại

Người dùng phản ánh:

- Tổng chi tiêu tháng hiện **519.000đ**, trong khi chỉ riêng một giao dịch đã là 2.500.000đ.
- Giao dịch đúng **1.000.000đ** không được tính là giao dịch lớn.
- Người dùng mới mở tài khoản, chưa có giao dịch nào, mở màn hình thống kê thì ứng dụng báo lỗi.

Nhắc lại kiến thức (Lesson 02):

- Khuôn chung cho danh sách: cơ sở là **danh sách rỗng**; bước đệ quy xử lý `transactions[0]` rồi gọi lại trên `transactions[1:]`, ngắn hơn đúng một phần tử.
- Chọn cơ sở là danh sách **một phần tử** là lỗi thường gặp: danh sách rỗng không bao giờ gặp cơ sở đó.
- Mỗi hàm đệ quy phải trả lời đúng **ba câu hỏi** (Lesson 01): (1) trường hợp cơ sở trả đúng chưa; (2) từ kết quả của bài toán nhỏ hơn, phần ghép ra kết quả lớn đúng chưa; (3) mỗi lần gọi có tiến về trường hợp cơ sở không.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `chi_tieu.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
def total_amount(transactions):
    # Tổng số tiền các giao dịch (đơn vị: đồng).
    if len(transactions) == 1:
        return transactions[0]
    return transactions[0] + total_amount(transactions[2:])


def count_large(transactions, limit):
    # Số giao dịch có số tiền từ limit trở lên (để gửi cảnh báo chi tiêu lớn).
    if len(transactions) == 0:
        return 0
    if transactions[0] > limit:
        return 1 + count_large(transactions[1:], limit)
    return count_large(transactions[1:], limit)


month = [150000, 2500000, 49000, 1000000, 320000]
print("Tổng chi tiêu tháng:", total_amount(month))
print("Số giao dịch từ 1.000.000đ:", count_large(month, 1000000))
print("Một giao dịch:", total_amount([75000]), count_large([75000], 1000000))
print("Tháng chưa có giao dịch:", total_amount([]), count_large([], 1000000))
```

Kết quả hiển thị trên Console:

```plaintext
Tổng chi tiêu tháng: 519000
Số giao dịch từ 1.000.000đ: 1
Một giao dịch: 75000 0
Traceback (most recent call last):
  ...
    return transactions[0] + total_amount(transactions[2:])
IndexError: list index out of range
```

Đối chiếu với kết quả đúng: tổng 5 giao dịch ra 519.000đ thay vì 4.019.000đ; số giao dịch lớn là 1 thay vì 2; tháng chưa có giao dịch gây lỗi `IndexError` nên dòng cuối không được in.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Chạy tay `total_amount` trên 5 giao dịch mẫu của mã hiện tại: ghi danh sách được truyền vào ở mỗi lời gọi. Những giao dịch nào bị bỏ qua? Vì sao?
- Với 4 giao dịch, `total_amount` của mã hiện tại có gặp được cơ sở `len == 1` không? Chuyện gì xảy ra?
- Vì sao `total_amount([])` báo `IndexError`? Viết lại trường hợp cơ sở theo khuôn của Lesson 02 và kiểm tra lại với danh sách 1 phần tử.
- Điều kiện nào trong `count_large` sai với quy định "từ 1.000.000đ trở lên"?
- Trả lời ba câu hỏi kiểm tra cho hai hàm sau khi sửa.
- Mỗi lời gọi tạo một lát cắt `transactions[1:]`. Với n giao dịch, có bao nhiêu lời gọi? Vì sao không dùng cách này cho danh sách hàng nghìn giao dịch (Lesson 03)?
- Ghi ba bộ dữ liệu thử cho `count_large`: một giao dịch đúng bằng hạn mức, một giao dịch nhỏ hơn hạn mức một đồng, danh sách rỗng; kèm kết quả mong đợi.

**(2) Sửa lỗi**

- Sửa hai hàm trong `chi_tieu.py`, giữ cách viết đệ quy. Không đổi tên hàm, tham số; không dùng vòng lặp hay `sum()`; không sửa list đầu vào.
- Chạy `python chi_tieu.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `python kiem_tra.py` phải đạt cả 4 mục.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex02`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-02 rồi chép các tệp vào kho: `chi_tieu.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `chi_tieu.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
