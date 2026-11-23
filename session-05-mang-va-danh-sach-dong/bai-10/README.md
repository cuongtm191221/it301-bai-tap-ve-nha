# Hàng chờ đơn GrabFood ở bếp trung tâm với số chỗ cố định

### 1. Bối cảnh & Vấn đề

![Bếp trung tâm nhận hàng trăm nghìn đơn mỗi ngày; hàng chờ trên màn hình bếp chỉ có 50 chỗ và không được chậm dần theo thời gian.](minh_hoa.png)

*Bếp trung tâm nhận hàng trăm nghìn đơn mỗi ngày; hàng chờ trên màn hình bếp chỉ có 50 chỗ và không được chậm dần theo thời gian.*

Bếp trung tâm của GrabFood (một bếp nấu cho nhiều thương hiệu) có màn hình **hàng chờ đơn**: đơn vào trước được nấu trước. Màn hình chạy trên thiết bị nhỏ, **bộ nhớ cấp sẵn đúng `capacity` chỗ** (ví dụ 50) và không được cấp thêm; hàng đầy thì đơn mới bị từ chối để hệ thống chuyển sang bếp khác.

Bản cũ dùng list Python và `pop(0)` để lấy đơn đầu hàng; mỗi lần lấy phải dồn mọi đơn còn lại lên một ô. Một ngày bếp nhận **200.000 đơn**, nhóm muốn mỗi thao tác lấy đơn và thêm đơn đều **O(1)**, không dồn phần tử nào.

Đầu bếp nhìn màn hình để biết món nào nấu tiếp; nếu màn hình đưa sai thứ tự, đơn đặt trước bị nấu sau, khách chờ quá 30 phút và được hoàn tiền theo chính sách của GrabFood. Nhóm vận hành cũng ghi nhận thiết bị chậm dần vào cuối ca, đúng lúc hàng chờ dài nhất. Đó là lý do nhóm muốn mỗi thao tác tốn thời gian như nhau dù hàng đã có bao nhiêu đơn, và không bao giờ cấp thêm bộ nhớ.

Lớp `KitchenQueue` đã có sẵn phần tạo vùng lưu trữ cố định `_data = [None] * capacity`. Bạn tự thêm các thuộc tính cần thiết vào `__init__` và viết các phương thức.

### 2. Yêu cầu nghiệp vụ

**2.1. `KitchenQueue(capacity)`**: `capacity` phải là số nguyên dương, nếu không báo `ValueError("Sức chứa phải là số nguyên dương")`.

**2.2. `enqueue(code)`**: thêm đơn vào cuối hàng, trả `True`; hàng đầy trả `False` và hàng giữ nguyên.

**2.3. `dequeue()`**: lấy và xóa đơn đứng đầu, trả mã đơn; hàng rỗng trả `None`.

**2.4. `peek()`, `size()`, `is_full()`, `to_list()`**: đơn đứng đầu (không xóa, rỗng trả `None`); số đơn đang chờ; hàng đã đầy chưa; list các đơn từ đầu tới cuối hàng.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Đầy và rỗng.** Hàng 2 chỗ: thêm đơn thứ ba trả `False`; lấy khi rỗng trả `None`.

**Bẫy 2 — Chỗ trống ở đầu vùng lưu trữ.** Hàng 3 chỗ đã đầy, lấy 2 đơn, thêm 2 đơn mới: các đơn mới phải dùng **chỗ trống ở đầu vùng**, thứ tự vẫn là đơn cũ trước, đơn mới sau.

**Bẫy 3 — Hàng 1 chỗ.** Thêm, lấy xen kẽ nhiều lần vẫn đúng.

**Bẫy 4 — Không giữ tham chiếu thừa.** Sau khi lấy hết đơn, mọi ô trong `_data` là `None`.

**Bẫy 5 — Không dồn, không thêm bớt ô.** Không dùng `pop`, `insert`, `append`, `remove`, `del` trên vùng lưu trữ; 200.000 lượt thêm và lấy phải xong trong 1 giây.

**Kịch bản chạy thử.** Chạy `python hang_cho_vong.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Thêm 4 đơn: [True, True, True, False]
Nấu: GF1 | đầu hàng: GF2 | hàng: ['GF2', 'GF3']
Thêm GF5: True | hàng: ['GF2', 'GF3', 'GF5'] | đầy: True
Nấu hết: ['GF2', 'GF3', 'GF5', None] | còn: 0
200.000 đơn, đã nấu: 199960 | đang chờ: 40 | đầu hàng: GF199960
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng hàm hoặc phương thức, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Thiết kế giải pháp: cần lưu thêm những thông tin nào để biết đơn đầu hàng ở ô nào và đơn mới phải ghi vào ô nào, mà không dồn phần tử? Vẽ vùng lưu trữ 3 ô qua từng bước của bẫy 2.
- Viết công thức tính ô ghi đơn mới và ô của đơn đầu hàng sau khi lấy; giải thích cách "quay về đầu vùng" khi chạm ô cuối.
- So sánh với bản cũ dùng list và `pop(0)`: số tham chiếu phải dịch khi lấy 200.000 đơn từ hàng 50 chỗ.
- Nếu sau này bếp được cấp thêm bộ nhớ và muốn hàng tự mở rộng khi đầy (như mảng động), việc chép sang vùng mới phải giữ đúng thứ tự đơn thế nào khi đơn đầu hàng không nằm ở ô 0?
- Bộ dữ liệu thử: lập bảng ít nhất 6 đầu vào phủ đủ 5 bẫy ở mục 3, mỗi dòng ghi kết quả mong đợi (tính tay trước khi chạy) và kết quả chạy thật của bài làm.
- Độ phức tạp: ghi Big-O thời gian của sáu thao tác và bộ nhớ phụ theo capacity.

**(2) Triển khai code**

- Viết thân các hàm, phương thức còn trống trong `hang_cho_vong.py`. Không đổi tên, tham số, thông báo lỗi; hàm ghi "Có sẵn" giữ nguyên; được thêm thuộc tính và hàm phụ.
- Vùng lưu trữ cố định `capacity` ô: không `pop`, `insert`, `append`, `remove`, `del` trên `_data`.
- Xử lý đủ 5 bẫy ở mục 3; `python hang_cho_vong.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test có sẵn.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ quyết định độ phức tạp.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex10`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-10 rồi chép các tệp vào kho: `hang_cho_vong.py`, `test_hang_cho_vong.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `hang_cho_vong.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
