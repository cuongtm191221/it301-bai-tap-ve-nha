# Bảng giá cước GrabCar theo vùng viết theo đặc tả

### 1. Bối cảnh & Vấn đề

![Nhiều nhóm cùng dùng một bảng giá: chỉ cần bảng giá nhận một chỉ số lạ hay một giá sai là cả hệ thống tính tiền sai.](minh_hoa.png)

*Nhiều nhóm cùng dùng một bảng giá: chỉ cần bảng giá nhận một chỉ số lạ hay một giá sai là cả hệ thống tính tiền sai.*

Giá cước GrabCar khác nhau theo **vùng** (nội thành, ven đô, sân bay...). Bảng giá được ứng dụng khách, ứng dụng tài xế và hệ thống khuyến mãi cùng dùng, nên nhóm định giá chốt **đặc tả (ADT)** trước, rồi giao bạn viết lớp `ZoneFares` đúng đặc tả. Mọi nơi khác **chỉ gọi thao tác**, không đọc thẳng dữ liệu bên trong.

Dữ liệu đến từ nhiều hệ thống: chỉ số có thể là chuỗi `"1"` (đọc từ biểu mẫu web), số thực `1.0` (từ bảng tính), thậm chí `True`; giá có thể là `0`, số âm hoặc số lẻ. Đặc tả phải chặn tất cả ngay tại bảng giá. Giờ cao điểm, hệ thống tạo **bảng giá tạm** tăng theo phần trăm; bảng gốc phải giữ nguyên để quay lại sau giờ cao điểm.

Hàm `money(amount)` (có sẵn) in số tiền có dấu chấm.

### 2. Yêu cầu nghiệp vụ

**2.1. `ZoneFares(fares)`**: tạo bảng từ list giá; mọi giá phải là **số nguyên dương**, nếu không báo `ValueError("Giá phải là số nguyên dương")`. Bảng giữ **bản sao**: list truyền vào bị sửa sau đó không ảnh hưởng bảng.

**2.2. `size()`, `get(i)`, `set(i, value)`**: số vùng; giá vùng i (i âm tính từ cuối như list); thay giá vùng i, số vùng giữ nguyên. Chỉ số không phải số nguyên báo `TypeError("Chỉ số phải là số nguyên")`; ngoài phạm vi báo `IndexError("Chỉ số ngoài phạm vi bảng giá")`; giá mới sai báo `ValueError` như trên và bảng giữ nguyên.

**2.3. `surge(percent)`**: trả về bảng giá **mới** sau khi tăng `percent` phần trăm (số nguyên từ 0 đến 100), mỗi giá làm tròn **xuống** tới 1.000đ và không nhỏ hơn 1.000đ; sai thì báo `ValueError("Mức tăng phải từ 0 đến 100")`.

**2.4. `report(board)`**: một dòng mô tả bảng, **chỉ dùng `size()` và `get()`**:

```plaintext
Vùng 1: 25.000đ | Vùng 2: 32.000đ | Vùng 3: 41.000đ
Chưa có vùng nào.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Chỉ số âm và ngoài phạm vi.** `get(-1)` là vùng cuối; `get(3)`, `get(-4)` với 3 vùng báo `IndexError`.

**Bẫy 2 — Chỉ số không phải số nguyên.** `"1"`, `1.0`, `True`, `None` đều báo `TypeError`. Lưu ý trong Python `True` cũng được coi là số nguyên 1 nếu chỉ kiểm tra bằng `isinstance`.

**Bẫy 3 — Giá sai.** `0`, `-1000`, `12000.5`, `"12000"`, `True` đều báo `ValueError`, cả khi tạo bảng và khi `set`.

**Bẫy 4 — Bảng gốc và bản sao.** `surge` không sửa bảng gốc; sửa list đầu vào sau khi tạo bảng không làm bảng đổi.

**Bẫy 5 — Mã bên ngoài chỉ dùng thao tác.** `report` phải chạy đúng với **bất kỳ đối tượng nào** có `size()` và `get()`, kể cả không phải `ZoneFares`.

**Kịch bản chạy thử.** Chạy `python bang_gia_vung.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Vùng 1: 25.000đ | Vùng 2: 32.000đ | Vùng 3: 41.000đ
Vùng cuối: 41000
Giờ cao điểm +15%: Vùng 1: 28.000đ | Vùng 2: 37.000đ | Vùng 3: 47.000đ
Bảng gốc giữ nguyên: Vùng 1: 25.000đ | Vùng 2: 33.000đ | Vùng 3: 41.000đ
get(3): IndexError - Chỉ số ngoài phạm vi bảng giá
get('1'): TypeError - Chỉ số phải là số nguyên
get(True): TypeError - Chỉ số phải là số nguyên
set(0, 0): Giá phải là số nguyên dương
Chưa có vùng nào.
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng hàm hoặc phương thức, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Thiết kế giải pháp: viết bảng đặc tả (thao tác, đầu vào hợp lệ, kết quả, lỗi) cho bốn thao tác; chỉ rõ thứ tự kiểm tra trong `get` (kiểu trước hay phạm vi trước) và lý do.
- Vì sao bảng phải giữ bản sao của list đầu vào? Vẽ sơ đồ tham chiếu khi giữ bản sao và khi không.
- Vì sao `report` chỉ được gọi `size()` và `get()`? Nếu sau này đổi cách lưu bên trong (ví dụ sang `DynamicArray` tự cài) thì phải sửa những gì?
- Bộ dữ liệu thử: lập bảng ít nhất 6 đầu vào phủ đủ 5 bẫy ở mục 3, mỗi dòng ghi kết quả mong đợi (tính tay trước khi chạy) và kết quả chạy thật của bài làm.
- Độ phức tạp: ghi Big-O thời gian của `get`, `set`, `size`, `surge`, `report` và Big-O bộ nhớ phụ của `surge` theo n (số vùng).

**(2) Triển khai code**

- Viết thân các hàm, phương thức còn trống trong `bang_gia_vung.py`. Không đổi tên, tham số, thông báo lỗi; hàm ghi "Có sẵn" giữ nguyên; được thêm thuộc tính và hàm phụ.
- Không để mã ngoài lớp đọc thẳng dữ liệu bên trong; `report` chỉ dùng `size()` và `get()`.
- Xử lý đủ 5 bẫy ở mục 3; `python bang_gia_vung.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test có sẵn.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ quyết định độ phức tạp.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex09`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-09 rồi chép các tệp vào kho: `bang_gia_vung.py`, `test_bang_gia_vung.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `bang_gia_vung.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
