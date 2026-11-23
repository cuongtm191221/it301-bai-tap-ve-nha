# Lỗi công cụ ước lượng chi phí thao tác trên hàng đơn GrabFood

### 1. Bối cảnh nghiệp vụ

![Công cụ ước lượng báo số âm, báo chi phí lấy món cuối còn đắt hơn lấy món đầu, và phóng đại chi phí phục vụ hàng chờ gấp đôi.](minh_hoa.png)

*Công cụ ước lượng báo số âm, báo chi phí lấy món cuối còn đắt hơn lấy món đầu, và phóng đại chi phí phục vụ hàng chờ gấp đôi.*

Bạn là kỹ sư phần mềm trong nhóm hạ tầng của GrabFood.

Giờ cao điểm, hàng đơn chờ nhà hàng xác nhận có tới **200.000 đơn**. Trước khi đổi cách xử lý hàng (ví dụ lấy đơn ở đầu bằng `pop(0)`), nhóm dùng một công cụ **ước lượng số tham chiếu phải dịch** để quyết định. Công cụ có hai hàm:

- `shift_cost(op, n, i)`: số tham chiếu phải dịch khi chạy thao tác trên list n phần tử. `op` là `"append"`, `"pop_end"` (tức `pop()`), `"pop"` (tức `pop(i)`) hoặc `"insert"` (tức `insert(i, x)`). Chỉ số âm tính từ cuối như list. `pop` với chỉ số ngoài khoảng −n đến n − 1 báo `ValueError("chỉ số không hợp lệ")`; `insert` với chỉ số vượt khoảng thì kẹp về 0 hoặc n, giống `list.insert`.
- `queue_cost(n, k)`: tổng số tham chiếu phải dịch khi phục vụ k người đầu hàng (hàng ban đầu n người) bằng k lần `pop(0)`. Hàng ngắn đi một người sau mỗi lần; k lớn hơn n thì chỉ phục vụ được n người.

Kịch bản kiểm tra (đoạn cuối tệp): năm phép tính `shift_cost` trên list 6 phần tử; phục vụ 3 người của hàng 5 người; phục vụ hết hàng 200.000 người.

Kết quả đúng cần hiển thị:

```plaintext
pop(0) trên 6 phần tử: 5
pop(-1) trên 6 phần tử: 0
insert(2, x) trên 6 phần tử: 4
insert(-2, x) trên 6 phần tử: 2
insert(99, x) trên 6 phần tử: 0
Phục vụ 3 người đầu hàng 5 người: 9
Phục vụ hết hàng 200.000 người: 19999900000
```

### 2. Vấn đề hiện tại

Nhóm hạ tầng phản ánh:

- Công cụ báo `pop(-1)` (lấy phần tử cuối) dịch **7** tham chiếu, nhiều hơn cả `pop(0)`.
- `insert(99, x)` trên 6 phần tử bị báo **−1** tham chiếu.
- Con số ước lượng khi phục vụ hết hàng 200.000 người gấp đôi số đo thực tế, làm nhóm suýt mua thêm máy chủ không cần thiết.

Nhắc lại kiến thức (Lesson 03):

- `pop(i)` với 0 ≤ i < n dịch **n − i − 1** tham chiếu (các phần tử sau i dồn trái).
- `insert(i, x)` với 0 ≤ i ≤ n dịch **n − i** tham chiếu (i phần tử đầu giữ nguyên).
- `append` và `pop()` không dịch tham chiếu nào. Chỉ số âm i tương ứng chỉ số i + n.
- Lấy liên tiếp k người ở đầu hàng: lần thứ t (đếm từ 0) dịch n − t − 1 tham chiếu, vì hàng đã ngắn đi t người.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `chi_phi.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Ước lượng chi phí thao tác trên hàng đơn GrabFood trước khi chạy."""
def shift_cost(op, n, i=None):
    # Số tham chiếu phải dịch khi chạy thao tác op trên list n phần tử (Lesson 03).
    # op: "append", "pop_end" (pop()), "pop" (pop(i)), "insert" (insert(i, x)).
    # i âm tính từ cuối. pop với i ngoài -n đến n - 1: ValueError("chỉ số không hợp lệ").
    # insert với i vượt khỏi khoảng thì kẹp vào 0 hoặc n như list.insert.
    if op in ("append", "pop_end"):
        return 0
    if op == "pop":
        if not -n <= i < n:
            raise ValueError("chỉ số không hợp lệ")
        return n - i
    if op == "insert":
        if i > n:
            i = n
        return n - i - 1
    raise ValueError("thao tác không hỗ trợ")


def queue_cost(n, k):
    # Tổng số tham chiếu phải dịch khi phục vụ k người đầu hàng bằng k lần pop(0), hàng ban đầu n người.
    return k * shift_cost("pop", n, 0)


print("pop(0) trên 6 phần tử:", shift_cost("pop", 6, 0))
print("pop(-1) trên 6 phần tử:", shift_cost("pop", 6, -1))
print("insert(2, x) trên 6 phần tử:", shift_cost("insert", 6, 2))
print("insert(-2, x) trên 6 phần tử:", shift_cost("insert", 6, -2))
print("insert(99, x) trên 6 phần tử:", shift_cost("insert", 6, 99))
print("Phục vụ 3 người đầu hàng 5 người:", queue_cost(5, 3))
print("Phục vụ hết hàng 200.000 người:", queue_cost(200000, 200000))
```

Kết quả hiển thị trên Console:

```plaintext
pop(0) trên 6 phần tử: 6
pop(-1) trên 6 phần tử: 7
insert(2, x) trên 6 phần tử: 3
insert(-2, x) trên 6 phần tử: 7
insert(99, x) trên 6 phần tử: -1
Phục vụ 3 người đầu hàng 5 người: 15
Phục vụ hết hàng 200.000 người: 40000000000
```

Đối chiếu với kết quả đúng: cả bảy dòng đều sai: `pop(0)` ra 6 thay vì 5, `pop(-1)` ra 7, `insert(99, x)` ra −1, và hai tổng hàng chờ đều lớn hơn kết quả đúng.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Với list `["A", "B", "C", "D", "E", "F"]`, vẽ các tham chiếu phải dịch khi `pop(0)`, `pop(5)`, `insert(0, x)`, `insert(6, x)`. Từ đó so với công thức trong mã hiện tại.
- Mã hiện tại tính `pop(-1)` thế nào? Chỉ số -1 phải được đổi thành chỉ số nào trước khi áp công thức?
- Vì sao `insert(99, x)` ra số âm? Kẹp chỉ số rồi mới áp công thức thì ra bao nhiêu?
- Vì sao `queue_cost` của mã hiện tại lớn gần gấp đôi kết quả đúng? Viết công thức đóng cho tổng khi k = n.
- Với hàng 200.000 người, so sánh tổng số tham chiếu dịch của hai cách: phục vụ bằng `pop(0)`, và đảo hàng một lần rồi phục vụ bằng `pop()`. Ghi Big-O của mỗi cách.
- Ghi bốn bộ dữ liệu thử: list rỗng, chỉ số -n, insert với chỉ số rất âm, k lớn hơn n; kèm kết quả mong đợi.

**(2) Sửa lỗi**

- Sửa hai hàm trong `chi_phi.py`. Không đổi tên hàm, tham số, thông báo lỗi.
- Chạy `python chi_phi.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex08`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-08 rồi chép các tệp vào kho: `chi_phi.py`, `test_chi_phi.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `chi_phi.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
