# Quản lý bãi đỗ xe điện GrabBike nhiều hàng

### 1. Bối cảnh & Vấn đề

![Trạm sạc có bãi đỗ nhiều hàng, nhiều cột; xe đỗ một ô mà bản đồ trạm hiện xe ở cả cột đó của mọi hàng.](minh_hoa.png)

*Trạm sạc có bãi đỗ nhiều hàng, nhiều cột; xe đỗ một ô mà bản đồ trạm hiện xe ở cả cột đó của mọi hàng.*

Grab thử nghiệm **xe máy điện**: tài xế trả xe vào **trạm sạc** có bãi đỗ `rows` hàng × `cols` cột. Ứng dụng của trạm hiện bản đồ bãi; mỗi ô chứa mã xe hoặc `None` (trống). Vạch sơn trên mặt bãi đánh **số ô** từ 1, theo từng hàng, từ trái sang phải (hàng 0 có ô 1 đến `cols`, hàng 1 bắt đầu từ `cols + 1`...).

Quy tắc của trạm:

- Xe vào được xếp vào **ô trống đầu tiên**, xét hàng 0 từ trái sang phải, rồi hàng 1...
- Một xe chỉ được đỗ **một ô**; xe đã có trong bãi mà quét lại thì từ chối.
- Xe rời bãi thì ô trở về trống và được dùng cho xe tiếp theo.

Bản thử đầu tiên tạo bãi bằng `[[None] * cols] * rows`: đỗ một xe thì bản đồ hiện xe ở cùng cột của **mọi hàng**.

Bài này tổng hợp kiến thức cả buổi: mảng hai chiều, tham chiếu trong list lồng nhau, tính vị trí từ chỉ số (như tính địa chỉ ô ở Lesson 01), chi phí tìm theo giá trị.

### 2. Yêu cầu nghiệp vụ

**2.1. `make_lot(rows, cols)`**: bãi trống, mỗi hàng một list riêng; kích thước không phải số nguyên dương báo `ValueError("Kích thước bãi không hợp lệ")`.

**2.2. `find(lot, code)`, `park(lot, code)`, `leave(lot, code)`**: vị trí `(hàng, cột)` của xe hoặc `None`; đỗ xe theo quy tắc, trả vị trí hoặc `None` (xe đã có, bãi đầy); xe rời bãi, trả `True` / `False`.

**2.3. `slot_number(lot, row, col)`**: số ô in trên vạch sơn; ô ngoài bãi báo `IndexError("Ô ngoài bãi")`.

**2.4. `occupancy(lot)`**: list số xe đang đỗ ở từng hàng.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Các hàng dùng chung.** Ghi vào hàng 0 không được làm đổi hàng khác.

**Bẫy 2 — Kích thước sai.** `(0, 3)`, `(2, -1)`, `(2.0, 3)`, `("2", 3)`.

**Bẫy 3 — Xe trùng, bãi đầy.** Trả `None`, bãi giữ nguyên.

**Bẫy 4 — Ô trống ở giữa.** Xe rời ô (0, 1) thì xe tiếp theo vào đúng ô đó, không phải ô cuối của bãi.

**Bẫy 5 — Số ô.** Bãi 3 × 4: ô (1, 0) là số 5, ô (2, 3) là số 12; ô (3, 0) báo lỗi.

**Kịch bản chạy thử.** Chạy `python bai_xe.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
XE01 đỗ tại (0, 0), ô số 1
XE02 đỗ tại (0, 1), ô số 2
XE03 đỗ tại (0, 2), ô số 3
XE04 đỗ tại (1, 0), ô số 4
Đỗ lại XE02: None
XE02 rời bãi: True | XE09 rời bãi: False
XE05 đỗ tại: (0, 1) | số xe mỗi hàng: [3, 1]
XE06, XE07 đỗ tại: (1, 1) (1, 2) | bãi: [['XE01', 'XE05', 'XE03'], ['XE04', 'XE06', 'XE07']]
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, phương thức, trong trường hợp thường và trong từng bẫy.
- Vẽ sơ đồ tham chiếu của `[[None] * 3] * 2` và của cách tạo bãi bạn dùng; kiểm chứng bằng `is`.
- Viết công thức số ô từ (hàng, cột) và công thức ngược từ số ô ra (hàng, cột); kiểm tra với bãi 3 × 4.
- `park` vừa kiểm tra xe trùng vừa tìm ô trống: mỗi việc xét bao nhiêu ô trong trường hợp xấu nhất? Có cách nào chỉ duyệt bãi một lần cho cả hai việc không?
- Độ phức tạp: ghi Big-O thời gian của sáu hàm theo R (số hàng) và C (số cột), và bộ nhớ của bãi.

**(2) Triển khai code**

- Viết mã trong `bai_xe.py`; được thêm thuộc tính, hàm phụ; không đổi tên và tham số đã có trong khung; hàm ghi "Có sẵn" giữ nguyên.
- Mỗi hàng là một list riêng; `occupancy` không dùng `count` trên cả bãi gộp lại thành một list mới.
- Xử lý đủ 5 bẫy; `python bai_xe.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 6 test có sẵn.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu hai cách lưu bảng hai chiều trong Python: list lồng nhau và **một list phẳng** với chỉ số `hàng * cols + cột` (cách các mảng hai chiều được lưu liền nhau trong bộ nhớ).
- Tạo `nghien_cuu.py`: với bãi 200 × 50, so sánh bộ nhớ (`sys.getsizeof` của list ngoài cộng các list hàng, so với list phẳng) và thời gian đọc một ô 1 triệu lần bằng `timeit`. Giải thích kết quả; cách nào bạn chọn cho trạm sạc, vì sao?
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex19`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-19 rồi chép các tệp vào kho: `bai_xe.py`, `test_bai_xe.py`, `PHAN_TICH.md`.
3. Viết mã trong `bai_xe.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần nghiên cứu.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
