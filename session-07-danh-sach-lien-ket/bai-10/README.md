# Bài 10: Rút mọi bài nộp của một học viên

Mã: N2 · Mức: Nâng cao · Cấp độ: Khá · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-10` · Tệp nộp: `bai_n2.py`

### 1. Mục tiêu

- Xóa nhiều node trong một lần duyệt, kể cả khi các node cần xóa đứng liền nhau hoặc ở hai đầu.
- Giữ đúng `head`, `tail` sau khi xóa.

### 2. Bối cảnh

Hàng chờ chấm bài là `LinkedList` các mã học viên; một học viên có thể nộp nhiều bài. Khi học viên rút khỏi khóa, chị Lan cần xóa mọi bài của người đó.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-10

- `bai_n2.py`: tệp làm bài.
- `test_bai_n2.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Viết `remove_all(queue, code)` xóa mọi node có giá trị `code`, trả về số node đã xóa. `head` và `tail` phải đúng; xóa hết thì cả hai là `None`.

| Hàng chờ | Gọi | Kết quả |
|---|---|---|
| HV1 → HV7 → HV2 → HV7 | `remove_all(q, "HV7")` | `2`, HV1 → HV2, `tail` là HV2 |
| HV7 → HV7 | `remove_all(q, "HV7")` | `2`, `head` và `tail` là `None` |

Giữ nguyên các tên sau trong tệp làm bài:

```python
def remove_all(queue, code):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex10`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-10` vào kho của bạn và làm bài trong `bai_n2.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

