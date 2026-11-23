# Lỗi băng chuyền đóng gói kho Tiki cài bằng list đổi đầu cuối

### 1. Bối cảnh nghiệp vụ

![Màn hình báo nhầm đơn tiếp theo, lấy lô đơn khi băng chuyền sắp hết thì sập, giờ cao điểm thêm đơn chậm dần.](minh_hoa.png)

*Màn hình báo nhầm đơn tiếp theo, lấy lô đơn khi băng chuyền sắp hết thì sập, giờ cao điểm thêm đơn chậm dần.*

Bạn là kỹ sư phần mềm trong nhóm vận hành kho của Tiki.

**Băng chuyền đóng gói** nhận đơn theo thứ tự; đơn vào trước được đóng gói trước. Máy đóng gói tự động lấy **theo lô** (ví dụ 3 đơn một lần). Một bạn trong nhóm biết `pop(0)` chậm, nên cài hàng đợi bằng list theo cách "đổi đầu cuối": **thêm ở đầu list** bằng `insert(0, ...)`, **lấy ở cuối list** bằng `pop()`.

Đặc tả của lớp `PackingLine`:

- `enqueue(order)`, `dequeue()`: thêm đơn, lấy đơn theo thứ tự vào trước ra trước; rỗng thì `dequeue()` trả `None`.
- `peek()`: đơn **sẽ được đóng gói tiếp theo**; rỗng trả `None`.
- `take_batch(k)`: lấy **tối đa** k đơn theo thứ tự; còn ít hơn k thì lấy hết, rỗng thì trả list rỗng.
- `size()`: số đơn đang chờ.

Giờ cao điểm ngày khuyến mãi, băng chuyền nhận tới **200.000 đơn**. Máy quét phải ghi nhận mỗi đơn vào băng chuyền ngay lập tức, nếu không, đơn bị quét trùng hoặc bỏ sót.

Kịch bản kiểm tra (đoạn cuối tệp): bốn đơn vào; xem đơn tiếp theo; lấy lô 3 đơn; lấy lô 3 đơn tiếp (chỉ còn 1); thêm 200.000 đơn rồi xem đơn tiếp theo và lấy lô 2 đơn.

Kết quả đúng cần hiển thị:

```plaintext
Đơn tiếp theo: TK201
Lô 3 đơn: ['TK201', 'TK202', 'TK203']
Lô 3 đơn tiếp: ['TK204'] | còn: 0
200.000 đơn, đơn tiếp theo: TK0 | lô 2 đơn: ['TK0', 'TK1']
```

### 2. Vấn đề hiện tại

Nhân viên kho phản ánh:

- Màn hình "Đơn tiếp theo" hiện **đơn vừa vào** thay vì đơn đứng đầu.
- Lấy lô khi băng chuyền còn ít đơn hơn kích thước lô thì máy **sập**.
- Giờ cao điểm, mỗi lần quét đơn vào băng chuyền chậm dần.

Nhắc lại kiến thức (Lesson 03, Lesson 04):

- Đổi đầu cuối của list (thêm ở đầu, lấy ở cuối) **vẫn chậm**: `insert(0, x)` dịch cả dãy, O(n). "Đổi đầu cuối của list mà vẫn chậm" là lỗi thường gặp.
- Hàng đợi cần thêm một đầu, lấy đầu kia, cả hai O(1): dùng chuỗi nút có head và tail, hoặc `collections.deque` với `append` và `popleft`.
- Khi đổi cách lưu, mọi thao tác đọc "đầu hàng" phải đổi theo.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `bang_chuyen.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Băng chuyền đóng gói ở kho Tiki: hàng đợi cài bằng list đổi đầu cuối."""
class PackingLine:
    # Băng chuyền đóng gói ở kho Tiki: đơn vào trước được đóng gói trước.
    # Bản cài bằng list: thêm đơn ở đầu list, lấy đơn ở cuối list.
    # peek() là đơn sẽ được đóng gói tiếp theo; take_batch(k) lấy tối đa k đơn theo thứ tự;
    # rỗng thì peek() trả None, take_batch trả list rỗng.
    def __init__(self):
        self._items = []

    def enqueue(self, order):
        self._items.insert(0, order)

    def dequeue(self):
        if not self._items:
            return None
        return self._items.pop()

    def peek(self):
        if not self._items:
            return None
        return self._items[0]

    def take_batch(self, k):
        batch = []
        for _ in range(k):
            batch.append(self._items.pop())
        return batch

    def size(self):
        return len(self._items)


line = PackingLine()
for code in ("TK201", "TK202", "TK203", "TK204"):
    line.enqueue(code)
print("Đơn tiếp theo:", line.peek())
print("Lô 3 đơn:", line.take_batch(3))
print("Lô 3 đơn tiếp:", line.take_batch(3), "| còn:", line.size())
big = PackingLine()
for k in range(200000):
    big.enqueue(f"TK{k}")
print("200.000 đơn, đơn tiếp theo:", big.peek(), "| lô 2 đơn:", big.take_batch(2))
```

Kết quả hiển thị trên Console:

```plaintext
Đơn tiếp theo: TK204
Lô 3 đơn: ['TK201', 'TK202', 'TK203']
Traceback (most recent call last):
  ...
    batch.append(self._items.pop())
IndexError: pop from empty list
```

Đối chiếu với kết quả đúng: "Đơn tiếp theo" là TK204 thay vì TK201; lô đầu đúng, nhưng lô thứ hai gây `IndexError`, nên các dòng sau không được in.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Ghi `_items` sau bốn lần `enqueue` của mã hiện tại. Đơn đứng đầu hàng nằm ở chỉ số nào? `peek` đang đọc chỉ số nào?
- Vì sao `take_batch(3)` lần thứ hai gây lỗi? Sửa để lấy tối đa k đơn.
- Mỗi lần `enqueue` của mã hiện tại dịch bao nhiêu tham chiếu? Tổng khi thêm 200.000 đơn? Đo thời gian thêm 20.000, 40.000, 80.000 đơn.
- Chọn cách lưu mới để `enqueue`, `dequeue`, `peek` đều O(1). Khi đổi cách lưu, những phương thức nào phải viết lại?
- Ghi Big-O của `take_batch(k)` sau khi sửa.
- Ghi bốn bộ dữ liệu thử: băng chuyền rỗng, lô lớn hơn số đơn, lô bằng 0, thêm xen kẽ lấy; kèm kết quả mong đợi.
- Nếu giữ list nhưng thêm ở cuối và lấy bằng `pop(0)`, chi phí thay đổi thế nào so với mã hiện tại? Cách nào trong hai cách đều không đạt?

**(2) Sửa lỗi**

- Sửa lớp `PackingLine` trong `bang_chuyen.py`. Không đổi tên lớp, phương thức, dạng giá trị trả về. Được đổi cách lưu bên trong.
- Thêm 200.000 đơn phải xong trong 1 giây.
- Chạy `python bang_chuyen.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex08`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-08 rồi chép các tệp vào kho: `bang_chuyen.py`, `test_bang_chuyen.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `bang_chuyen.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
