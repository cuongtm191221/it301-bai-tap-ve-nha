# Lỗi hàng chờ đóng gói ở kho Tiki cài bằng chuỗi nút

### 1. Bối cảnh nghiệp vụ

![Ba đơn vào hàng chờ đóng gói nhưng chỉ đóng được hai, đơn thứ hai biến mất khỏi hàng.](minh_hoa.png)

*Ba đơn vào hàng chờ đóng gói nhưng chỉ đóng được hai, đơn thứ hai biến mất khỏi hàng.*

Bạn là kỹ sư phần mềm trong nhóm vận hành kho của Tiki.

Đơn hàng sau khi nhặt đủ sản phẩm được đưa vào **hàng chờ đóng gói**: đơn vào trước được đóng gói trước. Nhóm cài hàng đợi bằng **chuỗi nút có head và tail** theo Lesson 03, mục 2.3: đơn mới gắn vào sau `tail`, đơn được đóng gói lấy ở `head`.

Đặc tả của lớp `PackingQueue`:

- `enqueue(order)`: thêm đơn vào cuối hàng (như `add_last`), O(1).
- `dequeue()`: lấy đơn đầu hàng (như `remove_first`), O(1).
- `peek()`: xem đơn **đầu hàng** (đơn sẽ được đóng gói tiếp theo).
- `size()`: số đơn đang chờ.
- Hàng rỗng: `dequeue()` và `peek()` báo `IndexError("hàng đợi rỗng")`.

Trong một ca, hàng chờ có lúc rỗng (đóng gói kịp) rồi lại có đơn mới, nên mọi thao tác phải đúng cả khi hàng vừa hết.

Lỗi ở đây rất khó thấy vì chuỗi nút vẫn "trông" bình thường khi chỉ có một, hai đơn; nhóm cần chạy tay kỹ từng bước.

Kịch bản kiểm tra (đoạn cuối tệp): ba đơn vào hàng; xem đầu hàng; đóng gói ba đơn; khi hàng đã rỗng, thêm hai đơn mới rồi đóng gói.

Kết quả đúng cần hiển thị:

```plaintext
Đầu hàng: TK101 | số đơn: 3
Đóng gói: TK101 TK102 TK103
Sau khi hàng rỗng, thêm 2 đơn: TK104 TK105 | còn: 0
```

### 2. Vấn đề hiện tại

Nhân viên đóng gói phản ánh:

- Ba đơn vào hàng nhưng chỉ đóng được hai; đơn **TK102** không bao giờ xuất hiện, màn hình báo "hàng đợi rỗng" trong khi số đơn vẫn còn.
- Sau khi sửa tạm phần trên, nhóm kiểm thử tiếp và thấy: hàng vừa rỗng mà có đơn mới vào thì đơn đó không đóng gói được.
- Màn hình "Đơn tiếp theo" có lúc hiện đơn vừa vào thay vì đơn đứng đầu.

Nhắc lại kiến thức (Lesson 03):

- `enqueue`: hàng rỗng thì nút mới vừa là head vừa là tail; ngược lại gắn vào sau tail. Trong **cả hai** trường hợp, tail phải trỏ tới nút mới.
- `dequeue`: lấy ở head; nếu vừa lấy nút cuối cùng (head thành `None`) thì **tail cũng về `None`**. "Lấy phần tử cuối cùng mà quên đưa tail về None" là lỗi thường gặp.
- head là đầu hàng (ra), tail là cuối hàng (vào).

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `hang_dong_goi.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Hàng chờ đóng gói ở kho Tiki, cài hàng đợi bằng chuỗi nút."""
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class PackingQueue:
    # Hàng chờ đóng gói ở kho Tiki, cài bằng chuỗi nút: đơn vào ở tail, ra ở head.
    # Rỗng: dequeue() và peek() báo IndexError("hàng đợi rỗng").
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, order):
        node = Node(order)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
        self._size += 1

    def dequeue(self):
        if self.head is None:
            raise IndexError("hàng đợi rỗng")
        value = self.head.value
        self.head = self.head.next
        self._size -= 1
        return value

    def peek(self):
        if self.head is None:
            raise IndexError("hàng đợi rỗng")
        return self.tail.value

    def size(self):
        return self._size


q = PackingQueue()
for code in ("TK101", "TK102", "TK103"):
    q.enqueue(code)
print("Đầu hàng:", q.peek(), "| số đơn:", q.size())
print("Đóng gói:", q.dequeue(), q.dequeue(), q.dequeue())
q.enqueue("TK104")
q.enqueue("TK105")
print("Sau khi hàng rỗng, thêm 2 đơn:", q.dequeue(), q.dequeue(), "| còn:", q.size())
```

Kết quả hiển thị trên Console:

```plaintext
Đầu hàng: TK101 | số đơn: 3
Traceback (most recent call last):
  ...
    raise IndexError("hàng đợi rỗng")
IndexError: hàng đợi rỗng
```

Hai dòng đầu trông đúng, nhưng lần đóng gói thứ ba gây `IndexError: hàng đợi rỗng` dù `size()` vẫn báo còn đơn, nên dòng cuối không được in.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Vẽ chuỗi nút sau ba lần `enqueue` của mã hiện tại: `head`, `tail` trỏ tới đâu, nút TK102 nằm ở đâu? Vì sao TK102 bị mất?
- Sửa `enqueue`. Vì sao sau khi sửa, `peek()` lại trả sai đơn? Sửa `peek`.
- Sau khi sửa hai lỗi trên, chạy tay đoạn "hàng rỗng rồi thêm 2 đơn": sau lần `dequeue` lấy TK103, `head` và `tail` trỏ tới đâu? Lần `enqueue` TK104 gắn nút vào đâu?
- Sửa `dequeue`. Vì sao `enqueue` dựa vào `tail is None` để nhận biết hàng rỗng?
- Ghi Big-O của bốn thao tác. Nếu không có `tail`, `enqueue` tốn bao nhiêu?
- Ghi bốn bộ dữ liệu thử: hàng 1 đơn, lấy hết rồi thêm lại, peek khi rỗng, thêm xen kẽ lấy; kèm kết quả mong đợi.
- Vì sao test có sẵn kiểm tra `q.tail is None` ngay sau khi lấy hết, dù kết quả `dequeue` lúc đó vẫn đúng?

**(2) Sửa lỗi**

- Sửa lớp `PackingQueue` trong `hang_dong_goi.py`. Không đổi tên lớp, phương thức, thuộc tính, thông báo lỗi; không dùng list Python để lưu đơn.
- Chạy `python hang_dong_goi.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex06`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-06 rồi chép các tệp vào kho: `hang_dong_goi.py`, `test_hang_dong_goi.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `hang_dong_goi.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
