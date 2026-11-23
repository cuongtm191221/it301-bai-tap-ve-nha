# Bài 12: Chỉ giữ k phiên bản nháp mới nhất

Mã: N4 · Mức: Nâng cao · Cấp độ: Khá · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-12` · Tệp nộp: `bai_n4.py`

### 1. Mục tiêu

- Xóa ở đầu danh sách liên kết đôi và giữ đúng liên kết hai chiều.
- Báo lỗi với đúng thông báo khi tham số không hợp lệ.

### 2. Bối cảnh

Để tiết kiệm bộ nhớ, hệ thống chỉ giữ k phiên bản nháp mới nhất của mỗi bài nộp; các bản cũ hơn bị bỏ.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-12

- `bai_n4.py`: tệp làm bài.
- `test_bai_n4.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Viết `keep_latest(drafts, k)` trên `DoublyLinkedList`: bỏ các phiên bản cũ ở đầu cho tới khi còn nhiều nhất k node, trả về số node đã bỏ. k âm thì báo `ValueError("số phiên bản giữ lại không được âm")`. Duyệt xuôi và duyệt ngược đều phải đúng.

| Phiên bản | Gọi | Kết quả |
|---|---|---|
| V1 ⇄ V2 ⇄ V3 ⇄ V4 ⇄ V5 | `keep_latest(d, 3)` | `2`, còn V3 ⇄ V4 ⇄ V5 |
| V1 ⇄ V2 | `keep_latest(d, 5)` | `0`, không đổi |

Giữ nguyên các tên sau trong tệp làm bài:

```python
def keep_latest(drafts, k):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex12`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-12` vào kho của bạn và làm bài trong `bai_n4.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

