# Bài 2: Cài lại thao tác thêm ở đầu và ở cuối

Mã: K2 · Mức: Cài lại · Cấp độ: Dễ · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-02` · Tệp nộp: `bai_k2.py`

### 1. Mục tiêu

- Tự viết lại hai thao tác thêm của danh sách liên kết đơn có `tail` (Lesson 03).
- Giữ đúng `head`, `tail` và `size` sau mỗi lần thêm, kể cả khi danh sách đang rỗng.

### 2. Bối cảnh

Quầy hỗ trợ học viên xếp các phiếu yêu cầu thành một hàng chờ. Phiếu thường được thêm vào cuối hàng; phiếu gấp được chị Lan cho chen lên đầu hàng. Cả hai việc phải xong ngay, dù hàng chờ dài bao nhiêu.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-02

- `bai_k2.py`: tệp làm bài.
- `test_bai_k2.py`: test công khai của bài.

Ràng buộc: Tự viết trong tệp của bài: không nhập `lien_ket.py`, không chép từ bài đọc. Giữ nguyên tên lớp và tên phương thức.

### 4. Yêu cầu đầu ra

Viết hai phương thức của lớp `LinkedList` có `head`, `tail`, `size`:

1. `add_first(value)`: thêm vào đầu trong O(1).
2. `add_last(value)`: thêm vào cuối trong O(1) nhờ `tail`, không duyệt từ `head`.

Sau mỗi lần thêm: `head` là node đầu, `tail` là node cuối, `size` tăng đúng 1. Thêm vào danh sách rỗng thì `head` và `tail` cùng trỏ tới node mới.

| Các lệnh (chạy nối tiếp trên danh sách rỗng) | `to_text()` | `tail.value` | `size` |
|---|---|---|---|
| `add_last("YC2")` | `"YC2 -> None"` | `"YC2"` | 1 |
| `add_first("YC1")` | `"YC1 -> YC2 -> None"` | `"YC2"` | 2 |
| `add_last("YC3")` | `"YC1 -> YC2 -> YC3 -> None"` | `"YC3"` | 3 |

Giữ nguyên các tên sau trong tệp làm bài:

```python
class Node:
class LinkedList:
    def add_first(self, value):
    def add_last(self, value):
    def to_text(self):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex02`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-02` vào kho của bạn và làm bài trong `bai_k2.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

