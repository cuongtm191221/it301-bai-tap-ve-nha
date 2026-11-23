# IT-301 Cấu trúc dữ liệu và giải thuật: tệp khởi đầu bài tập về nhà

Kho này chứa tệp khởi đầu và test của bài tập về nhà. Mỗi bài có một thư mục riêng; trong thư mục có `README.md` là đề của bài đó.

| Thư mục | Buổi học | Số bài |
|---|---|---|
| `session-01-tong-quan-do-phuc-tap/` | Session 01: Tổng quan CTDL & GT và độ phức tạp | 20 bài: `bai-01` … `bai-20` |
| `session-03-de-quy/` | Session 03: Đệ quy | 20 bài: `bai-01` … `bai-20` |
| `session-05-mang-va-danh-sach-dong/` | Session 05: Mảng và danh sách động | 20 bài: `bai-01` … `bai-20` |
| `session-07-danh-sach-lien-ket/` | Session 07: Danh sách liên kết | 20 bài: `bai-01` … `bai-20` |
| `session-09-stack-queue-deque/` | Session 09: Stack, Queue và Deque | 20 bài: `bai-01` … `bai-20` |

## Cách làm và nộp một bài

1. Mở thư mục của bài (ví dụ `session-07-danh-sach-lien-ket/bai-01/`). Tệp `README.md` trong đó là đề của bài.
2. Tạo một kho GitHub **riêng cho từng bài**, đặt tên theo mẫu `[Tên Lớp]_IT301_SessionNN_ExNN`, ví dụ `KS26A_IT301_Session07_Ex01`.
3. Tải kho này về (nút **Code**, chọn **Download ZIP**) và chép các tệp trong thư mục của bài vào kho của bạn.
4. Điền phần phân tích vào `PHAN_TICH.md` và viết mã trong tệp mã của bài. Không đổi tên tệp, tên hàm, tên lớp; không sửa tệp test có sẵn.
5. Tự kiểm tra tại máy bằng Python 3.10 trở lên: chạy tệp mã để đối chiếu với kết quả mẫu trong đề, rồi chạy bộ kiểm tra có sẵn trong thư mục của bài:
   - Bài có tệp `kiem_tra.py` (các buổi trước khi học pytest): `python kiem_tra.py`.
   - Bài có tệp `test_*.py`: cài pytest một lần (`pip install pytest`) rồi chạy `pytest -q`.

6. Đưa bài làm lên kho của bạn và nộp **đường dẫn kho** vào đúng bài tập trên hệ thống.

## Quy định

- Mức AI được dùng ghi ở mục 5 của đề từng bài (AI-0: tự làm, không dùng AI; AI-1: được hỏi AI để tìm hiểu, phải ghi nguồn; AI-2: đề cho sẵn mã do AI sinh để phản biện).
- Bài làm được chấm theo cả phần phân tích trong `PHAN_TICH.md` và phần mã; giảng viên kiểm tra thêm với dữ liệu khác đề.
- Thư mục `_lms/` là tệp phục vụ việc đưa đề lên hệ thống, học viên không cần dùng.
