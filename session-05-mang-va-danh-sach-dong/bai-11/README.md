# Gộp danh sách đơn GrabFood từ hai máy chủ theo giờ đặt

### 1. Bối cảnh & Vấn đề

![Hai máy chủ mỗi bên giữ hàng trăm nghìn đơn đã xếp theo giờ; báo cáo cần một danh sách chung, đúng thứ tự, không đơn nào bị ghi hai lần.](minh_hoa.png)

*Hai máy chủ mỗi bên giữ hàng trăm nghìn đơn đã xếp theo giờ; báo cáo cần một danh sách chung, đúng thứ tự, không đơn nào bị ghi hai lần.*

Đơn GrabFood được ghi ở **hai máy chủ** (hai khu vực). Mỗi máy chủ xuất một list đơn **đã xếp tăng dần theo giờ đặt**, mỗi đơn là bộ `(giờ "HH:MM", mã đơn)`:

```plaintext
Máy chủ A: [("07:05", "GF1001"), ("07:20", "GF1003"), ("08:10", "GF1006")]
Máy chủ B: [("07:10", "GF1002"), ("07:20", "GF1004"), ("07:20", "GF1003"), ("09:00", "GF1009")]
```

Bộ phận báo cáo cần **một list chung** xếp theo giờ. Do lỗi đồng bộ, một số đơn được **ghi ở cả hai máy chủ** (cùng giờ, cùng mã, như `GF1003` ở trên); đơn đó chỉ được tính một lần.

Báo cáo này được dùng để trả tiền cho nhà hàng và tài xế: đơn bị đếm hai lần là trả tiền hai lần, đơn bị mất là nhà hàng khiếu nại. Thứ tự theo giờ còn dùng để tính thời gian chờ trung bình theo từng khung giờ, nên đơn đứng sai chỗ làm sai cả chỉ số vận hành.

Mỗi bên có tới **100.000 đơn**, báo cáo chạy mỗi giờ. Một bạn trong nhóm định nối hai list rồi gọi `sort()`; trưởng nhóm muốn tận dụng việc hai list **đã có thứ tự** để chỉ duyệt mỗi đơn một lần, không sắp xếp lại. Hai list gốc còn dùng cho đối soát nên **không được sửa**.

### 2. Yêu cầu nghiệp vụ

**2.1. `merge_by_time(first, second)`**: list **mới** gồm mọi đơn của hai list, xếp tăng dần theo giờ; cùng giờ thì đơn của `first` đứng trước, các đơn trong cùng một list giữ nguyên thứ tự.

**2.2. `merge_unique(first, second)`**: như trên nhưng bỏ đơn **cùng giờ và cùng mã** với một đơn đã giữ; trả về bộ (list mới, số đơn đã bỏ).

**2.3. `merge_report(first, second)`**: một dòng báo cáo:

```plaintext
Gộp 6 đơn (bỏ 1 đơn trùng), đơn đầu 07:05 GF1001, đơn cuối 09:00 GF1009.
Không có đơn nào.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Một bên rỗng.** Kết quả là bản sao của bên còn lại (không phải chính list đó). Hai bên rỗng: list rỗng và "Không có đơn nào."

**Bẫy 2 — Cùng giờ.** `[("07:00", "A1"), ("07:00", "A2")]` gộp với `[("07:00", "B1")]` ra A1, A2, B1.

**Bẫy 3 — Đơn trùng không đứng liền nhau.** Trong ví dụ, giữa hai bản `GF1003` có `GF1004` cùng giờ 07:20; vẫn phải nhận ra trùng.

**Bẫy 4 — Không sửa hai list gốc.**

**Bẫy 5 — Dữ liệu lớn.** Hai list 100.000 đơn mỗi bên gộp trong 1 giây, không gọi `sort`, `sorted`, `pop`, `insert`.

**Kịch bản chạy thử.** Chạy `python gop_don.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
[('07:05', 'GF1001'), ('07:10', 'GF1002'), ('07:20', 'GF1003'), ('07:20', 'GF1004'), ('07:20', 'GF1003'), ('08:10', 'GF1006'), ('09:00', 'GF1009')]
Gộp 6 đơn (bỏ 1 đơn trùng), đơn đầu 07:05 GF1001, đơn cuối 09:00 GF1009.
Gộp 1 đơn (bỏ 0 đơn trùng), đơn đầu 06:00 GF0001, đơn cuối 06:00 GF0001.
Không có đơn nào.
Máy chủ A vẫn giữ nguyên: [('07:05', 'GF1001'), ('07:20', 'GF1003'), ('08:10', 'GF1006')]
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng hàm hoặc phương thức, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Thiết kế giải pháp: mô tả cách duyệt hai list cùng lúc chỉ một lượt (cần mấy biến chỉ số, mỗi bước so sánh gì, khi một list hết thì làm gì). Chạy tay trên ví dụ ở mục 1, ghi hai chỉ số sau mỗi bước.
- Để nhận ra đơn trùng mà không so với **mọi** đơn đã giữ, cần xét những đơn nào? Vì sao chỉ cần như vậy là đủ?
- So sánh với cách nối hai list rồi `sort()`: số phép so sánh, Big-O.
- Nếu sau này có thêm máy chủ thứ ba, bạn dùng lại hai hàm đã viết thế nào? Tổng chi phí khi gộp lần lượt ba list có n đơn mỗi list là bao nhiêu?
- Bộ dữ liệu thử: lập bảng ít nhất 6 đầu vào phủ đủ 5 bẫy ở mục 3, mỗi dòng ghi kết quả mong đợi (tính tay trước khi chạy) và kết quả chạy thật của bài làm.
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của ba hàm theo n, m (số đơn mỗi bên) và k (số đơn nhiều nhất trong cùng một phút).

**(2) Triển khai code**

- Viết thân các hàm, phương thức còn trống trong `gop_don.py`. Không đổi tên, tham số, thông báo lỗi; hàm ghi "Có sẵn" giữ nguyên; được thêm thuộc tính và hàm phụ.
- Không gọi `sort`, `sorted`; không `pop`, `insert` trên list; không sửa hai list đầu vào.
- Xử lý đủ 5 bẫy ở mục 3; `python gop_don.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test có sẵn.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ quyết định độ phức tạp.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex11`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-11 rồi chép các tệp vào kho: `gop_don.py`, `test_gop_don.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `gop_don.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
