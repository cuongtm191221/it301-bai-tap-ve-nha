# Bài 5: Tổng thời lượng một lộ trình học

Mã: C1 · Mức: Cơ bản · Cấp độ: Trung bình · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-05` · Tệp nộp: `bai_c1.py`

### 1. Mục tiêu

- Duyệt danh sách liên kết đơn bằng biến `current` để tính một giá trị tổng hợp.
- Không làm thay đổi danh sách khi chỉ đọc.

### 2. Bối cảnh

Mỗi lộ trình học là một `LinkedList`, mỗi node giữ số phút của một bài học. Chị Lan cần biết tổng thời lượng của một lộ trình và lộ trình đó có bao nhiêu bài.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-05

- `bai_c1.py`: tệp làm bài.
- `test_bai_c1.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Viết `total_minutes(path)` trả về bộ (tổng số phút, số node đã đi qua). Duyệt bằng biến `current`; sau khi gọi, lộ trình phải còn nguyên.

| Đầu vào (giá trị các node) | Đầu ra |
|---|---|
| 45 → 30 → 60 | `(135, 3)` |
| danh sách rỗng | `(0, 0)` |

Giữ nguyên các tên sau trong tệp làm bài:

```python
def total_minutes(path):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex05`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-05` vào kho của bạn và làm bài trong `bai_c1.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

