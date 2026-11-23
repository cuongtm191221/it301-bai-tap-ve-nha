# Bài 13: Phản biện mã AI cho hàng chờ chấm bài

Mã: P1 · Mức: Phân tích · Cấp độ: Giỏi · Tầng: Nâng cao (tùy chọn) · Mức AI: AI-2 · Thư mục: `bai-13` · Tệp nộp: `bai_p1.py`, `ai_danh_sach.py`, `nhat_ky_phan_bien.md`

### 1. Mục tiêu

- Đọc và phản biện mã do AI viết: tìm trường hợp làm mã sai dù một lần chạy thử cho kết quả đúng.
- Sửa mã và ghi nhật ký giữ – sửa – loại bỏ có bằng chứng.

### 2. Bối cảnh

Anh Hùng nhờ AI viết ba hàm cho hàng chờ chấm bài trong `ai_danh_sach.py`; mỗi hàm có một dòng nhận xét của AI. Với một lần gọi trên dữ liệu thường, cả ba đều trả kết quả đúng.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-13

- `bai_p1.py`: tệp làm bài.
- `test_bai_p1.py`: test công khai của bài.
- `ai_danh_sach.py`: ba hàm do AI viết, bạn đọc và sửa trong tệp này.
- `nhat_ky_phan_bien.md`: bảng nhật ký giữ – sửa – loại bỏ, bạn điền.
- `lien_ket.py`: các lớp danh sách liên kết của bài đọc, dùng lại và không sửa.
- `dap_an_ma_hoa.py`: đáp án đã mã hóa để test đối chiếu, không sửa.

Ràng buộc: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 và hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này. Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Việc của bạn:

1. Đọc từng hàm, thử gọi hai lần liên tiếp, đối chiếu với nhận xét. Ghi `"đúng"` hoặc `"sai"` vào dict `CLAIMS`.
2. Viết `count_waiting_fixed(queue)` và `newest_submission_fixed(queue)`: cùng kết quả với bản của AI, không làm thay đổi `queue`, và `newest_submission_fixed` chạy trong O(1).
3. Điền bảng giữ – sửa – loại bỏ trong `nhat_ky_phan_bien.md`, mỗi hàm một dòng.

Giữ nguyên các tên sau trong tệp làm bài:

```python
def count_waiting_fixed(queue):
def newest_submission_fixed(queue):
```

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex13`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-13` vào kho của bạn và làm bài trong `bai_p1.py`, `ai_danh_sach.py`, `nhat_ky_phan_bien.md`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-2 (được dùng AI và phải ghi lại trong nhật ký).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

