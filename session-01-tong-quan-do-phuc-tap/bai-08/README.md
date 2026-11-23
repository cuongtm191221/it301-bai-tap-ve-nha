# Lỗi xem lịch sử đơn hàng theo trang trên Shopee

### 1. Bối cảnh nghiệp vụ

![Khách mở trang 1 của lịch sử đơn thì không thấy đơn mới nhất, đơn cũ nhất thì biến mất.](minh_hoa.png)

*Khách mở trang 1 của lịch sử đơn thì không thấy đơn mới nhất, đơn cũ nhất thì biến mất.*

Bạn là kỹ sư phần mềm trong nhóm ứng dụng di động của Shopee.

Màn hình **"Đơn mua"** hiển thị lịch sử đơn hàng theo **trang**, mỗi trang `size` đơn, **đơn mới nhất ở trang 1**. Danh sách mã đơn của khách được lưu theo thứ tự **từ cũ đến mới**:

```plaintext
["DH8001", "DH8002", "DH8003", "DH8004", "DH8005", "DH8006", "DH8007"]
```

Với 3 đơn mỗi trang, khách thấy: trang 1 là `DH8007`, `DH8006`, `DH8005`; trang 2 là `DH8004`, `DH8003`, `DH8002`; trang 3 chỉ còn `DH8001`.

Hai hàm cần viết:

- `total_pages(n_orders, size)`: số trang cần để hiển thị hết các đơn. Trang cuối thiếu đơn vẫn là một trang.
- `get_page(orders, page, size)`: list mã đơn của trang `page` (tính từ 1), đơn mới nhất trước. Trang không tồn tại (0, số âm, quá số trang) thì trả về list rỗng.

Một khách mua nhiều có tới vài chục nghìn đơn, và mỗi lần vuốt sang trang, ứng dụng gọi `get_page` một lần. Vì vậy `get_page` chỉ được tạo list cho **đúng các đơn của trang đó**, không tạo bản sao cả danh sách.

Kịch bản kiểm tra (đoạn cuối tệp): 7 đơn, 3 đơn mỗi trang; in số trang, các trang 1 đến 4 và trang 0; cuối cùng in số trang của 6 đơn và của 0 đơn.

Kết quả đúng cần hiển thị:

```plaintext
Số trang (3 đơn mỗi trang): 3
Trang 1: ['DH8007', 'DH8006', 'DH8005']
Trang 2: ['DH8004', 'DH8003', 'DH8002']
Trang 3: ['DH8001']
Trang 0: []
Trang 4: []
Số trang của 6 đơn: 2 | của 0 đơn: 0
```

### 2. Vấn đề hiện tại

Khách hàng phản ánh:

- Mở "Đơn mua" thì **trang 1 không có đơn vừa đặt**.
- Ứng dụng báo chỉ có 2 trang, đơn **cũ nhất** `DH8001` không xem được ở đâu.
- Vào trang 0 (khi ứng dụng gửi sai số trang) lại hiện ra các đơn.

Nhóm hạ tầng thêm: mỗi lần khách vuốt sang trang, bộ nhớ ứng dụng tăng theo **toàn bộ** số đơn của khách.

Nhắc lại kiến thức (Lesson 04):

- Lát cắt, kể cả `orders[::-1]`, tạo một **list mới**: lát cắt cả danh sách tốn O(n) bộ nhớ phụ.
- Một hàm chỉ tạo list k phần tử thì bộ nhớ phụ là O(k), không phụ thuộc n.
- Trang `page` tính từ 1, nên trang 1 ứng với k = 0 đơn đã đi qua; công thức vị trí phải dùng `page - 1`.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `phan_trang.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
def total_pages(n_orders, size):
    # Số trang cần để hiển thị n_orders đơn, mỗi trang size đơn
    return n_orders // size


def get_page(orders, page, size):
    # orders xếp từ cũ đến mới. Trả về list các đơn của trang page (tính từ 1), mỗi trang size đơn,
    # đơn mới nhất đứng trước. Trang không tồn tại thì trả về list rỗng.
    newest_first = orders[::-1]
    start = page * size
    return newest_first[start:start + size]


orders = ["DH8001", "DH8002", "DH8003", "DH8004", "DH8005", "DH8006", "DH8007"]
print("Số trang (3 đơn mỗi trang):", total_pages(len(orders), 3))
print("Trang 1:", get_page(orders, 1, 3))
print("Trang 2:", get_page(orders, 2, 3))
print("Trang 3:", get_page(orders, 3, 3))
print("Trang 0:", get_page(orders, 0, 3))
print("Trang 4:", get_page(orders, 4, 3))
print("Số trang của 6 đơn:", total_pages(6, 3), "| của 0 đơn:", total_pages(0, 3))
```

Kết quả hiển thị trên Console:

```plaintext
Số trang (3 đơn mỗi trang): 2
Trang 1: ['DH8004', 'DH8003', 'DH8002']
Trang 2: ['DH8001']
Trang 3: []
Trang 0: ['DH8007', 'DH8006', 'DH8005']
Trang 4: []
Số trang của 6 đơn: 2 | của 0 đơn: 0
```

Đối chiếu với kết quả đúng: chỉ có 2 trang thay vì 3; trang 1 bắt đầu từ `DH8004` thay vì `DH8007`; trang 3 rỗng nên `DH8001` không xem được; trang 0 lại hiện ra ba đơn mới nhất.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Với 7 đơn và 3 đơn mỗi trang, `7 // 3` bằng bao nhiêu? Viết công thức số trang làm tròn lên chỉ dùng phép tính số nguyên, kiểm tra với 6 đơn, 7 đơn, 0 đơn.
- Với trang 1, mã hiện tại tính `start` bằng bao nhiêu? Đơn mới nhất nằm ở vị trí nào trong `newest_first`? Sửa công thức thế nào?
- Vì sao trang 0 lại hiện ra ba đơn? Cần kiểm tra điều kiện gì trước khi lấy đơn?
- Lát cắt `orders[::-1]` tạo thêm bao nhiêu phần tử với khách có 50.000 đơn? Bộ nhớ phụ của `get_page` hiện tại là O(?)
- Viết lại `get_page` sao cho chỉ tạo list `size` phần tử: đơn mới nhất của trang `page` nằm ở vị trí nào trong `orders`? Chạy tay với trang 2 (7 đơn, 3 đơn mỗi trang).
- Lập bảng thời gian và bộ nhớ phụ (Big-O theo n và size) của `get_page` trước và sau khi sửa.

**(2) Sửa lỗi**

- Sửa hai hàm trong `phan_trang.py`. Không đổi tên hàm, tham số và dạng giá trị trả về; `get_page` không được dùng lát cắt đảo ngược, `reverse()`, `reversed()` hay tạo bản sao cả danh sách, và không được sửa list `orders`.
- Chạy `python phan_trang.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `python kiem_tra.py` phải đạt cả 5 mục.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session01_Ex08`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-01-tong-quan-do-phuc-tap/bai-08 rồi chép các tệp vào kho: `phan_trang.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `phan_trang.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
