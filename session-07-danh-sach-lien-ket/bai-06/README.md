# Bài 6: Dựng hàng chờ chấm bài từ danh sách mã

Mã: C2 · Mức: Cơ bản · Cấp độ: Trung bình · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-06` · Tệp nộp: `bai_c2.py`

### 1. Mục tiêu

- Dựng một danh sách liên kết từ dữ liệu có sẵn bằng thao tác thêm ở cuối.
- Kiểm tra `head`, `tail` của danh sách vừa dựng, kể cả khi dữ liệu rỗng.

### 2. Bối cảnh

Hệ thống chấm bài nhận một list Python các mã bài nộp theo thứ tự đến và cần chuyển chúng thành hàng chờ chấm bài dạng danh sách liên kết.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-06

- `bai_c2.py`: tệp làm bài.
- `test_bai_c2.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Viết `from_codes(codes)` trả về một `LinkedList` mới chứa các mã đúng thứ tự đó: mã đầu ở `head`, mã cuối ở `tail`.

| Đầu vào | `to_text()` của kết quả | `tail.value` |
|---|---|---|
| `["BN201", "BN202", "BN203"]` | `"BN201 -> BN202 -> BN203 -> None"` | `"BN203"` |
| `[]` | `"None"` | (tail là `None`) |

Giữ nguyên các tên sau trong tệp làm bài:

```python
def from_codes(codes):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex06`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-06` vào kho của bạn và làm bài trong `bai_c2.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

