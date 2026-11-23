# Bài 15: Dựng dữ liệu tốt nhất và xấu nhất

Mã: P3 · Mức: Phân tích · Cấp độ: Giỏi · Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Thư mục: `bai-15` · Tệp nộp: `bai_p3.py`

### 1. Mục tiêu

- Dựng dữ liệu cho trường hợp tốt nhất, xấu nhất của `find` và trường hợp biên của `remove`.

### 2. Bối cảnh

Để viết test cho hàng chờ, anh Hùng cần các bộ dữ liệu ép thao tác rơi đúng vào trường hợp tốt nhất, xấu nhất và trường hợp xóa ở cuối.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-15

- `bai_p3.py`: tệp làm bài.
- `test_bai_p3.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.
- `dap_an_ma_hoa.py`: đáp án đã mã hóa để test đối chiếu, không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Viết ba hàm, mỗi hàm trả bộ (list n mã, mã cần dùng):

- `best_case_find(n)`: `find` chỉ so sánh 1 lần.
- `worst_case_find(n)`: `find` so sánh đủ n lần rồi trả `None`.
- `tail_case_remove(n)` (n ≥ 2): `remove` xóa đúng node cuối, nên `tail` phải lùi về node đứng trước.

Ghi Big-O của `find` trong trường hợp xấu nhất vào `FIND_WORST`.

Giữ nguyên các tên sau trong tệp làm bài:

```python
def best_case_find(n):
def worst_case_find(n):
def tail_case_remove(n):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex15`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-15` vào kho của bạn và làm bài trong `bai_p3.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

