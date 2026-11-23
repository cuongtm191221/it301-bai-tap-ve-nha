# Lỗi đếm và tìm bài hát trong danh sách phát Zing MP3

### 1. Bối cảnh nghiệp vụ

![Người nghe mở danh sách phát thấy số bài hiện thiếu và các bài đầu biến mất sau khi tìm kiếm.](minh_hoa.png)

*Màn hình danh sách phát báo thiếu một bài, và sau một lần tìm kiếm thì các bài đứng đầu biến mất.*

Bạn là kỹ sư phần mềm trong nhóm xây dựng tính năng danh sách phát của ứng dụng nghe nhạc Zing MP3.

Mỗi người nghe có một danh sách phát, lưu bằng **danh sách liên kết đơn**: mỗi node giữ mã một bài hát, `head` là bài sẽ phát đầu tiên, `tail` là bài cuối danh sách.

Ví dụ danh sách phát có bốn bài:

```plaintext
head                                    tail
 |                                       |
ZM001  ->  ZM002  ->  ZM003  ->  ZM004  ->  None
```

Màn hình danh sách phát cần ba thao tác **chỉ đọc**, không được làm thay đổi danh sách:

- Hiện số bài ở đầu màn hình ("4 bài hát").
- Ô tìm kiếm: người nghe gõ mã bài, ứng dụng cuộn tới vị trí của bài đó (vị trí tính từ 0); không có thì báo không tìm thấy.
- Hiện toàn bộ danh sách theo thứ tự sẽ phát.

Kịch bản kiểm tra của nhóm: tạo danh sách gồm `"ZM001"`, `"ZM002"`, `"ZM003"`, `"ZM004"`; đếm số bài; tìm `"ZM003"`; in danh sách; tìm `"ZM999"` (không có); in lại danh sách; cuối cùng đếm số bài của một danh sách mới tạo, chưa có bài nào.

Kết quả đúng cần hiển thị:

```plaintext
Số bài: 4
Vị trí của ZM003: 2
Danh sách phát: ZM001 -> ZM002 -> ZM003 -> ZM004 -> None
Vị trí của ZM999: None
Danh sách phát: ZM001 -> ZM002 -> ZM003 -> ZM004 -> None
Số bài của danh sách mới: 0
```

### 2. Vấn đề hiện tại

Người nghe phản ánh ba hiện tượng: số bài hiện ra luôn **thiếu một bài**; sau khi dùng ô tìm kiếm thì **các bài đứng trước bài vừa tìm biến mất**; và với danh sách mới tạo thì màn hình **bị treo**.

Lập trình viên trước đã viết hai phương thức `count` và `find`, nhưng chưa nắm chắc cách duyệt danh sách liên kết:

- Duyệt bằng một **biến riêng** (thường đặt tên `current`), bắt đầu từ `head`, mỗi bước gán `current = current.next`. Không được dời chính `head`, vì `head` là lối vào duy nhất của danh sách.
- Điều kiện dừng là `current is not None`: node cuối cùng vẫn phải được xử lý. Viết `current.next is not None` thì vòng lặp dừng trước node cuối.
- Danh sách rỗng có `head` là `None`; gọi `.next` hoặc `.value` trên `None` sẽ báo `AttributeError`.
- Tìm không thấy phải trả về `None`, không trả về một con số.

### 3. Mã nguồn hiện tại (Legacy Code)

Tệp `playlist.py` trong thư mục khởi đầu (`add_last` và `to_text` đã đúng, không cần sửa):

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Playlist:
    def __init__(self):
        self.head = None    # bài sẽ phát đầu tiên
        self.tail = None    # bài cuối danh sách

    def add_last(self, code):
        # Cho sẵn, đã đúng: thêm bài vào cuối danh sách
        node = Node(code)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def count(self):
        # Đếm số bài trong danh sách
        total = 0
        current = self.head
        while current.next is not None:
            total += 1
            current = current.next
        return total

    def find(self, code):
        # Trả về vị trí (tính từ 0) của bài có mã code, không có thì trả None
        position = 0
        while self.head is not None:
            if self.head.value == code:
                return position
            self.head = self.head.next
            position += 1
        return position

    def to_text(self):
        # Cho sẵn, đã đúng
        parts = []
        current = self.head
        while current is not None:
            parts.append(current.value)
            current = current.next
        return " -> ".join(parts + ["None"])


playlist = Playlist()
for code in ["ZM001", "ZM002", "ZM003", "ZM004"]:
    playlist.add_last(code)
print("Số bài:", playlist.count())
print("Vị trí của ZM003:", playlist.find("ZM003"))
print("Danh sách phát:", playlist.to_text())
print("Vị trí của ZM999:", playlist.find("ZM999"))
print("Danh sách phát:", playlist.to_text())

# Danh sách mới tạo, chưa có bài nào
empty = Playlist()
print("Số bài của danh sách mới:", empty.count())
```

Kết quả hiển thị trên Console:

```plaintext
Số bài: 3
Vị trí của ZM003: 2
Danh sách phát: ZM003 -> ZM004 -> None
Vị trí của ZM999: 2
Danh sách phát: None
Traceback (most recent call last):
  ...
    while current.next is not None:
AttributeError: 'NoneType' object has no attribute 'next'
```

Chương trình dừng ở dòng `empty.count()`. Trước đó, năm dòng đã in cũng sai so với kết quả đúng:

- Số bài là 3, trong khi danh sách có 4 bài.
- Sau lần tìm `ZM003`, danh sách chỉ còn `ZM003 -> ZM004`.
- Tìm `ZM999` (không có) lại trả về số 2 thay vì `None`.
- Sau lần tìm thứ hai, danh sách phát trống trơn.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Chạy tay `count()` trên danh sách bốn bài: ghi giá trị của `current` và `total` sau mỗi vòng lặp. Vòng lặp dừng khi `current` đang ở node nào? Node đó đã được đếm chưa?
- Cần đổi điều kiện của vòng `while` trong `count` thành gì?
- Vì sao `empty.count()` báo `AttributeError: 'NoneType' object has no attribute 'next'`? Sau khi đổi điều kiện ở câu trên, lỗi này còn không?
- Trong `find`, biến nào đang bị dời đi sau mỗi vòng lặp? Sau lệnh `find("ZM003")`, `head` đang trỏ tới node nào?
- Các node `ZM001`, `ZM002` còn nằm trong bộ nhớ không, và còn cách nào đi tới chúng không?
- Vì sao `find("ZM999")` trả về 2? Khi không tìm thấy, `find` phải trả về gì?
- Viết lại vòng lặp của `find` với biến `current`.
- `count` và `find` có Big-O thời gian là bao nhiêu (n là số bài)? Vì sao?

**(2) Sửa lỗi**

- Sửa hai phương thức `count` và `find` trong `playlist.py`. Không đổi tên lớp, tên phương thức; không dùng list Python để lưu các bài.
- Chạy `python playlist.py` phải cho đúng kết quả:

```plaintext
Số bài: 4
Vị trí của ZM003: 2
Danh sách phát: ZM001 -> ZM002 -> ZM003 -> ZM004 -> None
Vị trí của ZM999: None
Danh sách phát: ZM001 -> ZM002 -> ZM003 -> ZM004 -> None
Số bài của danh sách mới: 0
```

- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex01`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-01 rồi chép các tệp vào kho: `playlist.py`, `test_playlist.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong tệp mã nguồn.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
