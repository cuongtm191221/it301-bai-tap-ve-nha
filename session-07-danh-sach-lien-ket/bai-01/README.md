# Bài 1: Cài lại các thao tác duyệt

Mã: K1 · Mức: Cài lại · Cấp độ: Dễ · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-01` · Tệp nộp: `bai_k1.py`

### 1. Mục tiêu

- Tự viết lại các thao tác duyệt của danh sách liên kết đơn (Lesson 02): đếm, tìm, đọc theo vị trí, in ra chuỗi.
- Duyệt bằng biến `current` mà không làm thay đổi danh sách.

### 2. Bối cảnh

Phòng đào tạo lưu lộ trình học của mỗi học viên bằng một danh sách liên kết đơn, mỗi node giữ một mã khóa học. Anh Hùng cần các thao tác đọc dữ liệu trên lộ trình: đếm số khóa, tìm một khóa, xem khóa ở một vị trí và in cả lộ trình.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-01

- `bai_k1.py`: tệp làm bài.
- `test_bai_k1.py`: test công khai của bài.

Ràng buộc: Tự viết trong tệp của bài: không nhập `lien_ket.py`, không chép từ bài đọc. Giữ nguyên tên lớp và tên phương thức.

### 4. Yêu cầu đầu ra

Viết bốn phương thức của lớp `LinkedList`, đều duyệt bằng biến `current` và không làm thay đổi danh sách:

1. `count()`: trả về số node.
2. `find(value)`: trả về vị trí (tính từ 0) của node đầu tiên có giá trị `value`; không có thì trả `None`.
3. `get(position)`: trả về giá trị ở vị trí `position`; vị trí âm hoặc từ số node trở lên thì báo `IndexError("vị trí ngoài phạm vi")`.
4. `to_text()`: trả về chuỗi dạng `"KH1 -> KH2 -> None"`.

| Danh sách | Gọi | Kết quả |
|---|---|---|
| KH1 → KH2 → KH3 | `count()`, `find("KH3")`, `get(0)` | `3`, `2`, `"KH1"` |
| KH1 → KH2 → KH3 | `find("KH9")` | `None` |
| KH1 → KH2 | `get(2)` | `IndexError: vị trí ngoài phạm vi` |
| danh sách rỗng | `count()`, `to_text()` | `0`, `"None"` |

Giữ nguyên các tên sau trong tệp làm bài:

```python
class Node:
class LinkedList:
    def count(self):
    def find(self, value):
    def get(self, position):
    def to_text(self):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex01`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-01` vào kho của bạn và làm bài trong `bai_k1.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

