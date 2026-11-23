# Lỗi đếm số bước trong báo cáo doanh thu Shopee

### 1. Bối cảnh nghiệp vụ

![Báo cáo doanh thu ghi số bước sai, nhóm hạ tầng không ước lượng được thời gian chạy cho gian hàng lớn.](minh_hoa.png)

*Báo cáo doanh thu ghi số bước sai, nhóm hạ tầng không ước lượng được thời gian chạy cho gian hàng lớn.*

Bạn là kỹ sư phần mềm trong nhóm báo cáo dành cho người bán trên Shopee.

Cuối mỗi ngày, hệ thống chạy hai báo cáo cho từng gian hàng: **tổng doanh thu** và **số đơn lớn** (đơn có giá trị từ 500.000đ trở lên, để gian hàng biết cần đóng gói chống sốc bao nhiêu kiện). Mỗi đơn là một dict:

```plaintext
{"code": "DH2002", "amount": 560000}
```

Gian hàng lớn có hàng trăm nghìn đơn mỗi ngày. Để ước lượng thời gian chạy trước khi bật báo cáo, nhóm hạ tầng yêu cầu mỗi hàm trả thêm **số bước** đã thực hiện, theo đúng quy ước của Lesson 02: **mỗi dòng lệnh được thực hiện là một bước**. Cụ thể:

- Dòng khởi tạo (`total = 0`, `count = 0`): 1 bước.
- Dòng trong thân vòng lặp: mỗi lần chạy là 1 bước. Dòng `if` chạy ở mọi lượt, dù điều kiện đúng hay sai; dòng bên trong `if` chỉ chạy khi điều kiện đúng.
- Dòng `return`: 1 bước.

Dòng `for` và các dòng cộng vào biến `steps` không tính. Với cách đếm này, `total_revenue` có số bước **n + 2** với n đơn.

Ngoài ra, tài liệu kỹ thuật của nhóm ghi Big-O thời gian của hai hàm trong dict `COMPLEXITY`, viết ở dạng **đã rút gọn**.

Kịch bản kiểm tra (đoạn cuối tệp): chạy hai báo cáo trên 5 đơn mẫu, rồi đo số bước trên 1.000 đơn toàn đơn nhỏ và 1.000 đơn toàn đơn lớn.

Kết quả đúng cần hiển thị:

```plaintext
Tổng doanh thu: (2519000, 7)
Đơn từ 500.000đ: (3, 10)
1.000 đơn, tổng doanh thu: 1002 bước
1.000 đơn nhỏ, đếm đơn lớn: 1002 bước
1.000 đơn lớn, đếm đơn lớn: 2002 bước
Big-O: {'total_revenue': 'O(n)', 'count_big_orders': 'O(n)'}
```

### 2. Vấn đề hiện tại

Nhóm hạ tầng phản ánh: theo số bước báo cáo ghi lại, gian hàng 1.000 đơn chỉ tốn **1 bước** để tính tổng doanh thu, điều không thể đúng. Họ đã cấp quá ít thời gian chạy cho đêm sale và báo cáo bị cắt giữa chừng.

Người bán thì phản ánh: số đơn lớn **thiếu**, những đơn đúng 500.000đ không được tính, nên gian hàng chuẩn bị thiếu thùng chống sốc.

Nhắc lại kiến thức (Lesson 02):

- Số bước là một **biểu thức theo n**, ví dụ f(n) = n + 2. Muốn kiểm chứng biểu thức, đặt biến đếm đúng vào chỗ dòng lệnh chạy, rồi chạy với nhiều giá trị n và so với biểu thức.
- **Big-O** giữ số hạng tăng nhanh nhất và bỏ hệ số: n + 2 là O(n); 3n + 5 là O(n); hằng số là O(1).
- Có hàm mà số bước còn phụ thuộc vào dữ liệu (Lesson 03): khi đó ghi số bước theo trường hợp xấu nhất.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `bao_cao.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Báo cáo doanh thu cuối ngày của gian hàng trên Shopee, có đếm số bước."""

# Quy ước đếm: mỗi dòng lệnh được thực hiện là một bước (như bài đọc Lesson 02).


def total_revenue(orders):
    # Tổng tiền các đơn; trả về (tổng tiền, số bước)
    steps = 0
    total = 0
    for order in orders:
        total += order["amount"]
    steps += 1
    return total, steps


def count_big_orders(orders, threshold):
    # Đếm đơn có giá trị từ threshold trở lên; trả về (số đơn, số bước)
    steps = 1            # count = 0
    count = 0
    for order in orders:
        if order["amount"] > threshold:
            count += 1
            steps += 1
    steps += 1           # return
    return count, steps


# Big-O thời gian của hai hàm, ghi trong tài liệu kỹ thuật của nhóm
COMPLEXITY = {
    "total_revenue": "O(n + 2)",
    "count_big_orders": "O(2n + 2)",
}


orders = [
    {"code": "DH2001", "amount": 120000},
    {"code": "DH2002", "amount": 560000},
    {"code": "DH2003", "amount": 500000},
    {"code": "DH2004", "amount": 89000},
    {"code": "DH2005", "amount": 1250000},
]
print("Tổng doanh thu:", total_revenue(orders))
print("Đơn từ 500.000đ:", count_big_orders(orders, 500000))

small = [{"code": "DH", "amount": 100000}] * 1000
big = [{"code": "DH", "amount": 600000}] * 1000
print("1.000 đơn, tổng doanh thu:", total_revenue(small)[1], "bước")
print("1.000 đơn nhỏ, đếm đơn lớn:", count_big_orders(small, 500000)[1], "bước")
print("1.000 đơn lớn, đếm đơn lớn:", count_big_orders(big, 500000)[1], "bước")
print("Big-O:", COMPLEXITY)
```

Kết quả hiển thị trên Console:

```plaintext
Tổng doanh thu: (2519000, 1)
Đơn từ 500.000đ: (2, 4)
1.000 đơn, tổng doanh thu: 1 bước
1.000 đơn nhỏ, đếm đơn lớn: 2 bước
1.000 đơn lớn, đếm đơn lớn: 1002 bước
Big-O: {'total_revenue': 'O(n + 2)', 'count_big_orders': 'O(2n + 2)'}
```

Đối chiếu với kết quả đúng: số bước của `total_revenue` là 1 ở mọi trường hợp thay vì n + 2; số đơn lớn là 2 thay vì 3; số bước của `count_big_orders` chỉ tăng theo số đơn lớn; Big-O trong `COMPLEXITY` chưa rút gọn.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Theo quy ước đếm, liệt kê các dòng lệnh của `total_revenue` được thực hiện với n đơn và số lần chạy của từng dòng. Tổng là bao nhiêu? Biến `steps` trong mã hiện tại đang đếm được dòng nào?
- Lệnh `steps += 1` đặt ngoài vòng lặp thì đếm được mấy lần dù n là 10 hay 1.000? Phải đặt ở đâu?
- Trong `count_big_orders`, dòng `if` chạy bao nhiêu lần với n đơn? Dòng `count += 1` chạy bao nhiêu lần nếu có k đơn lớn? Viết số bước f(n, k).
- Với 1.000 đơn, số bước của `count_big_orders` nhỏ nhất và lớn nhất là bao nhiêu? Mỗi trường hợp xảy ra khi nào?
- Đơn 500.000đ có phải đơn lớn không? Dòng điều kiện nào sai?
- Rút gọn "O(n + 2)" và "O(2n + 2)" theo quy tắc Big-O. Vì sao hai hàm có số bước khác nhau lại có cùng Big-O?
- Nếu gian hàng tăng từ 1.000 lên 10.000 đơn, số bước của `total_revenue` tăng khoảng bao nhiêu lần?

**(2) Sửa lỗi**

- Sửa hai hàm và dict `COMPLEXITY` trong `bao_cao.py`. Không đổi tên hàm, tham số và dạng giá trị trả về; chỉ thêm, bớt, dời các lệnh đếm `steps` và sửa điều kiện.
- Chạy `python bao_cao.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `python kiem_tra.py` phải đạt cả 5 mục.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session01_Ex02`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-01-tong-quan-do-phuc-tap/bai-02 rồi chép các tệp vào kho: `bao_cao.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `bao_cao.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
