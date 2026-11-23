# Lỗi xem lịch sử nghe nhạc trên Zing MP3

### 1. Bối cảnh nghiệp vụ

![Người nghe mở mục Nghe gần đây nhưng chỉ thấy một bài, dù vừa nghe bốn bài.](minh_hoa.png)

*Mục "Nghe gần đây" chỉ hiện một bài, dù người nghe vừa nghe bốn bài.*

Bạn là kỹ sư phần mềm trong nhóm xây dựng mục "Nghe gần đây" của ứng dụng nghe nhạc Zing MP3.

Mỗi lần người nghe nghe xong một bài, mã bài được ghi vào **lịch sử nghe**. Mục "Nghe gần đây" hiện các bài **từ mới về cũ**, còn trang thống kê hiện **từ cũ đến mới**. Vì phải đi được cả hai chiều, nhóm lưu lịch sử bằng **danh sách liên kết đôi**: mỗi node có `prev` (bài nghe ngay trước) và `next` (bài nghe ngay sau); `head` là bài nghe cũ nhất, `tail` là bài nghe mới nhất.

Ví dụ lịch sử có ba bài:

```plaintext
head                              tail
 |                                 |
ZM001  <->  ZM002  <->  ZM003          size = 3
```

Hai thao tác làm thay đổi lịch sử:

- Nghe xong một bài: ghi bài đó vào **cuối** lịch sử (`add_last`).
- Lịch sử chỉ giữ một số bài gần nhất: khi vượt quá thì bỏ bài **cũ nhất** ở đầu (`remove_first`), trả về mã bài đã bỏ. Lịch sử trống mà vẫn gọi bỏ thì báo `IndexError("lịch sử nghe đang trống")`.

Kịch bản kiểm tra của nhóm: ghi lần lượt `"ZM001"`, `"ZM002"`, `"ZM003"`, `"ZM004"`; in lịch sử theo hai chiều; bỏ bài cũ nhất; in lại từ mới về cũ; in node đứng trước bài cũ nhất (phải là `None`); cuối cùng, với một lịch sử chỉ có một bài, bỏ bài đó rồi in bài mới nhất.

Kết quả đúng cần hiển thị:

```plaintext
Từ cũ đến mới: ZM001 -> ZM002 -> ZM003 -> ZM004 -> None
Từ mới về cũ: ZM004 -> ZM003 -> ZM002 -> ZM001 -> None
Bỏ bài cũ nhất: ZM001
Từ mới về cũ: ZM004 -> ZM003 -> ZM002 -> None
Bài đứng trước bài cũ nhất: None
Bài mới nhất sau khi xóa hết: None
```

### 2. Vấn đề hiện tại

Người nghe phản ánh: mục "Nghe gần đây" **chỉ hiện đúng một bài**, dù trang thống kê (từ cũ đến mới) vẫn hiện đủ. Nhóm kiểm thử báo thêm: sau khi lịch sử bị xóa hết, ứng dụng vẫn hiện một bài "ma" ở mục này.

Lập trình viên trước đã viết `add_last` và `remove_first` giống hệt bản của danh sách liên kết đơn, nên bỏ sót phần riêng của danh sách liên kết đôi:

- Mỗi lần nối một node mới phải đặt **cả hai chiều**: `next` của node cũ và `prev` của node mới. Thiếu `prev` thì duyệt xuôi vẫn đúng, nhưng duyệt ngược dừng ngay ở node đầu tiên gặp.
- Khi bỏ node đầu, node kế tiếp trở thành `head`, và `prev` của `head` phải là `None`. Nếu không, `head` vẫn giữ liên kết tới một node đã bị gỡ.
- Khi bỏ **node duy nhất**, cả `head` và `tail` đều phải thành `None`.

Lưu ý: lỗi thứ hai đang bị lỗi thứ nhất che mất. Sau khi sửa `add_last`, hãy chạy lại để thấy lỗi của `remove_first` lộ ra.

### 3. Mã nguồn hiện tại (Legacy Code)

Tệp `history.py` trong thư mục khởi đầu (`to_text` và `to_text_backward` đã đúng, không cần sửa):

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class History:
    def __init__(self):
        self.head = None    # bài nghe cũ nhất
        self.tail = None    # bài nghe mới nhất
        self.size = 0       # số bài trong lịch sử

    def add_last(self, code):
        # Ghi bài vừa nghe vào cuối lịch sử
        node = Node(code)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def remove_first(self):
        # Bỏ bài nghe cũ nhất, trả về mã bài
        code = self.head.value
        self.head = self.head.next
        self.size -= 1
        return code

    def to_text(self):
        # Cho sẵn, đã đúng: từ cũ đến mới
        parts = []
        current = self.head
        while current is not None:
            parts.append(current.value)
            current = current.next
        return " -> ".join(parts + ["None"])

    def to_text_backward(self):
        # Cho sẵn, đã đúng: từ mới về cũ, đi theo prev
        parts = []
        current = self.tail
        while current is not None:
            parts.append(current.value)
            current = current.prev
        return " -> ".join(parts + ["None"])


history = History()
for code in ["ZM001", "ZM002", "ZM003", "ZM004"]:
    history.add_last(code)
print("Từ cũ đến mới:", history.to_text())
print("Từ mới về cũ:", history.to_text_backward())
# Lịch sử chỉ giữ 3 bài gần nhất: bỏ bài cũ nhất
print("Bỏ bài cũ nhất:", history.remove_first())
print("Từ mới về cũ:", history.to_text_backward())
print("Bài đứng trước bài cũ nhất:", history.head.prev)

# Lịch sử chỉ có một bài rồi bị xóa hết
single = History()
single.add_last("ZM010")
single.remove_first()
print("Bài mới nhất sau khi xóa hết:", single.tail)
```

Kết quả hiển thị trên Console:

```plaintext
Từ cũ đến mới: ZM001 -> ZM002 -> ZM003 -> ZM004 -> None
Từ mới về cũ: ZM004 -> None
Bỏ bài cũ nhất: ZM001
Từ mới về cũ: ZM004 -> None
Bài đứng trước bài cũ nhất: None
Bài mới nhất sau khi xóa hết: <__main__.Node object at 0x...>
```

Chương trình không báo lỗi nào, nhưng ba dòng sai so với kết quả đúng:

- Hai lần in "Từ mới về cũ" chỉ có `ZM004`.
- Lịch sử đã xóa hết mà `tail` vẫn trỏ tới một node.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Sau bốn lệnh `add_last` của mã hiện tại, `prev` của node `ZM004` đang là gì? `prev` của node `ZM002` là gì?
- Vì sao duyệt từ cũ đến mới vẫn đủ bốn bài, còn duyệt từ mới về cũ chỉ được một bài?
- Trong `add_last`, cần thêm dòng lệnh nào, ở nhánh nào? Dòng đó phải đứng trước hay sau dòng `self.tail = node`? Vì sao?
- Sửa xong `add_last`, chạy lại chương trình: dòng "Bài đứng trước bài cũ nhất" in ra gì? Vì sao nó không còn là `None`?
- Trong `remove_first`, cần thêm lệnh gì để `head` mới không còn liên kết về node đã bỏ?
- Với lịch sử chỉ có một bài, sau `remove_first` của mã hiện tại thì `head` và `tail` là gì? Cần sửa thế nào?
- Vì sao gọi `remove_first` trên lịch sử trống sẽ báo `AttributeError`? Cần kiểm tra gì và báo lỗi nào?
- Vì sao chương trình không hề báo lỗi mà kết quả vẫn sai? Loại lỗi này nên được phát hiện bằng cách nào?

**(2) Sửa lỗi**

- Sửa hai phương thức `add_last` và `remove_first` trong `history.py`. Không đổi tên lớp, tên phương thức; không dùng list Python để lưu lịch sử.
- Chạy `python history.py` phải cho đúng kết quả:

```plaintext
Từ cũ đến mới: ZM001 -> ZM002 -> ZM003 -> ZM004 -> None
Từ mới về cũ: ZM004 -> ZM003 -> ZM002 -> ZM001 -> None
Bỏ bài cũ nhất: ZM001
Từ mới về cũ: ZM004 -> ZM003 -> ZM002 -> None
Bài đứng trước bài cũ nhất: None
Bài mới nhất sau khi xóa hết: None
```

- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex04`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-04 rồi chép các tệp vào kho: `history.py`, `test_history.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong tệp mã nguồn.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
