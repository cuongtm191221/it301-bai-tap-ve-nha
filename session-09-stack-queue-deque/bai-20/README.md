# Tối ưu hàng in phiếu giao hàng ở kho Tiki

### 1. Bối cảnh & Vấn đề

![Ngày hội mua sắm, hàng in phiếu giao hàng có hàng chục nghìn phiếu; máy in chờ phần mềm chứ không phải ngược lại.](minh_hoa.png)

*Ngày hội mua sắm, hàng in phiếu giao hàng có hàng chục nghìn phiếu; máy in chờ phần mềm chứ không phải ngược lại.*

Ở kho Tiki, mỗi đơn hàng đã đóng gói cần một **phiếu giao hàng** dán lên thùng. Phần mềm của kho giữ một **hàng in**: nhân viên đóng gói quét mã đơn để thêm phiếu, trưởng ca có thể đẩy đơn giao nhanh (TikiNOW) lên **đầu hàng**, và máy in lấy phiếu ở đầu hàng ra in. Các lệnh được ghi lại dạng chữ:

| Lệnh | Ý nghĩa |
|---|---|
| `ADD <mã>` | thêm phiếu vào cuối hàng; mã đang chờ thì bỏ qua |
| `URGENT <mã>` | đưa phiếu lên đầu hàng; mã đang chờ thì bỏ qua |
| `PRINT` | in phiếu đầu hàng; hàng rỗng thì bỏ qua |

Hàm `print_order_slow(commands)` (có sẵn trong tệp, **không được sửa**) là bản đang chạy: kết quả đúng, nhưng ngày hội mua sắm, một ca có **200.000 lệnh** và hàng chờ lên hàng chục nghìn phiếu, máy in đứng chờ phần mềm. Đọc kỹ bản cũ, bạn sẽ thấy nó dùng gần như mọi thao tác "đắt" của list đã gặp trong buổi: tìm theo giá trị, chèn đầu, lấy đầu, nối list tạo list mới.

Nhóm vận hành kho yêu cầu bản mới cho **kết quả giống hệt** bản cũ với mọi chuỗi lệnh, vì thứ tự in quyết định thứ tự xe lấy hàng, và yêu cầu kèm **số đo** chứng minh bản mới nhanh hơn ở nhiều kích thước dữ liệu, không chỉ một lần chạy với dữ liệu nhỏ.

Bài này tổng hợp kiến thức cả buổi: queue (vào trước ra trước), thao tác ở cả hai đầu của deque, chi phí `pop(0)`, `insert(0, ...)`, `in` trên list, so khớp hai bản cài bằng dữ liệu ngẫu nhiên.

### 2. Yêu cầu nghiệp vụ

**2.1. `print_order_fast(commands)`**: trả về bộ `(list mã đã in theo thứ tự, list mã còn chờ từ đầu đến cuối hàng)` giống `print_order_slow`; không sửa `commands`; cả hai phần tử của bộ đều là `list`.

**2.2. `print_summary(commands)`**: dùng `print_order_fast`, trả về một dòng:

```plaintext
In 4 phiếu, còn chờ 1: TK8
In 1 phiếu, còn chờ 0
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ với dữ liệu ngẫu nhiên.** Test so sánh hai bản trên 200 chuỗi lệnh ngẫu nhiên, có mã lặp lại nhiều lần.

**Bẫy 2 — Nhiều lệnh URGENT.** `URGENT A`, `URGENT B` thì B in trước A; `URGENT A` khi A đang chờ thì không đổi chỗ.

**Bẫy 3 — In rồi thêm lại.** Mã đã in không còn "đang chờ", nên `ADD` hoặc `URGENT` mã đó lần nữa được nhận.

**Bẫy 4 — Hàng rỗng, chuỗi lệnh rỗng.** `PRINT` khi rỗng bị bỏ qua; kiểu trả về vẫn là list.

**Bẫy 5 — 200.000 lệnh trong 1 giây.** Bản cũ với cùng dữ liệu chạy rất lâu, nên đừng chạy `print_order_slow` với 200.000 lệnh khi thử.

**Kịch bản chạy thử.** Chạy `python hang_in_phieu.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
(['TK8', 'TK9', 'TK1', 'TK2'], ['TK8'])
(['TK8', 'TK9', 'TK1', 'TK2'], ['TK8'])
In 4 phiếu, còn chờ 1: TK8
In 1 phiếu, còn chờ 0
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, phương thức, trong trường hợp thường và trong từng bẫy.
- Lập bảng các thao tác của `print_order_slow`: mỗi thao tác làm gì, chi phí theo n (số phiếu đang chờ) hoặc theo số phiếu đã in, Big-O của cả hàm với m lệnh.
- Thiết kế `print_order_fast`: mỗi thao tác của bản cũ được thay bằng gì; làm sao kiểm tra "mã đang chờ" mà không duyệt hàng; khi in một phiếu cần cập nhật những gì.
- Chạy tay kịch bản chạy thử với cấu trúc của bạn.
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của hai bản theo m (số lệnh).

**(2) Triển khai code**

- Viết mã trong `hang_in_phieu.py`; được thêm thuộc tính, hàm phụ; không đổi tên và tham số đã có trong khung; hàm ghi "Có sẵn" giữ nguyên.
- `print_order_fast` không gọi `print_order_slow`; không dùng `pop(0)`, `insert(0, ...)`, `in` trên list, `+` để nối list trong vòng lặp.
- Xử lý đủ 5 bẫy; `python hang_in_phieu.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 6 test có sẵn.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Kho muốn mở rộng: mỗi phiếu có **mức ưu tiên** từ 1 đến 5, phiếu mức cao in trước, cùng mức thì đến trước in trước. Deque không còn đủ. Tìm hiểu module `heapq` (hàng đợi ưu tiên) của thư viện chuẩn và cách giữ thứ tự đến trước khi cùng mức.
- Tạo `nghien_cuu.py`: cài hai cách sắp n phiếu theo ưu tiên, `heapq` và list luôn giữ sắp xếp bằng `bisect.insort`; kiểm tra hai cách cho cùng thứ tự rồi đo bằng `timeit` với n = 25.000, 50.000, 100.000. n gấp đôi thì mỗi cách chậm đi bao nhiêu lần? Vì sao?
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex20`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-20 rồi chép các tệp vào kho: `hang_in_phieu.py`, `test_hang_in_phieu.py`, `PHAN_TICH.md`.
3. Viết mã trong `hang_in_phieu.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần nghiên cứu.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
