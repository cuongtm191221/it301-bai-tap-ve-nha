# Bài 16: Chọn cấu trúc cho năm tình huống

Mã: P4 · Mức: Phân tích · Cấp độ: Giỏi · Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Thư mục: `bai-16` · Tệp nộp: `bai_p4.py`

### 1. Mục tiêu

- Chọn giữa list Python, danh sách liên kết đơn và danh sách liên kết đôi dựa trên chi phí của thao tác dùng nhiều nhất.

### 2. Bối cảnh

Phòng đào tạo có năm chức năng mới, mỗi chức năng dùng dữ liệu theo một cách khác nhau. Anh Hùng cần chọn cấu trúc lưu trữ cho từng chức năng.

### 3. Dữ liệu cho sẵn và ràng buộc

Thư mục khởi đầu: https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-16

- `bai_p4.py`: tệp làm bài.
- `test_bai_p4.py`: test công khai của bài.
- `dap_an_ma_hoa.py`: đáp án đã mã hóa để test đối chiếu, không sửa.

Ràng buộc: Giữ nguyên tên hàm, tên biến đã cho.

### 4. Yêu cầu đầu ra

Với mỗi tình huống, ghi vào `CHOICES` một trong ba giá trị `"list"`, `"don"` (danh sách liên kết đơn có `tail`), `"doi"` (danh sách liên kết đôi), và một câu lý do vào `LY_DO`.

| Khóa | Tình huống |
|---|---|
| `t1` | Bảng điểm 5.000 bài, giảng viên thường mở bài thứ k bất kỳ |
| `t2` | Hàng chờ phỏng vấn mentor: liên tục chen ứng viên ưu tiên lên đầu và lấy người ở đầu; không cần đi lùi |
| `t3` | Hàng chờ chấm lại: bài gấp chen lên đầu, bài thường thêm ở cuối; giảng viên lấy bài ở đầu để chấm, và hay hủy bài vừa thêm ở cuối khi học viên nộp nhầm (hàng có hàng nghìn bài) |
| `t4` | Danh sách phiếu hỗ trợ đã xử lý của quầy, giữ 20.000 phiếu gần nhất: mỗi phiếu vừa xử lý thêm vào đầu (mới nhất đứng đầu); quá 20.000 phiếu thì bỏ phiếu cũ nhất ở cuối; trang "Xem lại từ đầu ca" in từ cũ nhất đến mới nhất |
| `t5` | Danh sách khóa học: chỉ thêm ở cuối, duyệt từ đầu, thỉnh thoảng lấy khóa thứ k |

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex16`.
2. Tải kho khởi đầu về (nút Code, Download ZIP), chép các tệp trong thư mục `bai-16` vào kho của bạn và làm bài trong `bai_p4.py`.
3. Tự kiểm tra tại máy bằng Python 3.10 trở lên (lệnh ở khối bên dưới). Lúc mới nhận đề, mọi test đều đỏ; bài xong khi mọi test xanh.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.

```bash
pip install pytest
pytest -q
```

