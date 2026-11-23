# Bài 8: Đọc các phiên bản nháp từ mới đến cũ

Mã: C4 · Mức: Cơ bản · Cấp độ: Trung bình · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-08` · Tệp nộp: `bai_c4.py`

### 1. Mục tiêu

- Duyệt danh sách liên kết đôi theo chiều ngược bằng liên kết `prev`.

### 2. Bối cảnh

Các phiên bản nháp bài nộp lưu trong `DoublyLinkedList`, cũ nhất ở `head`, mới nhất ở `tail`. Trang lịch sử cần hiện các bản nháp từ mới đến cũ.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-08

- `bai_c4.py`: tệp làm bài.
- `test_bai_c4.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Viết `to_list_backward(drafts)` trả list Python các giá trị từ `tail` về `head`. Phải đi theo liên kết `prev`; không duyệt xuôi rồi đảo ngược.

| Đầu vào | Đầu ra |
|---|---|
| V1 ⇄ V2 ⇄ V3 | `["V3", "V2", "V1"]` |
| danh sách rỗng | `[]` |

Giữ nguyên các tên sau trong tệp làm bài:

```python
def to_list_backward(drafts):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex08`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-08` vào kho của bạn và làm bài trong `bai_c4.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

