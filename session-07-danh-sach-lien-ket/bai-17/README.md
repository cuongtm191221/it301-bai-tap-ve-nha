# Bài 17: Gộp các lượt nộp trùng liền kề

Mã: S1 · Mức: Sáng tạo · Cấp độ: Xuất sắc · Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Thư mục: `bai-17` · Tệp nộp: `bai_s1.py`

### 1. Mục tiêu

- Xóa node ngay trong lúc duyệt với bộ nhớ phụ O(1).
- Tự viết test cho các trường hợp biên và giải thích chi phí của cách làm.

### 2. Bối cảnh

Học viên bấm nộp nhiều lần liên tiếp nên hàng chờ chấm bài có các node trùng nhau đứng cạnh nhau. Chị Lan muốn mỗi lượt nộp liên tiếp chỉ còn một node.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-17

- `bai_s1.py`: tệp làm bài.
- `test_bai_s1.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

Bạn tự chọn cách làm và ghi lý do, Big-O vào biến `GIAI_THICH`. Bạn tự viết hàm `tu_kiem_tra()` có ít nhất 3 lệnh `assert`, trong đó có trường hợp biên (rỗng, một phần tử, trúng `head` hoặc `tail`).

### 4. Yêu cầu đầu ra

Viết `dedupe_adjacent(queue)` bỏ mọi node có giá trị bằng node đứng ngay trước nó, trả về số node đã bỏ. Yêu cầu: một lần duyệt, không tạo list Python mới (bộ nhớ phụ O(1)), `tail` đúng.

| Đầu vào | Đầu ra |
|---|---|
| S1 → S1 → S2 → S2 → S2 → S3 | `3`, S1 → S2 → S3 |

Giữ nguyên các tên sau trong tệp làm bài:

```python
def dedupe_adjacent(queue):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex17`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-17` vào kho của bạn và làm bài trong `bai_s1.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

