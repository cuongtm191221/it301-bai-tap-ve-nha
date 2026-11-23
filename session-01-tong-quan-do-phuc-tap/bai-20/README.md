# Tối ưu báo cáo cuối ngày chạy quá chậm của Shopee

### 1. Bối cảnh & Vấn đề

![Báo cáo cuối ngày chạy cả đêm với 200.000 đơn và còn làm đảo thứ tự đơn; cần viết lại cho kịp 3 giây.](minh_hoa.png)

*Báo cáo cuối ngày chạy cả đêm với 200.000 đơn và còn làm đảo thứ tự đơn; cần viết lại cho kịp 3 giây.*

Mỗi tối, hệ thống của Shopee chạy **báo cáo cuối ngày** cho một ngành hàng: tổng doanh thu, số khách mua, khách chi nhiều nhất, các đơn lớn bất thường và đơn có giá trị cao nhất. Mỗi đơn là một dict:

```plaintext
{"code": "DH06", "buyer": "dung", "amount": 1600000}
```

Bản báo cáo đang chạy cho kết quả đúng với ngày thường vài nghìn đơn, nhưng ngày sale có **200.000 đơn**: báo cáo chạy **cả đêm** chưa xong. Ngoài ra, sau khi báo cáo chạy, **thứ tự đơn** trong hệ thống bị đảo lộn, và ngày không có đơn nào thì báo cáo báo lỗi.

Bạn được giao viết bản mới `daily_report_fast`. Đây là bài **mở**: đề không chỉ ra chỗ nào chậm; bạn phải tự đọc mã, đo, tìm nguyên nhân và chọn cách viết lại.

### 2. Yêu cầu nghiệp vụ

Bản đang chạy (hàm `daily_report`, có sẵn trong `bao_cao_ngay.py`, **không sửa** để còn đối chiếu):

```python
def daily_report(orders):
    """Có sẵn: bản đang chạy. orders là list dict {"code", "buyer", "amount"}. Không sửa hàm này."""
    total = 0
    for o in orders:
        total += o["amount"]

    buyers = []
    for o in orders:
        if o["buyer"] not in buyers:
            buyers.append(o["buyer"])

    best_buyer, best_spent = None, -1
    for b in buyers:
        spent = 0
        for o in orders:
            if o["buyer"] == b:
                spent += o["amount"]
        if spent > best_spent:
            best_buyer, best_spent = b, spent

    big = []
    for o in orders:
        average = sum(x["amount"] for x in orders) / len(orders)
        if o["amount"] > 2 * average:
            big.append(o["code"])

    orders.sort(key=lambda o: o["amount"], reverse=True)
    return {"total": total, "buyers": len(buyers), "best_buyer": best_buyer,
            "big_orders": big, "largest": orders[0]["code"]}
```

Hàm `daily_report_fast(orders)` phải:

- Trả về dict **giống hệt** bản đang chạy với mọi list đơn không rỗng, gồm năm khóa: `total`, `buyers` (số khách khác nhau), `best_buyer`, `big_orders` (mã các đơn lớn hơn gấp đôi giá trị trung bình, theo thứ tự trong list), `largest` (mã đơn có giá trị cao nhất).
- Chạy xong 200.000 đơn trong **3 giây**.
- **Không sửa** list `orders`.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Hai khách chi bằng nhau:** bản đang chạy chọn khách **xuất hiện trước** trong list (ví dụ ở kịch bản chạy thử: `binh` và `dung` cùng chi 1.600.000đ, kết quả là `binh`). Bản mới phải giữ đúng quy tắc này.

**Bẫy 2 — Hai đơn cùng giá trị cao nhất:** chọn đơn đứng trước trong list.

**Bẫy 3 — Không sửa list đơn:** bản đang chạy gọi `orders.sort(...)`, làm đảo thứ tự đơn của cả hệ thống. Bản mới không được sửa.

**Bẫy 4 — Ngày không có đơn:** trả về

```plaintext
{'total': 0, 'buyers': 0, 'best_buyer': None, 'big_orders': [], 'largest': None}
```

**Bẫy 5 — 200.000 đơn của 50.000 khách:** chạy trong 3 giây. Không dùng `set`, `dict` để gom khách (sẽ học ở buổi bảng băm); hãy nghĩ cách gom các đơn của cùng một khách bằng những gì đã học trong buổi này.

**Kịch bản chạy thử.** Chạy `python bao_cao_ngay.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Bản đang chạy: {'total': 4100000, 'buyers': 4, 'best_buyer': 'binh', 'big_orders': ['DH02', 'DH06'], 'largest': 'DH06'}
Thứ tự đơn sau khi chạy: ['DH06', 'DH02', 'DH01', 'DH04', 'DH03', 'DH07', 'DH05']
Bản của bạn:   {'total': 4100000, 'buyers': 4, 'best_buyer': 'binh', 'big_orders': ['DH02', 'DH06'], 'largest': 'DH06'}
Thứ tự đơn sau khi chạy: ['DH01', 'DH02', 'DH03', 'DH04', 'DH05', 'DH06', 'DH07']
Ngày chưa có đơn: {'total': 0, 'buyers': 0, 'best_buyer': None, 'big_orders': [], 'largest': None}
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, trong trường hợp thường và trong từng bẫy.
- Chia bản đang chạy thành các phần (tổng tiền, đếm khách, khách chi nhiều nhất, đơn lớn, đơn cao nhất). Với mỗi phần, ghi số bước theo n (số đơn) và k (số khách), Big-O, và chỉ ra phần nào làm báo cáo chạy cả đêm.
- Đo bản đang chạy bằng `timeit` với n = 1.000, 2.000, 4.000; dùng tỉ lệ thời gian để kiểm chứng Big-O bạn vừa ghi.
- Với mỗi phần, mô tả cách viết lại và Big-O sau khi viết lại. Giải thích cách bản mới giữ đúng bẫy 1 và bẫy 2.
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ phụ của cả báo cáo trước và sau khi viết lại.

**(2) Triển khai code**

- Viết mã trong `bao_cao_ngay.py`; được thêm hàm phụ; không đổi tên và tham số đã có trong khung.
- Không sửa hàm `daily_report`; `daily_report_fast` không dùng `set`, `dict`, `collections` để gom khách và không sửa list `orders`.
- Xử lý đủ 5 bẫy; `python bao_cao_ngay.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 5 mục.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu công cụ đo hiệu năng `cProfile` của Python (chạy `python -m cProfile -s cumtime <tệp>`): bảng kết quả có những cột nào, đọc thế nào.
- Tạo `nghien_cuu.py` chạy `daily_report` với 3.000 đơn; dùng `cProfile` để tìm 3 dòng hoặc hàm tốn thời gian nhất. Kết quả có khớp với phân tích của bạn ở phần (1) không? Chép bảng 5 dòng đầu vào `PHAN_TICH.md` và giải thích.
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session01_Ex20`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-01-tong-quan-do-phuc-tap/bai-20 rồi chép các tệp vào kho: `bao_cao_ngay.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Viết mã trong `bao_cao_ngay.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần dùng `cProfile`.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
