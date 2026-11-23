# Bài 4: Cài lại danh sách liên kết đôi

Mã: K4 · Mức: Cài lại · Cấp độ: Dễ · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-04` · Tệp nộp: `bai_k4.py`

### 1. Mục tiêu

- Tự viết lại danh sách liên kết đôi (Lesson 04): thêm, xóa ở hai đầu và duyệt ngược.
- Giữ đúng cả hai chiều liên kết `next`, `prev` sau mỗi thao tác.

### 2. Bối cảnh

Hệ thống lưu các phiên bản nháp của một bài nộp, cũ nhất ở đầu, mới nhất ở cuối. Học viên cần xem các bản nháp theo cả hai chiều và bỏ được bản ở hai đầu.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-04

- `bai_k4.py`: tệp làm bài.
- `test_bai_k4.py`: test công khai của bài.

Ràng buộc: Tự viết trong tệp của bài: không nhập `lien_ket.py`, không chép từ bài đọc. Giữ nguyên tên lớp và tên phương thức.

### 4. Yêu cầu đầu ra

Viết năm phương thức của lớp `DoublyLinkedList` có `head`, `tail`, `size` (tệp đã cho sẵn `DNode` và `to_text`):

1. `add_first(value)`, `add_last(value)`: thêm ở hai đầu trong O(1), nối đủ cả `next` và `prev`.
2. `remove_first()`, `remove_last()`: xóa ở hai đầu trong O(1), trả về giá trị đã xóa; danh sách rỗng thì báo `IndexError("danh sách rỗng, không có phần tử để xóa")`.
3. `to_text_backward()`: trả về chuỗi các giá trị từ `tail` về `head`, đi theo `prev`.

Sau mỗi thao tác: `prev` của `head` là `None`, `next` của `tail` là `None`; xóa node duy nhất thì `head` và `tail` đều là `None`.

| Danh sách | Gọi | Kết quả |
|---|---|---|
| V1 ⇄ V2 ⇄ V3 | `to_text_backward()` | `"V3 -> V2 -> V1 -> None"` |
| V1 ⇄ V2 ⇄ V3 | `remove_last()` | `"V3"`, `tail.value` là `"V2"`, `size` 2 |
| V1 ⇄ V2 ⇄ V3 | `remove_first()` | `"V1"`, `prev` của `head` mới là `None` |
| V1 | `remove_last()` | `"V1"`, `head` và `tail` là `None` |

Giữ nguyên các tên sau trong tệp làm bài:

```python
class DNode:
class DoublyLinkedList:
    def to_text(self):
    def add_first(self, value):
    def add_last(self, value):
    def remove_first(self):
    def remove_last(self):
    def to_text_backward(self):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex04`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-04` vào kho của bạn và làm bài trong `bai_k4.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

