# Lỗi bảng giá cước GrabBike theo từng km

### 1. Bối cảnh nghiệp vụ

![Đọc giá mức cuối làm ứng dụng báo lỗi, sửa giá một km thì bảng giá dài thêm một mức.](minh_hoa.png)

*Đọc giá mức cuối làm ứng dụng báo lỗi, sửa giá một km thì bảng giá dài thêm một mức.*

Bạn là kỹ sư phần mềm trong nhóm định giá của Grab.

Giá cước GrabBike được tính theo **từng km**: km đầu tiên một giá, km thứ hai một giá khác, càng đi xa giá mỗi km càng giảm. Nhóm lưu bảng giá trong lớp `FareTable` và viết **đặc tả** (ADT) trước khi viết mã:

- `get(i)`: giá của km thứ i + 1 (chỉ số bắt đầu từ 0).
- `set(i, value)`: thay giá tại chỉ số i; **số mức giá và các giá khác giữ nguyên**.
- `size()`: số mức giá đang lưu.
- `last()`: giá của mức cuối cùng (áp dụng cho mọi km vượt quá bảng).
- `get`, `set` với i ngoài khoảng 0 đến size() − 1 báo `IndexError` với thông báo `Chỉ số ngoài phạm vi bảng giá`.

Các nhóm khác (ứng dụng tài xế, màn hình báo giá) chỉ gọi các thao tác trên, không đọc thẳng `_data`. Vì vậy chỉ cần lớp làm đúng đặc tả thì mọi nơi đều đúng; ngược lại, một lỗi trong lớp lan ra mọi màn hình.

Kịch bản kiểm tra (đoạn cuối tệp): bảng 4 mức giá; đọc km đầu, số mức, mức cuối; sửa giá km thứ hai; đọc mức thứ năm (không có).

Kết quả đúng cần hiển thị:

```plaintext
Giá km đầu: 12000
Số mức giá: 4
Giá mức cuối: 8000
Sau khi sửa giá km thứ hai: [12000, 11000, 9000, 8000] | số mức: 4
Đọc mức thứ năm: Chỉ số ngoài phạm vi bảng giá
```

### 2. Vấn đề hiện tại

Nhóm vận hành phản ánh:

- Màn hình báo giá **sập** khi hiện "giá cho km vượt bảng".
- Sau khi sửa giá km thứ hai, bảng giá **có thêm một mức** và giá các km sau bị lùi một vị trí: khách đi 4 km bị tính sai.
- Một số màn hình đọc nhầm chỉ số bằng số mức giá nhưng không nhận được thông báo `Chỉ số ngoài phạm vi bảng giá` như đặc tả, mà nhận lỗi khó hiểu của Python.

Nhắc lại kiến thức (Lesson 01, Lesson 03):

- ADT mô tả **thao tác và ý nghĩa**, gồm cả cách xử lý đầu vào sai; cấu trúc dữ liệu là cách triển khai. Mã bên ngoài chỉ dựa vào đặc tả.
- Với n phần tử, chỉ số hợp lệ là 0 đến n − 1. Dùng độ dài làm chỉ số phần tử cuối là lỗi thường gặp.
- Gán `a[i] = x` thay tại chỗ, O(1); `a.insert(i, x)` chèn thêm phần tử, dịch n − i tham chiếu sang phải.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `bang_gia.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Bảng giá cước GrabBike theo từng km."""
class FareTable:
    # Bảng giá cước GrabBike theo từng km: get(i) là giá của km thứ i + 1 (chỉ số từ 0).
    # Đặc tả: get, set với i ngoài 0 đến size() - 1 báo IndexError("Chỉ số ngoài phạm vi bảng giá");
    # set chỉ thay giá, không đổi số mức.
    def __init__(self, fares):
        self._data = list(fares)

    def _check(self, i):
        if i < 0 or i > self.size():
            raise IndexError("Chỉ số ngoài phạm vi bảng giá")

    def get(self, i):
        self._check(i)
        return self._data[i]

    def set(self, i, value):
        self._check(i)
        self._data.insert(i, value)

    def size(self):
        return len(self._data)

    def last(self):
        return self.get(self.size())


table = FareTable([12000, 10000, 9000, 8000])
print("Giá km đầu:", table.get(0))
print("Số mức giá:", table.size())
print("Giá mức cuối:", table.last())
table.set(1, 11000)
print("Sau khi sửa giá km thứ hai:", [table.get(i) for i in range(table.size())], "| số mức:", table.size())
try:
    table.get(4)
except IndexError as error:
    print("Đọc mức thứ năm:", error)
```

Kết quả hiển thị trên Console:

```plaintext
Giá km đầu: 12000
Số mức giá: 4
Traceback (most recent call last):
  ...
    return self._data[i]
IndexError: list index out of range
```

Dòng đầu và dòng thứ hai đúng. `last()` gây lỗi `IndexError: list index out of range` (lỗi của list, không phải thông báo của đặc tả), nên các dòng sau không được in.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Với bảng 4 mức, `last()` gọi `get` với chỉ số nào? Chỉ số đó có hợp lệ theo đặc tả không? Sửa thế nào?
- Điều kiện trong `_check` cho qua những chỉ số nào? So với đặc tả, chỉ số nào bị cho qua sai? Vì sao lỗi nhận được lại là `list index out of range` chứ không phải thông báo của đặc tả?
- Ghi nội dung `_data` và `size()` sau `set(1, 11000)` của mã hiện tại. Thao tác nào gây ra? Nó dịch bao nhiêu tham chiếu, Big-O là gì?
- Chi phí Big-O của `get`, `set`, `size`, `last` sau khi sửa.
- Vì sao các màn hình khác không nên đọc thẳng `table._data[-1]` để lấy giá mức cuối, dù cách này chạy được?
- Ghi bốn bộ dữ liệu thử: bảng 1 mức, chỉ số bằng size(), chỉ số âm, sửa giá mức cuối; kèm kết quả mong đợi.

**(2) Sửa lỗi**

- Sửa lớp `FareTable` trong `bang_gia.py`. Không đổi tên lớp, phương thức, tham số; không đổi thông báo lỗi.
- Chạy `python bang_gia.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex01`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-01 rồi chép các tệp vào kho: `bang_gia.py`, `test_bang_gia.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `bang_gia.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
