# Bài 20: Chèn điểm vào bảng đã xếp tăng dần

Mã: S4 · Mức: Sáng tạo · Cấp độ: Xuất sắc · Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Thư mục: `bai-20` · Tệp nộp: `bai_s4.py`

### 1. Mục tiêu

- Chèn vào đúng vị trí trong danh sách đã xếp thứ tự, giữ `head`, `tail` đúng.
- Tự viết test cho các trường hợp biên và giải thích chi phí của cách làm.

### 2. Bối cảnh

Bảng điểm là `LinkedList` đã xếp tăng dần. Mỗi khi có điểm mới, hệ thống phải chèn vào đúng chỗ để bảng vẫn tăng dần.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-20

- `bai_s4.py`: tệp làm bài.
- `test_bai_s4.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

Bạn tự chọn cách làm và ghi lý do, Big-O vào biến `GIAI_THICH`. Bạn tự viết hàm `tu_kiem_tra()` có ít nhất 3 lệnh `assert`, trong đó có trường hợp biên (rỗng, một phần tử, trúng `head` hoặc `tail`).

### 4. Yêu cầu đầu ra

Viết `insert_sorted(scores, value)` chèn `value` sao cho bảng vẫn tăng dần; giá trị bằng nhau thì node mới đứng sau các node bằng nó. `head` và `tail` phải đúng. Không dùng `sort()`, `sorted()`.

| Bảng | Gọi | Kết quả |
|---|---|---|
| 3 → 5 → 9 | `insert_sorted(s, 7)` | 3 → 5 → 7 → 9 |
| 3 → 5 → 7 → 9 | `insert_sorted(s, 1)` rồi `insert_sorted(s, 10)` | `head` là 1, `tail` là 10 |

Giữ nguyên các tên sau trong tệp làm bài:

```python
def insert_sorted(scores, value):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex20`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-20` vào kho của bạn và làm bài trong `bai_s4.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

