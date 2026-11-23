# Bài 18: Tách bảng điểm thành đạt và chưa đạt

Mã: S2 · Mức: Sáng tạo · Cấp độ: Xuất sắc · Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Thư mục: `bai-18` · Tệp nộp: `bai_s2.py`

### 1. Mục tiêu

- Tạo hai danh sách mới từ một danh sách trong một lần duyệt mà không làm đổi dữ liệu gốc.
- Tự viết test cho các trường hợp biên và giải thích chi phí của cách làm.

### 2. Bối cảnh

Bảng điểm một bài kiểm tra lưu trong `LinkedList` theo thứ tự nộp. Chị Lan cần tách thành hai danh sách: đạt và chưa đạt.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-18

- `bai_s2.py`: tệp làm bài.
- `test_bai_s2.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

Bạn tự chọn cách làm và ghi lý do, Big-O vào biến `GIAI_THICH`. Bạn tự viết hàm `tu_kiem_tra()` có ít nhất 3 lệnh `assert`, trong đó có trường hợp biên (rỗng, một phần tử, trúng `head` hoặc `tail`).

### 4. Yêu cầu đầu ra

Viết `split_by_score(scores, threshold)` trả bộ (passed, failed) là hai `LinkedList` mới: passed gồm điểm ≥ threshold, failed gồm điểm còn lại, giữ đúng thứ tự cũ. Không làm thay đổi `scores`; thời gian O(n).

| Đầu vào | threshold | Đầu ra |
|---|---|---|
| 7 → 4 → 9 → 5 → 3 | 5 | passed 7 → 9 → 5, failed 4 → 3 |

Giữ nguyên các tên sau trong tệp làm bài:

```python
def split_by_score(scores, threshold):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex18`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-18` vào kho của bạn và làm bài trong `bai_s2.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

