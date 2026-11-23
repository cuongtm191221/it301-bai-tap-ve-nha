# Lỗi bộ đệm điểm GPS của tài xế Grab

### 1. Bối cảnh nghiệp vụ

![Ứng dụng báo tài xế có 7 điểm GPS dù chỉ ghi 6, và máy chủ chép hàng chục triệu tham chiếu chỉ để ghi 10.000 điểm.](minh_hoa.png)

*Ứng dụng báo tài xế có 7 điểm GPS dù chỉ ghi 6, và máy chủ chép hàng chục triệu tham chiếu chỉ để ghi 10.000 điểm.*

Bạn là kỹ sư phần mềm trong nhóm bản đồ của Grab.

Trong một chuyến, ứng dụng tài xế ghi **điểm GPS** vài giây một lần vào bộ đệm, rồi gửi về máy chủ để vẽ đường đi và tính quãng đường. Thiết bị tài xế chạy bản Python rút gọn, nên nhóm tự cài lớp `DynamicArray` theo Lesson 04 thay cho list:

- `append(value)`: ghi thêm một điểm; khi vùng lưu trữ đầy thì cấp vùng mới **gấp đôi** và chép các tham chiếu sang (`copies` đếm số tham chiếu đã chép).
- `len(points)`: **số điểm đã ghi**.
- `points[i]`: điểm tại chỉ số i, i âm tính từ cuối; i ngoài khoảng phần tử báo `IndexError("Chỉ số ngoài phạm vi phần tử")`.

Một chuyến dài có hơn 10.000 điểm. Số điểm còn được dùng để tính phụ phí chờ, nên đếm sai là tính sai tiền của khách.

Kịch bản kiểm tra (đoạn cuối tệp): ghi 6 điểm; in số điểm, điểm cuối; đọc điểm thứ 7 (không có); ghi 10.000 điểm và in số tham chiếu đã chép.

Kết quả đúng cần hiển thị:

```plaintext
Số điểm GPS: 6
Điểm cuối: GPS6
Điểm thứ 7: Chỉ số ngoài phạm vi phần tử
10.000 điểm, số tham chiếu đã chép: 16383
```

### 2. Vấn đề hiện tại

Nhóm bản đồ phản ánh:

- Tài xế ghi 6 điểm nhưng ứng dụng báo **7 điểm**; đọc "điểm thứ 7" nhận được `None` thay vì báo lỗi, làm bản đồ vẽ một đoạn thẳng về gốc tọa độ.
- Chuyến dài làm máy tài xế nóng và chậm: ghi 10.000 điểm mà phải chép **25 triệu** tham chiếu.

Nhắc lại kiến thức (Lesson 02, Lesson 04):

- `_data` là vùng lưu trữ có `_capacity` ô; chỉ `_size` ô đầu là **phần tử thật**, các ô còn lại là **ô dự phòng**. Mọi thao tác trả lời "có bao nhiêu phần tử", "chỉ số nào hợp lệ" phải dựa vào `_size`, không dựa vào `_capacity`.
- Mở rộng **gấp đôi**: tổng số tham chiếu phải chép sau n lần append nhỏ hơn 2n, nên `append` là O(1) khấu hao. Mở rộng thêm một số ô cố định (+1, +2...): tổng số lần chép cỡ n²/c, append trung bình O(n).
- "Đếm ô dự phòng thành phần tử" là lỗi thường gặp khi tự cài mảng động.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `mang_dong.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Bộ đệm điểm GPS của tài xế Grab, lưu bằng mảng động tự cài."""
class DynamicArray:
    # Mảng động tự cài (Lesson 04): _data là vùng lưu trữ có _capacity ô, chỉ _size ô đầu là phần tử thật.
    # copies đếm số tham chiếu đã chép khi mở rộng.
    def __init__(self):
        self._capacity = 1
        self._size = 0
        self._data = [None] * self._capacity
        self.copies = 0

    def __len__(self):
        return self._capacity

    def _normalize_index(self, index):
        if index < 0:
            index += self._size
        if not 0 <= index < self._capacity:
            raise IndexError("Chỉ số ngoài phạm vi phần tử")
        return index

    def __getitem__(self, index):
        return self._data[self._normalize_index(index)]

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for j in range(self._size):
            new_data[j] = self._data[j]
            self.copies += 1
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        if self._size == self._capacity:
            self._resize(self._capacity + 2)
        self._data[self._size] = value
        self._size += 1


points = DynamicArray()
for k in range(6):
    points.append(f"GPS{k + 1}")
print("Số điểm GPS:", len(points))
print("Điểm cuối:", points[-1])
try:
    print("Điểm thứ 7:", points[6])
except IndexError as error:
    print("Điểm thứ 7:", error)
track = DynamicArray()
for k in range(10000):
    track.append(k)
print("10.000 điểm, số tham chiếu đã chép:", track.copies)
```

Kết quả hiển thị trên Console:

```plaintext
Số điểm GPS: 7
Điểm cuối: GPS6
Điểm thứ 7: None
10.000 điểm, số tham chiếu đã chép: 25000000
```

Đối chiếu với kết quả đúng: điểm cuối đúng, nhưng số điểm là 7, điểm thứ 7 là `None`, và số tham chiếu đã chép là 25.000.000 thay vì 16.383.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Ghi `_size`, `_capacity` sau mỗi lần append trong 6 lần đầu của mã hiện tại. Vì sao `len` ra 7?
- Với 6 điểm, những chỉ số nào `_normalize_index` của mã hiện tại cho qua? Chỉ số nào trong đó trỏ vào ô dự phòng?
- Tính tổng số tham chiếu đã chép sau n lần append khi mỗi lần mở rộng thêm 2 ô; kiểm tra với n = 10.000 (25.000.000). Ghi Big-O của một lần append trung bình.
- Sau khi đổi sang gấp đôi, liệt kê các lần mở rộng khi ghi 10 điểm và tổng số tham chiếu đã chép. Vì sao 10.000 điểm chép 16.383 tham chiếu?
- Bộ nhớ dự phòng lớn nhất của cách gấp đôi là bao nhiêu ô so với số phần tử? Đánh đổi gì để có O(1) khấu hao?
- Ghi bốn bộ dữ liệu thử: mảng rỗng, đọc chỉ số size, đọc chỉ số -size, 8 lần append (đúng lúc đầy); kèm kết quả mong đợi.

**(2) Sửa lỗi**

- Sửa lớp `DynamicArray` trong `mang_dong.py`. Không đổi tên lớp, phương thức, thuộc tính, thông báo lỗi; không dùng list Python làm phần tử thay cho vùng lưu trữ (không `append` vào `_data`).
- Chạy `python mang_dong.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex05`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-05 rồi chép các tệp vào kho: `mang_dong.py`, `test_mang_dong.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `mang_dong.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
