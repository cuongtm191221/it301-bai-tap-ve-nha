# Bài 19: Lịch sử bản nháp có lùi và tiến

Mã: S3 · Mức: Sáng tạo · Cấp độ: Xuất sắc · Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Thư mục: `bai-19` · Tệp nộp: `bai_s3.py`

### 1. Mục tiêu

- Thiết kế một lớp dùng các node nối hai chiều để lùi, tiến trong lịch sử với mỗi thao tác O(1).
- Tự viết test cho các trường hợp biên và giải thích chi phí của cách làm.

### 2. Bối cảnh

Trình soạn bài nộp cho học viên lùi về bản nháp trước và tiến lại bản sau, giống nút hoàn tác và làm lại.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-19

- `bai_s3.py`: tệp làm bài.
- `test_bai_s3.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

Bạn tự chọn cách làm và ghi lý do, Big-O vào biến `GIAI_THICH`. Bạn tự viết hàm `tu_kiem_tra()` có ít nhất 3 lệnh `assert`, trong đó có trường hợp biên (rỗng, một phần tử, trúng `head` hoặc `tail`).

### 4. Yêu cầu đầu ra

Viết lớp `DraftHistory` dùng các `DNode` nối hai chiều, với `save(text)`, `back()`, `forward()`, `current()` như docstring trong tệp. Lưu bản mới sau khi đã lùi thì các bản đứng sau bản đang xem bị bỏ. Mỗi thao tác O(1).

| Thao tác | Kết quả |
|---|---|
| save v1, v2, v3; back(); back(); back() | `"v2"`, `"v1"`, `None` |
| forward(); save v4; forward(); current() | `"v2"`, (không trả), `None`, `"v4"` |

Giữ nguyên các tên sau trong tệp làm bài:

```python
class DraftHistory:
    def save(self, text):
    def back(self):
    def forward(self):
    def current(self):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex19`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-19` vào kho của bạn và làm bài trong `bai_s3.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

