# IT-301 Cấu trúc dữ liệu và giải thuật: tệp khởi đầu bài tập về nhà

Kho này chứa tệp khởi đầu và test của bài tập về nhà. Đề bài từng bài xem trên hệ thống học tập; mỗi thư mục cũng có `DE_BAI.md` chứa toàn bộ đề của buổi.

| Thư mục | Buổi học |
|---|---|
| `session-07-danh-sach-lien-ket/` | Session 07: Danh sách liên kết (20 bài: K1–K4, C1–C4, N1–N4, P1–P4, S1–S4) |

## Cách làm và nộp bài

1. Tạo một kho GitHub của riêng bạn từ kho này (nút **Fork**, hoặc **Use this template** nếu có), rồi tải về máy bằng `git clone`.
2. Vào thư mục của buổi học, làm bài trong tệp `bai_xx.py` của bài được giao. Không đổi tên tệp, tên hàm, tên lớp.
3. Tự kiểm tra tại máy (cần Python 3.10 trở lên):

   ```bash
   pip install pytest
   cd session-07-danh-sach-lien-ket
   pytest -q test_bai_k1.py      # kiểm tra một bài
   pytest -q                     # kiểm tra mọi bài
   ```

   Lúc mới nhận đề, mọi test đều đỏ. Bài xong khi test của bài đó xanh.
4. Đưa bài làm lên kho của bạn (`git add`, `git commit`, `git push`) và nộp **link kho của bạn** vào bài tập tương ứng trên hệ thống.

## Quy định

- Mức AI được dùng ghi ở từng bài (AI-0: tự làm, không dùng AI; AI-2: được dùng AI và phải ghi nhật ký).
- Không sửa các tệp dùng chung (`lien_ket.py`, `dap_an_ma_hoa.py`) và các tệp `test_bai_xx.py` có sẵn; bạn được thêm test của riêng mình.
- Giảng viên chấm thêm bằng một bộ kiểm tra riêng với dữ liệu khác đề và các trường hợp biên.
