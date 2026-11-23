# Báo cáo chi tiêu theo cây danh mục trên MoMo

### 1. Bối cảnh & Vấn đề

![Người dùng xếp chi tiêu vào danh mục và danh mục con nhiều cấp; báo cáo phải cộng đúng từng cấp và thụt lề theo cấp.](minh_hoa.png)

*Người dùng xếp chi tiêu vào danh mục và danh mục con nhiều cấp; báo cáo phải cộng đúng từng cấp và thụt lề theo cấp.*

Màn hình **"Quản lý chi tiêu"** của ví MoMo cho người dùng xếp giao dịch vào **danh mục**, và danh mục có thể chứa **danh mục con** nhiều cấp. Một danh mục là một bộ `(tên, list phần tử)`; mỗi phần tử là **một số tiền** (số âm là hoàn tiền) hoặc **một danh mục con** cùng dạng:

```plaintext
("Tháng 6", [
    ("Ăn uống", [120000, ("Cà phê", [45000, 30000, -30000]), 85000]),
    ("Di chuyển", [("Xe ôm", [25000, 40000]), ("Xăng", [100000])]),
    ("Hóa đơn", [350000, 220000]),
    ("Giải trí", []),
])
```

Nhóm cần ba tính năng: **tổng tiền** của một danh mục (cộng cả các danh mục con ở mọi cấp), **báo cáo nhiều dòng** thụt lề theo cấp, và **ô tìm kiếm** trả về đường dẫn tới danh mục, ví dụ `Tháng 6 > Di chuyển > Xe ôm`.

Bài này tổng hợp kiến thức cả buổi: dữ liệu có cấu trúc lặp lại chính nó (danh mục chứa danh mục) là nơi đệ quy tự nhiên nhất; cần chọn đúng trường hợp cơ sở, ghép đúng kết quả của các danh mục con, và biết độ sâu tối đa. Ứng dụng giới hạn **300 cấp** danh mục. Hàm `money(amount)` và `normalize(name)` có sẵn.

### 2. Yêu cầu nghiệp vụ

Bạn viết bốn hàm trong `danh_muc.py`.

**2.1. `category_total(category)`**: tổng tiền của danh mục, kể cả mọi danh mục con.

**2.2. `report_lines(category, level=0)`**: list dòng, mỗi danh mục một dòng `<thụt lề><tên>: <tổng>đ`, thụt 2 dấu cách cho mỗi cấp; danh mục cha đứng trước các danh mục con của nó, các danh mục con giữ đúng thứ tự trong list.

**2.3. `find_path(category, name)`**: đường dẫn từ gốc tới danh mục **đầu tiên** (theo thứ tự của báo cáo) có tên trùng `name` sau khi chuẩn hóa bằng `normalize`; không có thì `None`.

**2.4. `category_report(category)`**: toàn bộ báo cáo là một chuỗi, các dòng nối bằng ký tự xuống dòng.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Hoàn tiền.** "Cà phê" có `[45000, 30000, -30000]`: tổng 45.000đ.

**Bẫy 2 — Danh mục rỗng.** "Giải trí" chưa có giao dịch: vẫn có dòng `  Giải trí: 0đ`.

**Bẫy 3 — Tên gõ lệch.** Tìm `" xe  ÔM "` vẫn ra `Tháng 6 > Di chuyển > Xe ôm`; tìm chính tên gốc ra `Tháng 6`.

**Bẫy 4 — Tên trùng ở hai nhánh.** `("Gốc", [("A", [("Phí", [1000])]), ("Phí", [2000])])`: tìm "phí" ra `Gốc > A > Phí` (đứng trước trong báo cáo).

**Bẫy 5 — Cây sâu 300 cấp.** Cả ba hàm chạy được, không báo `RecursionError`.

**Kịch bản chạy thử.** Chạy `python danh_muc.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Tháng 6: 985.000đ
  Ăn uống: 250.000đ
    Cà phê: 45.000đ
  Di chuyển: 165.000đ
    Xe ôm: 65.000đ
    Xăng: 100.000đ
  Hóa đơn: 570.000đ
  Giải trí: 0đ
Tháng 6 > Di chuyển > Xe ôm
Tháng 6 > Ăn uống > Cà phê
None
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, trong trường hợp thường và trong từng bẫy.
- Với mỗi hàm đệ quy: ba câu hỏi kiểm tra (Lesson 01) và độ sâu call stack lớn nhất trong bối cảnh của bài. Với mỗi hàm bạn chọn viết bằng vòng lặp: vì sao không dùng đệ quy.
- Vẽ cây danh mục tháng 6 và đánh số thứ tự các lời gọi `report_lines`. Vì sao thứ tự đó chính là thứ tự dòng của báo cáo?
- `find_path` phải trả về kết quả ngay khi tìm thấy ở một danh mục con. Mô tả cách giá trị `None` và giá trị tìm thấy được truyền lên các tầng trên.
- Độ phức tạp: ghi Big-O thời gian của bốn hàm theo N (tổng số phần tử) và D (số cấp). `report_lines` gọi `category_total` ở mỗi danh mục: tổng số lần cộng với cây sâu D cấp mỗi cấp một danh mục là bao nhiêu? Đề xuất cách giảm.

**(2) Triển khai code**

- Viết mã trong `danh_muc.py`; được thêm hàm phụ; không đổi tên và tham số đã có trong khung; hàm ghi "Có sẵn" giữ nguyên.
- Ba hàm `category_total`, `report_lines`, `find_path` viết bằng đệ quy theo danh mục con. Không sửa dữ liệu đầu vào.
- Xử lý đủ 5 bẫy; `python danh_muc.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 6 mục.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu định dạng JSON và module `json` của Python (`json.loads`, `json.dumps`): JSON biểu diễn dữ liệu lồng nhau thế nào, có kiểu tuple không.
- Tạo `nghien_cuu.py`: viết một chuỗi JSON mô tả cây danh mục tháng 7 (danh mục là object có `"name"` và `"items"`), đọc bằng `json.loads`, đổi sang dạng `(tên, list)` bằng một hàm đệ quy, rồi in báo cáo bằng `category_report`.
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex19`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-19 rồi chép các tệp vào kho: `danh_muc.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Viết mã trong `danh_muc.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần nghiên cứu.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
