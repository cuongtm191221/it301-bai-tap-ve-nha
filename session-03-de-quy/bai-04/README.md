# Lỗi tính số tháng tiết kiệm "Heo đất" trên ví MoMo

### 1. Bối cảnh nghiệp vụ

![Người dùng đặt mục tiêu tiết kiệm thì ứng dụng báo lỗi, góp 0đ mỗi tháng hay mục tiêu lớn thì sập.](minh_hoa.png)

*Người dùng đặt mục tiêu tiết kiệm thì ứng dụng báo lỗi, góp 0đ mỗi tháng hay mục tiêu lớn thì sập.*

Bạn là kỹ sư phần mềm trong nhóm tính năng tiết kiệm "Heo đất" của ví MoMo.

Người dùng đặt **mục tiêu** (ví dụ 5.000.000đ), cho biết **số dư hiện có** và **số tiền góp mỗi tháng**. Ứng dụng hiện: "Bạn cần thêm N tháng để đạt mục tiêu". Quy tắc:

- Số dư đã **bằng hoặc vượt** mục tiêu thì cần 0 tháng.
- Mỗi tháng số dư tăng thêm đúng số tiền góp; tháng nào số dư bằng hoặc vượt mục tiêu thì dừng đếm.
- Góp 0đ hoặc số âm thì không bao giờ đạt: hàm trả về `None` để ứng dụng hiện lời nhắc tăng số tiền góp.

Hàm `months_to_goal(balance, goal, monthly)` được viết bằng đệ quy: số tháng từ số dư hiện tại bằng 1 cộng số tháng từ số dư của tháng sau. Có người dùng đặt mục tiêu 100 triệu đồng với mức góp 50.000đ mỗi tháng, tức **2.000 tháng**.

Con số này hiện ngay trên màn hình đặt mục tiêu, nên lỗi ở đây làm người dùng bỏ dở việc mở Heo đất. Nhóm sản phẩm muốn hàm trả lời đúng với mọi mục tiêu, kể cả mục tiêu dài hạn như mua nhà hay quỹ hưu trí.

Kịch bản kiểm tra (đoạn cuối tệp): số dư vừa đủ, ví dụ cần 5 tháng, số dư đã vượt mục tiêu, góp 0đ mỗi tháng, và mục tiêu 100 triệu đồng.

Kết quả đúng cần hiển thị:

```plaintext
Vừa đủ tiền: 0 tháng
Mục tiêu 5.000.000đ, đang có 1.000.000đ, góp 800.000đ/tháng: 5 tháng
Đã đủ tiền: 0 tháng
Góp 0đ mỗi tháng: None
Mục tiêu 100 triệu, góp 50.000đ/tháng: 2000 tháng
```

### 2. Vấn đề hiện tại

Người dùng và nhóm hạ tầng phản ánh:

- Đặt mục tiêu bình thường thì màn hình báo lỗi `TypeError`.
- Số dư đã **vượt** mục tiêu hoặc góp vượt ở tháng cuối thì ứng dụng chạy mãi rồi báo `RecursionError`.
- Nhập nhầm mức góp 0đ thì ứng dụng cũng báo `RecursionError` thay vì nhắc tăng mức góp.
- Mục tiêu 100 triệu đồng góp 50.000đ mỗi tháng thì báo `RecursionError`, dù mọi thứ khác đều đúng.

Nhắc lại kiến thức (Lesson 03):

- Ba lỗi thường gặp khi viết đệ quy: **cơ sở bỏ sót đầu vào hợp lệ**, **lời gọi không tiến về cơ sở**, **quên `return` ở bước đệ quy** (hàm trả về `None` và phép cộng ở tầng trên báo `TypeError`).
- Mỗi lời gọi chưa xong là một khung trên call stack; đệ quy n tầng tốn O(n) bộ nhớ. Python mặc định cho khoảng 1.000 tầng (`sys.getrecursionlimit()`). Khi n có thể lên hàng nghìn, dùng **vòng lặp** với bộ nhớ O(1).

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `tiet_kiem.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
def months_to_goal(balance, goal, monthly):
    # Số tháng góp thêm monthly đồng mỗi tháng để số dư balance đạt ít nhất goal.
    # Đã đủ thì 0 tháng. monthly không dương thì không bao giờ đạt: trả về None.
    if balance == goal:
        return 0
    months_to_goal(balance + monthly, goal, monthly) + 1


print("Vừa đủ tiền:", months_to_goal(5000000, 5000000, 800000), "tháng")
print("Mục tiêu 5.000.000đ, đang có 1.000.000đ, góp 800.000đ/tháng:", months_to_goal(1000000, 5000000, 800000), "tháng")
print("Đã đủ tiền:", months_to_goal(6000000, 5000000, 800000), "tháng")
print("Góp 0đ mỗi tháng:", months_to_goal(1000000, 5000000, 0))
print("Mục tiêu 100 triệu, góp 50.000đ/tháng:", months_to_goal(0, 100000000, 50000), "tháng")
```

Kết quả hiển thị trên Console:

```plaintext
Vừa đủ tiền: 0 tháng
Traceback (most recent call last):
  ...
  [Previous line repeated 1 more time]
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

Dòng đầu (số dư vừa đủ) đúng. Ngay ở ví dụ cần 5 tháng, chương trình dừng với lỗi `TypeError`, nên mọi dòng sau không được in.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Chạy tay lời gọi ví dụ (1.000.000đ, mục tiêu 5.000.000đ, góp 800.000đ): ghi số dư ở mỗi tầng và giá trị mỗi tầng trả về. Tầng nào trả về `None`, vì sao? Vì sao lỗi lại là `TypeError`?
- Với số dư 0đ, mục tiêu 1.000.000đ, góp 300.000đ, điều kiện `balance == goal` có bao giờ đúng không? Chuyện gì xảy ra? Sửa cơ sở thế nào?
- Với mức góp 0đ, lời gọi đệ quy có tiến về cơ sở không? Cần kiểm tra gì, đặt ở đâu?
- Sau khi sửa ba lỗi trên, mục tiêu 100 triệu góp 50.000đ/tháng cần bao nhiêu tầng đệ quy? Vì sao vẫn báo `RecursionError`?
- Viết lại hàm bằng vòng lặp. So sánh bộ nhớ phụ (Big-O) của cách đệ quy và cách vòng lặp với n tháng.
- Vì sao không nên giải quyết bằng `sys.setrecursionlimit(100000)`?
- Ghi bốn bộ dữ liệu thử: số dư vượt mục tiêu, góp vượt ở tháng cuối, góp 0đ, mục tiêu cần 20.000 tháng; kèm kết quả mong đợi.

**(2) Sửa lỗi**

- Sửa hàm `months_to_goal` trong `tiet_kiem.py`. Không đổi tên hàm, tham số và dạng giá trị trả về. Hàm phải tính được cả mục tiêu cần hàng chục nghìn tháng.
- Chạy `python tiet_kiem.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `python kiem_tra.py` phải đạt cả 5 mục.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex04`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-04 rồi chép các tệp vào kho: `tiet_kiem.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `tiet_kiem.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
