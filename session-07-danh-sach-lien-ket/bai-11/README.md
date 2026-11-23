# Bài 11: Đưa yêu cầu ưu tiên lên đầu hàng

Mã: N3 · Mức: Nâng cao · Cấp độ: Khá · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-11` · Tệp nộp: `bai_n3.py`

### 1. Mục tiêu

- Kết hợp các thao tác tìm, xóa và thêm ở đầu để di chuyển một node.
- Xử lý trường hợp node cần chuyển đang ở đầu, ở cuối hoặc không có.

### 2. Bối cảnh

Hàng chờ hỗ trợ là `LinkedList` các mã yêu cầu. Khi một yêu cầu được đánh dấu ưu tiên, chị Lan cần đưa nó lên đầu hàng.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-11

- `bai_n3.py`: tệp làm bài.
- `test_bai_n3.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Viết `move_to_front(queue, code)`: đưa node đầu tiên có giá trị `code` lên đầu hàng chờ, trả `True`; đã ở đầu thì giữ nguyên và vẫn trả `True`; không có thì trả `False`, hàng chờ không đổi. Được dùng lại các phương thức của `LinkedList`.

| Hàng chờ | Gọi | Kết quả |
|---|---|---|
| A → B → C | `move_to_front(q, "C")` | `True`, C → A → B, `tail` là B |
| A → B | `move_to_front(q, "Z")` | `False`, không đổi |

Giữ nguyên các tên sau trong tệp làm bài:

```python
def move_to_front(queue, code):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex11`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-11` vào kho của bạn và làm bài trong `bai_n3.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

