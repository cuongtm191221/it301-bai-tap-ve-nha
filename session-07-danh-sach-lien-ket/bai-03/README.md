# Bài 3: Cài lại thao tác xóa

Mã: K3 · Mức: Cài lại · Cấp độ: Dễ · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-03` · Tệp nộp: `bai_k3.py`

### 1. Mục tiêu

- Tự viết lại hai thao tác xóa của danh sách liên kết đơn (Lesson 03).
- Xử lý đủ bốn trường hợp biên: rỗng, một phần tử, xóa ở đầu, xóa ở cuối.

### 2. Bối cảnh

Nhân viên quầy hỗ trợ lấy phiếu ở đầu hàng chờ để xử lý. Học viên cũng có thể hủy phiếu của mình khi nó đang nằm ở bất kỳ vị trí nào trong hàng.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-03

- `bai_k3.py`: tệp làm bài.
- `test_bai_k3.py`: test công khai của bài.

Ràng buộc: Tự viết trong tệp của bài: không nhập `lien_ket.py`, không chép từ bài đọc. Giữ nguyên tên lớp và tên phương thức.

### 4. Yêu cầu đầu ra

Viết hai phương thức (tệp đã cho sẵn `add_last` và `to_text`):

1. `remove_first()`: xóa node đầu và trả về giá trị của nó; danh sách rỗng thì báo `IndexError("danh sách rỗng, không có phần tử để lấy")`.
2. `remove(value)`: xóa node đầu tiên có giá trị `value`, trả `True`; không có thì trả `False` và danh sách giữ nguyên.

Bốn trường hợp phải đúng: danh sách rỗng; xóa node duy nhất (`head` và `tail` đều là `None`); xóa node đầu; xóa node cuối (`tail` lùi về node đứng trước). `size` giảm đúng 1 mỗi lần xóa được.

| Danh sách | Gọi | Kết quả |
|---|---|---|
| YC1 → YC2 → YC3 | `remove_first()` | `"YC1"`, còn YC2 → YC3, `size` 2 |
| YC1 → YC2 → YC3 | `remove("YC3")` | `True`, `tail.value` là `"YC2"`, `size` 2 |
| YC1 | `remove_first()` | `"YC1"`, `head` và `tail` là `None`, `size` 0 |
| YC1 → YC2 | `remove("YC9")` | `False`, không đổi |

Giữ nguyên các tên sau trong tệp làm bài:

```python
class Node:
class LinkedList:
    def add_last(self, value):
    def to_text(self):
    def remove_first(self):
    def remove(self, value):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex03`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-03` vào kho của bạn và làm bài trong `bai_k3.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

