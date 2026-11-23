# Lỗi hàng yêu cầu hỗ trợ của tổng đài Tiki dùng deque

### 1. Bối cảnh nghiệp vụ

![Khách gọi sau cùng lại được phục vụ trước, yêu cầu gấp vẫn phải chờ, hết hàng thì màn hình tổng đài sập.](minh_hoa.png)

*Khách gọi sau cùng lại được phục vụ trước, yêu cầu gấp vẫn phải chờ, hết hàng thì màn hình tổng đài sập.*

Bạn là kỹ sư phần mềm trong nhóm chăm sóc khách hàng của Tiki.

Tổng đài nhận **yêu cầu hỗ trợ** và phục vụ theo thứ tự gọi đến. Riêng **yêu cầu gấp** (đơn giao trễ quá hạn) được đưa lên **đầu hàng**. Màn hình còn hiện **3 yêu cầu được phục vụ gần nhất** để trưởng ca kiểm tra lại. Nhóm dùng `collections.deque` theo Lesson 04:

- `add(code)`: yêu cầu thường xếp cuối hàng.
- `add_urgent(code)`: yêu cầu gấp lên đầu hàng (nhiều yêu cầu gấp thì cái đến sau đứng trước).
- `serve()`: phục vụ người đứng đầu, trả mã yêu cầu; hàng rỗng trả `None`.
- `recent_list()`: mã 3 yêu cầu được phục vụ gần nhất, **mới nhất trước**. Phần này dùng `deque(maxlen=3)` và đã đúng.

Mỗi ngày tổng đài nhận hàng nghìn cuộc gọi; phục vụ sai thứ tự làm khách chờ lâu, gọi lại nhiều lần và để lại đánh giá thấp.

Khi đổi từ list sang deque, bạn trong nhóm viết mã chỉ đổi tên kiểu dữ liệu mà giữ nguyên các lệnh cũ; ba thao tác của hàng chờ cần được xem lại theo đúng bảng "dùng deque làm Stack hoặc Queue" của Lesson 04. Trưởng ca cũng yêu cầu: điện thoại viên bấm "Phục vụ" khi không còn ai chờ thì màn hình chỉ hiện "Không còn yêu cầu", không được sập.

Kịch bản kiểm tra (đoạn cuối tệp): ba yêu cầu thường, một yêu cầu gấp; phục vụ ba lượt; thêm một yêu cầu; phục vụ ba lượt nữa (lượt cuối khi hàng đã rỗng); in 3 yêu cầu gần nhất.

Kết quả đúng cần hiển thị:

```plaintext
Phục vụ: ['GAP1', 'YC01', 'YC02']
Phục vụ: YC03 YC04 None
3 yêu cầu gần nhất: ['YC04', 'YC03', 'YC02']
```

### 2. Vấn đề hiện tại

Trưởng ca phản ánh:

- Khách gọi **sau cùng** lại được phục vụ trước.
- Yêu cầu gấp vẫn phải chờ sau mọi người.
- Hết người chờ mà điện thoại viên bấm "Phục vụ" thì màn hình **sập**.

Nhắc lại kiến thức (Lesson 04):

- Dùng deque làm **hàng đợi**: thêm một đầu, lấy **đầu kia** (`append` và `popleft`). Dùng `append` và `pop` là ngăn xếp. "Dùng deque làm hàng đợi nhưng lấy nhầm đầu" là lỗi thường gặp.
- `appendleft` thêm vào bên trái; cả bốn thao tác ở hai đầu đều O(1).
- Gọi `pop()` hoặc `popleft()` trên deque rỗng báo `IndexError: pop from an empty deque`.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `tong_dai.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Hàng yêu cầu hỗ trợ của tổng đài Tiki, dùng collections.deque."""
from collections import deque


class SupportDesk:
    # Hàng yêu cầu hỗ trợ của tổng đài Tiki: yêu cầu thường xếp cuối hàng, yêu cầu gấp (đơn giao trễ)
    # được đưa lên đầu hàng; luôn phục vụ người đứng đầu. Hàng rỗng: serve() trả None.
    # recent_list(): mã 3 yêu cầu được phục vụ gần nhất, mới nhất trước.
    def __init__(self):
        self.waiting = deque()
        self.recent = deque(maxlen=3)

    def add(self, code):
        self.waiting.append(code)

    def add_urgent(self, code):
        self.waiting.append(code)

    def serve(self):
        code = self.waiting.pop()
        self.recent.appendleft(code)
        return code

    def recent_list(self):
        return list(self.recent)


desk = SupportDesk()
for code in ("YC01", "YC02", "YC03"):
    desk.add(code)
desk.add_urgent("GAP1")
print("Phục vụ:", [desk.serve() for _ in range(3)])
desk.add("YC04")
print("Phục vụ:", desk.serve(), desk.serve(), desk.serve())
print("3 yêu cầu gần nhất:", desk.recent_list())
```

Kết quả hiển thị trên Console:

```plaintext
Phục vụ: ['GAP1', 'YC03', 'YC02']
Traceback (most recent call last):
  ...
    code = self.waiting.pop()
IndexError: pop from an empty deque
```

Đối chiếu với kết quả đúng: ba lượt đầu phục vụ GAP1, YC03, YC02 (ngược thứ tự gọi, và GAP1 chỉ ra trước vì tình cờ vào sau cùng); lượt phục vụ khi hàng rỗng gây `IndexError`.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Chạy tay kịch bản với mã hiện tại: ghi nội dung `waiting` (từ trái sang phải) sau mỗi thao tác. Hàng đang hoạt động như ADT nào?
- Vì sao GAP1 vẫn được phục vụ đầu tiên với mã hiện tại? Thêm một yêu cầu thường sau GAP1 thì sao?
- Sửa `serve` và `add_urgent`. Với hai yêu cầu gấp G1 rồi G2, ai được phục vụ trước? Có đúng đặc tả không?
- Sửa `serve` để trả `None` khi hàng rỗng. Có nên ghi `None` vào danh sách gần nhất không?
- `recent` dùng `deque(maxlen=3)` với `appendleft`: khi đã đủ 3 mã, mã nào tự bị bỏ? Nếu đổi sang `append` thì `recent_list` phải đổi thế nào?
- Ghi bốn bộ dữ liệu thử: hàng rỗng, chỉ có yêu cầu gấp, phục vụ 5 lượt rồi xem gần nhất, xen kẽ thêm và phục vụ; kèm kết quả mong đợi.
- Ghi Big-O của bốn thao tác sau khi sửa.

**(2) Sửa lỗi**

- Sửa lớp `SupportDesk` trong `tong_dai.py`. Không đổi tên lớp, phương thức, thuộc tính; tiếp tục dùng `deque`.
- Chạy `python tong_dai.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex07`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-07 rồi chép các tệp vào kho: `tong_dai.py`, `test_tong_dai.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `tong_dai.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
