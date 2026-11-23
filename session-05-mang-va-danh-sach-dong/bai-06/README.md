# Lỗi chèn điểm dừng vào lộ trình GrabCar

### 1. Bối cảnh nghiệp vụ

![Khách thêm điểm dừng thì điểm đến cuối biến mất, thêm điểm dừng thứ hai thì ứng dụng báo lỗi.](minh_hoa.png)

*Khách thêm điểm dừng thì điểm đến cuối biến mất, thêm điểm dừng thứ hai thì ứng dụng báo lỗi.*

Bạn là kỹ sư phần mềm trong nhóm tính năng **"Nhiều điểm dừng"** của GrabCar.

Khách có thể thêm điểm dừng vào **giữa** lộ trình (ghé đón bạn, ghé mua đồ). Lộ trình lưu trong lớp `Route`, cài bằng mảng động theo Lesson 04 (các phương thức `append`, `_resize`, `stops` đã có và đúng). Nhóm viết thêm `insert(index, value)` với hành vi giống `list.insert`:

- Điểm mới có chỉ số `index`; các điểm từ chỉ số đó trở đi lùi một vị trí, **không mất điểm nào**.
- `index` âm tính từ cuối (`-1` là chèn trước điểm cuối); nhỏ hơn `-len` thì chèn đầu; lớn hơn `len` thì chèn cuối.
- Vùng lưu trữ đầy thì mở rộng gấp đôi trước khi chèn.
- `moves` đếm số tham chiếu đã dịch.

Tài xế nhìn danh sách điểm dừng để chạy, nên chỉ cần mất một điểm là khách bị bỏ lại giữa đường.

Kịch bản kiểm tra (đoạn cuối tệp): lộ trình 3 điểm; chèn "Chợ Lớn" vào chỉ số 1; chèn "Quận 3" trước điểm cuối (chỉ số -1); chèn "Đổ xăng" vào đầu; chèn "Về nhà" với chỉ số 99.

Kết quả đúng cần hiển thị:

```plaintext
Chèn Chợ Lớn vào chỉ số 1: ['Đón khách', 'Chợ Lớn', 'Bến Thành', 'Sân bay'] | dịch: 2
Chèn Quận 3 trước điểm cuối: ['Đón khách', 'Chợ Lớn', 'Bến Thành', 'Quận 3', 'Sân bay']
Chèn Đổ xăng vào đầu: ['Đổ xăng', 'Đón khách', 'Chợ Lớn', 'Bến Thành', 'Quận 3', 'Sân bay']
Chèn cuối: ['Đổ xăng', 'Đón khách', 'Chợ Lớn', 'Bến Thành', 'Quận 3', 'Sân bay', 'Về nhà'] | số điểm: 7
```

### 2. Vấn đề hiện tại

Tài xế và khách phản ánh:

- Thêm "Chợ Lớn" vào giữa thì điểm **"Sân bay" biến mất**, "Bến Thành" xuất hiện hai lần.
- Thêm điểm dừng thứ hai thì ứng dụng báo `IndexError`.

Nhắc lại kiến thức (Lesson 03, Lesson 04):

- `insert(i, x)` trên n phần tử dịch **n − i** tham chiếu sang phải để tạo chỗ ở ô i.
- Vòng dịch phải đi **từ cuối về** (`j` từ `size` xuống `i + 1`, gán `data[j] = data[j - 1]`). Đi từ đầu tới thì mỗi bước ghi đè phần tử chưa kịp dịch: "vòng dịch của insert đi sai chiều" là lỗi thường gặp.
- Trước khi ghi vào ô `size`, phải chắc vùng lưu trữ còn chỗ; đầy thì `_resize` trước.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `lo_trinh.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Lộ trình nhiều điểm dừng của GrabCar, lưu bằng mảng động tự cài."""
class Route:
    # Lộ trình GrabCar nhiều điểm dừng, lưu bằng mảng động tự cài (Lesson 04).
    # moves đếm số tham chiếu đã dịch khi chèn; copies đếm số tham chiếu đã chép khi mở rộng.
    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._data = [None] * self._capacity
        self.moves = self.copies = 0

    def __len__(self):
        return self._size

    def stops(self):
        return [self._data[j] for j in range(self._size)]

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for j in range(self._size):
            new_data[j] = self._data[j]
            self.copies += 1
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        # Chèn điểm dừng value để nó có chỉ số index; index âm tính từ cuối,
        # index nhỏ hơn -len thì chèn đầu, lớn hơn len thì chèn cuối (giống list.insert).
        if index > self._size:
            index = self._size
        for j in range(index, self._size):
            self._data[j + 1] = self._data[j]
            self.moves += 1
        self._data[index] = value
        self._size += 1


route = Route()
for stop in ("Đón khách", "Bến Thành", "Sân bay"):
    route.append(stop)
route.insert(1, "Chợ Lớn")
print("Chèn Chợ Lớn vào chỉ số 1:", route.stops(), "| dịch:", route.moves)
route.insert(-1, "Quận 3")
print("Chèn Quận 3 trước điểm cuối:", route.stops())
route.insert(0, "Đổ xăng")
print("Chèn Đổ xăng vào đầu:", route.stops())
route.insert(99, "Về nhà")
print("Chèn cuối:", route.stops(), "| số điểm:", len(route))
```

Kết quả hiển thị trên Console:

```plaintext
Chèn Chợ Lớn vào chỉ số 1: ['Đón khách', 'Chợ Lớn', 'Bến Thành', 'Bến Thành'] | dịch: 2
Traceback (most recent call last):
  ...
    self._data[j + 1] = self._data[j]
IndexError: list assignment index out of range
```

Đối chiếu với kết quả đúng: sau lần chèn đầu, "Sân bay" mất và "Bến Thành" bị lặp; lần chèn thứ hai gây `IndexError`, nên các dòng sau không được in.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Chạy tay lần chèn "Chợ Lớn" vào chỉ số 1 của mã hiện tại: ghi `_data` sau mỗi vòng dịch. Vòng nào làm mất "Sân bay"?
- Viết lại vòng dịch theo đúng chiều; chạy tay lại và đếm số lần dịch.
- Vì sao lần chèn thứ hai báo `IndexError`? `_capacity` và `_size` lúc đó là bao nhiêu?
- Mã hiện tại xử lý `index = -1` thế nào? Theo đặc tả phải thành chỉ số nào? `index = -99` thì sao?
- Lập bảng số tham chiếu phải dịch khi chèn vào chỉ số 0, 2, len với lộ trình 6 điểm. Ghi Big-O của `insert` trong trường hợp xấu nhất và tốt nhất.
- Ghi bốn bộ dữ liệu thử: lộ trình rỗng, chèn khi đầy, chỉ số âm, chỉ số vượt; kèm kết quả mong đợi.

**(2) Sửa lỗi**

- Sửa phương thức `insert` trong `lo_trinh.py`. Không đổi tên lớp, phương thức, thuộc tính; không dùng `list.insert` hay cắt list trên `_data`.
- Chạy `python lo_trinh.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex06`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-06 rồi chép các tệp vào kho: `lo_trinh.py`, `test_lo_trinh.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `lo_trinh.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
