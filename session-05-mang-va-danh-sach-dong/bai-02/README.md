# Lỗi nhật ký chuyến đi GrabBike và bản mô phỏng mảng động

### 1. Bối cảnh nghiệp vụ

![Ghi nhật ký 100.000 chuyến làm máy chủ treo, báo cáo dung lượng thấp bất thường, mô phỏng đếm sai số lần chép.](minh_hoa.png)

*Ghi nhật ký 100.000 chuyến làm máy chủ treo, báo cáo dung lượng thấp bất thường, mô phỏng đếm sai số lần chép.*

Bạn là kỹ sư phần mềm trong nhóm dữ liệu của Grab.

Mỗi tối, hệ thống gom **nhật ký chuyến đi** GrabBike trong ngày vào một list theo đúng thứ tự (một điểm đón lớn có hơn 100.000 chuyến), rồi báo cáo **dung lượng bộ nhớ** của nhật ký để nhóm hạ tầng dự trù máy chủ.

Để giải thích cho nhóm hạ tầng vì sao list Python ghi thêm nhanh, nhóm viết thêm hàm `simulate_append(n, capacity=1)` mô phỏng mảng động như Lesson 02: khi đầy, cấp vùng mới **gấp đôi** và **chép mọi tham chiếu đang có** sang vùng mới. Hàm trả về (capacity cuối, tổng số tham chiếu đã chép). Ví dụ 5 lần append: capacity đi từ 1 lên 2, 4, 8; các lần chép 1 + 2 + 4 = 7 tham chiếu.

Ba hàm trong `nhat_ky.py`:

- `simulate_append(n, capacity=1)`: mô phỏng như trên.
- `build_log(events)`: list mới chứa các sự kiện theo thứ tự.
- `log_bytes(log)`: tổng số byte của nhật ký, gồm **phần list và mọi bản ghi** trong đó.

Kịch bản kiểm tra (đoạn cuối tệp): mô phỏng 1, 5, 10, 1.000 lần append; ghi nhật ký 5 chuyến; dung lượng của nhật ký có một bản ghi dài; ghi nhật ký 100.000 chuyến.

Kết quả đúng cần hiển thị:

```plaintext
1 lần append: (capacity, số tham chiếu đã chép) = (1, 0)
5 lần append: (capacity, số tham chiếu đã chép) = (8, 7)
10 lần append: (capacity, số tham chiếu đã chép) = (16, 15)
1000 lần append: (capacity, số tham chiếu đã chép) = (1024, 1023)
Nhật ký 5 chuyến: ['GB2000', 'GB2001', 'GB2002', 'GB2003', 'GB2004']
Byte của nhật ký 1 bản ghi dài lớn hơn 400: True
Nhật ký 100.000 chuyến: 100000 dòng
```

### 2. Vấn đề hiện tại

Nhóm hạ tầng phản ánh:

- Bản mô phỏng báo 1.000 lần append chỉ chép **10** tham chiếu: con số quá đẹp, không khớp lý thuyết.
- Nhật ký một bản ghi dài hơn 400 ký tự lại được báo dung lượng chưa tới 400 byte.
- Gom nhật ký 100.000 chuyến làm tác vụ tối **chạy mãi không xong**, trong khi gom 1.000 chuyến thì rất nhanh.

Nhắc lại kiến thức (Lesson 02):

- list lưu **tham chiếu** trong một vùng liền nhau. Khi đầy, CPython cấp vùng lớn hơn và chép các tham chiếu sang; nhờ vùng tăng theo cấp số nhân, `append` là **O(1) khấu hao**.
- `a = a + [x]` tạo **list mới** và chép toàn bộ a mỗi lần: n lần là O(n²).
- `sys.getsizeof(list)` chỉ đo phần list (vùng tham chiếu), **không** gồm các đối tượng mà list trỏ tới.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `nhat_ky.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Nhật ký chuyến đi GrabBike và mô phỏng mảng động."""
import sys


def simulate_append(n, capacity=1):
    # Mô phỏng n lần append vào mảng động: đầy thì cấp vùng gấp đôi và chép mọi tham chiếu đang có sang.
    # Trả về (capacity cuối, tổng số tham chiếu đã chép).
    size = 0
    copies = 0
    for _ in range(n):
        if size == capacity:
            copies += 1
            capacity *= 2
        size += 1
    return capacity, copies


def build_log(events):
    # Nhật ký chuyến đi: list mới chứa các sự kiện theo đúng thứ tự.
    log = []
    for event in events:
        log = log + [event]
    return log


def log_bytes(log):
    # Tổng số byte của nhật ký: phần list và mọi bản ghi trong đó.
    return sys.getsizeof(log)


for n in (1, 5, 10, 1000):
    print(f"{n} lần append:", "(capacity, số tham chiếu đã chép) =", simulate_append(n))
log = build_log([f"GB{2000 + k}" for k in range(5)])
print("Nhật ký 5 chuyến:", log)
record = "GB2001 | Nguyễn Văn An | Quận 1 -> Quận 7 | " + "ghi chú " * 50
print("Byte của nhật ký 1 bản ghi dài lớn hơn 400:", log_bytes([record]) > 400)
print("Nhật ký 100.000 chuyến:", len(build_log([f"GB{k}" for k in range(100000)])), "dòng")
```

Kết quả hiển thị trên Console:

```plaintext
1 lần append: (capacity, số tham chiếu đã chép) = (1, 0)
5 lần append: (capacity, số tham chiếu đã chép) = (8, 3)
10 lần append: (capacity, số tham chiếu đã chép) = (16, 4)
1000 lần append: (capacity, số tham chiếu đã chép) = (1024, 10)
Nhật ký 5 chuyến: ['GB2000', 'GB2001', 'GB2002', 'GB2003', 'GB2004']
Byte của nhật ký 1 bản ghi dài lớn hơn 400: False
(chương trình đứng yên, không in thêm gì; phải bấm Ctrl + C để dừng)
```

Đối chiếu với kết quả đúng: capacity đúng nhưng số tham chiếu đã chép sai từ 5 lần append trở lên; dung lượng báo `False`; dòng 100.000 chuyến phải chờ rất lâu mới in ra (trong lần chạy thử, quá 3 giây vẫn chưa xong).

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Lập bảng các lần mở rộng khi mô phỏng 10 lần append: lúc đó size là bao nhiêu, phải chép bao nhiêu tham chiếu. Dòng nào trong `simulate_append` đếm sai?
- Với n = 2ᵏ lần append, tổng số tham chiếu đã chép là bao nhiêu? Từ đó giải thích "O(1) khấu hao".
- Mỗi lần `log = log + [event]` chép bao nhiêu tham chiếu? Tổng cho 100.000 sự kiện khoảng bao nhiêu? Ghi Big-O.
- Đo thời gian `build_log` của mã hiện tại với 5.000, 10.000, 20.000 sự kiện. Thời gian tăng thế nào khi n gấp đôi?
- `sys.getsizeof(log)` đo phần nào của nhật ký? Vì sao list chứa một bản ghi 1.000 ký tự vẫn có `getsizeof` nhỏ?
- Ghi ba bộ dữ liệu thử bạn dùng cho `simulate_append` và `log_bytes`, kèm kết quả mong đợi.

**(2) Sửa lỗi**

- Sửa ba hàm trong `nhat_ky.py`. Không đổi tên hàm, tham số và dạng giá trị trả về.
- Ghi nhật ký 100.000 chuyến phải xong trong 1 giây.
- Chạy `python nhat_ky.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex02`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-02 rồi chép các tệp vào kho: `nhat_ky.py`, `test_nhat_ky.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `nhat_ky.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
