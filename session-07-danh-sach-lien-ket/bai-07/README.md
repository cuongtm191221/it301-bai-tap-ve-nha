# Bài 7: Big-O của sáu thao tác

Mã: C3 · Mức: Cơ bản · Cấp độ: Trung bình · Tầng: Bắt buộc · Mức AI: AI-0 · Thư mục: `bai-07` · Tệp nộp: `bai_c3.py`

### 1. Mục tiêu

- Xác định Big-O thời gian của các thao tác trên danh sách liên kết và so với list Python.

### 2. Bối cảnh

Trước khi chọn cấu trúc cho một chức năng mới, anh Hùng lập bảng chi phí của sáu thao tác thường dùng trên danh sách liên kết và trên list Python.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-07

- `bai_c3.py`: tệp làm bài.
- `test_bai_c3.py`: test công khai của bài.
- `dap_an_ma_hoa.py`: đáp án đã mã hóa để test đối chiếu, không sửa.

Ràng buộc: Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Ghi Big-O thời gian (trường hợp xấu nhất) của từng thao tác vào dict `ANSWERS`, dạng `"O(1)"` hoặc `"O(n)"`. n là số phần tử.

| Khóa | Thao tác |
|---|---|
| `"a"` | `add_first` trên `LinkedList` |
| `"b"` | `add_last` trên `LinkedList` có `tail` |
| `"c"` | `find` trên `LinkedList` |
| `"d"` | `insert(0, x)` trên list Python |
| `"e"` | đọc giá trị ở vị trí k (k gần n) trên `LinkedList` |
| `"f"` | `remove_last` trên `DoublyLinkedList` |

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex07`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-07` vào kho của bạn và làm bài trong `bai_c3.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

