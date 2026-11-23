# Bài 14: Đo tỉ lệ thời gian chèn ở đầu

Mã: P2 · Mức: Phân tích · Cấp độ: Giỏi · Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Thư mục: `bai-14` · Tệp nộp: `bai_p2.py`

### 1. Mục tiêu

- Đo thời gian chèn ở đầu trên list Python và trên danh sách liên kết bằng `timeit`.
- Rút ra tỉ lệ tăng thời gian khi số phần tử gấp đôi.

### 2. Bối cảnh

Chị Lan hỏi vì sao hàng chờ có nhiều phiếu gấp nên dùng danh sách liên kết thay cho list Python. Anh Hùng muốn trả lời bằng số đo trên máy.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-14

- `bai_p2.py`: tệp làm bài.
- `test_bai_p2.py`: test công khai của bài.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.
- `dap_an_ma_hoa.py`: đáp án đã mã hóa để test đối chiếu, không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Viết `time_front_inserts(kind, n, number=1000)` trả số mili giây cho `number` lần chèn ở đầu vào cấu trúc có sẵn n phần tử: `kind == "list"` dùng `list.insert(0, x)`, `kind == "linked"` dùng `add_first`. Tạo cấu trúc trong phần chuẩn bị (`setup`) của `timeit`, đo 5 lần, lấy lần nhỏ nhất. Chạy `python bai_p2.py` với n = 50.000 và 100.000, rồi ghi vào `RATIOS` thời gian gấp khoảng bao nhiêu lần khi n gấp đôi: `"x1"`, `"x2"` hoặc `"x4"`.

Giữ nguyên các tên sau trong tệp làm bài:

```python
def time_front_inserts(kind, n, number=1000):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex14`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-14` vào kho của bạn và làm bài trong `bai_p2.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

