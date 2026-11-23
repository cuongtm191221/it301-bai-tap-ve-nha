# Lỗi chồng phiếu xuất kho Tiki cài bằng chuỗi nút

### 1. Bối cảnh nghiệp vụ

![Máy in phiếu xuất kho báo xử lý một phiếu ba lần liền, chồng phiếu không bao giờ hết.](minh_hoa.png)

*Máy in phiếu xuất kho báo xử lý một phiếu ba lần liền, chồng phiếu không bao giờ hết.*

Bạn là kỹ sư phần mềm trong nhóm vận hành kho của Tiki.

Mỗi phiếu xuất kho được in ra và đặt lên **chồng phiếu** ở quầy; nhân viên luôn xử lý **phiếu trên cùng** (phiếu in sau cùng) trước. Phần mềm của quầy chạy trên máy cũ, nhóm đã cài ngăn xếp bằng **chuỗi nút** theo Lesson 01, mục 2.3: đỉnh là nút `head`, mỗi nút có `value` và `next`.

Đặc tả của lớp `SlipStack`:

- `push(slip)`: đặt phiếu lên trên cùng (như `add_first`).
- `pop()`: lấy phiếu trên cùng, trả về mã phiếu (như `remove_first`).
- `peek()`: xem phiếu trên cùng mà không lấy.
- `is_empty()`, `size()`: chồng có rỗng không; số phiếu (dùng `_size` để không phải duyệt).
- Chồng rỗng: `pop()` và `peek()` báo `IndexError("ngăn xếp rỗng")`.

Màn hình quầy hiện số phiếu còn lại để trưởng ca biết khi nào hết việc; số sai thì ca làm việc không kết thúc được và nhân viên phải ở lại đối chiếu bằng tay.

Vì phiếu nằm trong chuỗi nút, không ai nhìn thấy trực tiếp; nhóm chỉ phát hiện lỗi khi nhân viên phàn nàn rằng phiếu cũ không bao giờ được xử lý và khách của các đơn đó gọi lên hỏi vì sao hàng chưa xuất kho sau hai ngày.

Kịch bản kiểm tra (đoạn cuối tệp): in ba phiếu PX01, PX02, PX03; xử lý hai phiếu; xử lý phiếu cuối; xem chồng rỗng.

Kết quả đúng cần hiển thị:

```plaintext
Xử lý: PX03 PX02 | còn 1 phiếu, trên cùng: PX01
Xử lý: PX01 | rỗng: True | còn 0 phiếu
Xem chồng rỗng: ngăn xếp rỗng
```

### 2. Vấn đề hiện tại

Nhân viên quầy phản ánh:

- Bấm "Xử lý" ba lần thì cả ba lần đều ra **PX03**; phiếu PX01, PX02 không bao giờ tới lượt.
- Màn hình luôn báo còn 3 phiếu, chồng không bao giờ rỗng.
- Xem chồng (khi lẽ ra đã rỗng) vẫn hiện một mã phiếu thay vì báo rỗng.

Nhắc lại kiến thức (Lesson 01):

- `LinkedStack` đặt **đỉnh ở head**: `push` như `add_first`, `pop` như `remove_first` của Session 07, đều O(1).
- `pop` phải **chuyển head sang nút thứ hai** sau khi đọc giá trị, và giảm `_size`. "pop của LinkedStack quên chuyển head" là lỗi thường gặp.
- `peek` trên ngăn xếp rỗng phải báo lỗi như đặc tả, không trả `None` (vì `None` có thể bị hiểu nhầm là một phiếu).

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `chong_phieu.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Chồng phiếu xuất kho Tiki, cài ngăn xếp bằng chuỗi nút."""
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class SlipStack:
    # Chồng phiếu xuất kho Tiki, cài bằng chuỗi nút: phiếu in sau cùng nằm trên cùng (head).
    # Rỗng: pop() và peek() báo IndexError("ngăn xếp rỗng").
    def __init__(self):
        self.head = None
        self._size = 0

    def push(self, slip):
        self.head = Node(slip, self.head)
        self._size += 1

    def pop(self):
        if self.head is None:
            raise IndexError("ngăn xếp rỗng")
        value = self.head.value
        return value

    def peek(self):
        if self.head is None:
            return None
        return self.head.value

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size


slips = SlipStack()
for code in ("PX01", "PX02", "PX03"):
    slips.push(code)
print("Xử lý:", slips.pop(), slips.pop(), "| còn", slips.size(), "phiếu, trên cùng:", slips.peek())
print("Xử lý:", slips.pop(), "| rỗng:", slips.is_empty(), "| còn", slips.size(), "phiếu")
try:
    print("Xem chồng rỗng:", slips.peek())
except IndexError as error:
    print("Xem chồng rỗng:", error)
```

Kết quả hiển thị trên Console:

```plaintext
Xử lý: PX03 PX03 | còn 3 phiếu, trên cùng: PX03
Xử lý: PX03 | rỗng: False | còn 3 phiếu
Xem chồng rỗng: PX03
```

Đối chiếu với kết quả đúng: mỗi lần `pop` đều ra PX03, số phiếu luôn là 3, chồng không bao giờ rỗng.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Vẽ chuỗi nút sau ba lần `push`. Sau lần `pop` đầu tiên của mã hiện tại, `head` trỏ tới nút nào? Vì sao lần `pop` tiếp theo vẫn ra PX03?
- Sửa `pop`: thêm những dòng nào, theo thứ tự nào? Nếu đổi thứ tự "đọc giá trị" và "chuyển head" thì sao?
- Sau khi sửa `pop`, nút PX03 cũ còn được tham chiếu từ đâu không? Python làm gì với nó?
- Vì sao `peek()` trả `None` là sai đặc tả? Nêu một tình huống `None` gây lỗi ở màn hình quầy.
- Ghi Big-O của `push`, `pop`, `peek`, `size`. Vì sao cần `_size` thay vì đếm nút?
- Ghi bốn bộ dữ liệu thử: chồng 1 phiếu, pop trên chồng rỗng, push sau khi pop hết, peek hai lần liên tiếp; kèm kết quả mong đợi.
- So sánh `SlipStack` với `ArrayStack` (list, đỉnh ở cuối): Big-O và bộ nhớ thêm của mỗi cách.

**(2) Sửa lỗi**

- Sửa lớp `SlipStack` trong `chong_phieu.py`. Không đổi tên lớp, phương thức, thuộc tính, thông báo lỗi; không dùng list Python để lưu phiếu.
- Chạy `python chong_phieu.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex05`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-05 rồi chép các tệp vào kho: `chong_phieu.py`, `test_chong_phieu.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `chong_phieu.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
