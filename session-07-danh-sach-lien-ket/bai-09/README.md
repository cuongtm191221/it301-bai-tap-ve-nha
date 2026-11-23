# Bài 9: Chèn khóa bổ trợ ngay sau khóa nền

Mã: N1 · Mức: Nâng cao · Cấp độ: Khá · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-09` · Tệp nộp: `bai_n1.py`

### 1. Mục tiêu

- Chèn một node vào giữa danh sách liên kết đơn bằng cách nối lại liên kết.
- Cập nhật `tail` khi chèn sau node cuối.

### 2. Bối cảnh

Lộ trình học là `LinkedList` các mã khóa học. Anh Hùng cần chèn một khóa bổ trợ ngay sau một khóa nền.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-09

- `bai_n1.py`: tệp làm bài.
- `test_bai_n1.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Viết `insert_after(path, target, value)`: chèn `value` ngay sau node **đầu tiên** có giá trị `target`, trả `True`; không có `target` thì trả `False` và lộ trình giữ nguyên. Chèn sau node cuối thì `tail` phải chuyển sang node mới.

| Lộ trình | Gọi | Kết quả |
|---|---|---|
| KH1 → KH2 → KH3 | `insert_after(p, "KH2", "KH9")` | `True`, KH1 → KH2 → KH9 → KH3 |
| KH1 → KH2 → KH3 | `insert_after(p, "KH3", "KH8")` | `True`, `tail.value` là `"KH8"` |
| KH1 | `insert_after(p, "KH5", "KH9")` | `False`, không đổi |

Giữ nguyên các tên sau trong tệp làm bài:

```python
def insert_after(path, target, value):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex09`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-09` vào kho của bạn và làm bài trong `bai_n1.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

