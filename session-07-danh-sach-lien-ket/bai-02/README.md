# Lỗi thêm bài hát vào danh sách phát Zing MP3

### 1. Bối cảnh nghiệp vụ

![Người nghe thấy bài ZM002 biến mất khỏi danh sách phát và ứng dụng bị treo; kỹ sư phần mềm lần theo con trỏ tail.](minh_hoa.png)

*Người nghe thấy bài ZM002 biến mất khỏi danh sách phát và ứng dụng bị treo; kỹ sư phần mềm lần theo con trỏ tail.*

Bạn là kỹ sư phần mềm trong nhóm xây dựng tính năng danh sách phát của ứng dụng nghe nhạc Zing MP3.

Mỗi người nghe có một danh sách phát. Nhóm chọn lưu danh sách phát bằng **danh sách liên kết đơn**: mỗi node giữ mã một bài hát, `head` là bài sẽ phát đầu tiên, `tail` là bài cuối danh sách, `size` là số bài.

Ví dụ danh sách phát có ba bài:

```plaintext
head                         tail
 |                            |
ZM001  ->  ZM002  ->  ZM003  ->  None        size = 3
```

Trong lúc nghe nhạc, người nghe làm hai thao tác:

- Bấm "Thêm vào danh sách phát": bài mới được thêm vào **cuối** danh sách.
- Bấm "Phát tiếp theo": bài được chèn vào **đầu** danh sách để phát ngay sau bài hiện tại.

Cả hai thao tác phải chạy trong O(1), dù danh sách có vài bài hay vài nghìn bài.

Kịch bản kiểm tra của nhóm:

- Danh sách `playlist`: thêm lần lượt `"ZM001"`, `"ZM002"`, `"ZM003"` vào cuối, rồi chọn "Phát tiếp theo" cho `"ZM000"`.
- Danh sách `morning` (đang rỗng): chọn "Phát tiếp theo" cho `"ZM010"`, rồi thêm `"ZM011"` vào cuối.

Kết quả đúng cần hiển thị:

```plaintext
Danh sách phát: ZM000 -> ZM001 -> ZM002 -> ZM003 -> None
Bài cuối danh sách: ZM003
Số bài: 4
Danh sách buổi sáng: ZM010 -> ZM011 -> None
```

### 2. Vấn đề hiện tại

Người nghe phản ánh hai hiện tượng: có bài vừa thêm xong thì **biến mất** khỏi danh sách phát, và với một danh sách mới tạo thì ứng dụng **bị treo** khi thêm bài.

Lập trình viên trước đã viết lớp `Playlist` với hai phương thức `add_first` và `add_last`, nhưng chưa nắm chắc ba điều của danh sách liên kết đơn có `tail`:

- `tail` phải luôn trỏ tới **node cuối cùng**. Thêm một node vào cuối mà không dời `tail` thì lần thêm sau sẽ nối đè lên node vừa thêm.
- Khi danh sách **rỗng**, node đầu tiên được thêm vào vừa là `head` vừa là `tail`, dù nó được thêm bằng `add_first` hay `add_last`.
- `size` phải tăng đúng 1 ở **mọi** thao tác thêm.

### 3. Mã nguồn hiện tại (Legacy Code)

Tệp `playlist.py` trong thư mục khởi đầu:

```python
class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class Playlist:
    def __init__(self):
        self.head = None    # bài sẽ phát đầu tiên
        self.tail = None    # bài cuối danh sách
        self.size = 0       # số bài trong danh sách

    def add_first(self, code):
        # Chèn bài "phát tiếp theo" vào đầu danh sách
        node = Node(code, self.head)
        self.head = node

    def add_last(self, code):
        # Thêm bài vào cuối danh sách
        node = Node(code)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
        self.size += 1

    def to_text(self):
        parts = []
        current = self.head
        while current is not None:
            parts.append(current.value)
            current = current.next
        return " -> ".join(parts + ["None"])


playlist = Playlist()
# Người nghe thêm ba bài vào cuối danh sách
playlist.add_last("ZM001")
playlist.add_last("ZM002")
playlist.add_last("ZM003")
# Người nghe chọn "phát tiếp theo" cho bài ZM000
playlist.add_first("ZM000")
print("Danh sách phát:", playlist.to_text())
print("Bài cuối danh sách:", playlist.tail.value)
print("Số bài:", playlist.size)

# Một danh sách mới: chọn "phát tiếp theo" trước, rồi mới thêm vào cuối
morning = Playlist()
morning.add_first("ZM010")
morning.add_last("ZM011")
print("Danh sách buổi sáng:", morning.to_text())
```

Kết quả hiển thị trên Console:

```plaintext
Danh sách phát: ZM000 -> ZM001 -> ZM003 -> None
Bài cuối danh sách: ZM001
Số bài: 3
Traceback (most recent call last):
  ...
    self.tail.next = node
AttributeError: 'NoneType' object has no attribute 'next'
```

Chương trình dừng ở dòng `morning.add_last("ZM011")`. Trước đó, ba dòng đã in ra cũng sai so với kết quả đúng:

- Bài `ZM002` biến mất khỏi danh sách phát.
- Bài cuối danh sách được báo là `ZM001`, không phải `ZM003`.
- Số bài là 3, trong khi người nghe đã thêm 4 bài.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Vẽ danh sách (các node, `head`, `tail`) sau từng lệnh `add_last("ZM001")`, `add_last("ZM002")`, `add_last("ZM003")` khi chạy mã hiện tại. Sau lệnh thứ hai, `tail` đang trỏ tới node nào?
- Vì sao bài `ZM002` biến mất sau lệnh `add_last("ZM003")`? Node `ZM002` còn được node nào trỏ tới không?
- Trong `add_last`, cần thêm dòng lệnh nào, ở nhánh nào, để `tail` luôn là node cuối?
- Sau `morning.add_first("ZM010")`, `head` và `tail` của `morning` đang là gì?
- Vì sao dòng `self.tail.next = node` báo `AttributeError: 'NoneType' object has no attribute 'next'`?
- `add_first` cần làm thêm việc gì khi danh sách đang rỗng?
- Vì sao số bài in ra là 3 mà không phải 4? Phương thức nào quên tăng `size`?
- Sau khi sửa, `add_first` và `add_last` có còn là O(1) không? Vì sao?

**(2) Sửa lỗi**

- Sửa hai phương thức `add_first` và `add_last` trong `playlist.py`. Không đổi tên lớp, tên phương thức; không dùng list Python để lưu các bài.
- Chạy `python playlist.py` phải cho đúng kết quả:

```plaintext
Danh sách phát: ZM000 -> ZM001 -> ZM002 -> ZM003 -> None
Bài cuối danh sách: ZM003
Số bài: 4
Danh sách buổi sáng: ZM010 -> ZM011 -> None
```

- Chạy `pytest -q` phải xanh cả 3 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex01`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-02 rồi chép các tệp vào kho: `playlist.py`, `test_playlist.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `playlist.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
