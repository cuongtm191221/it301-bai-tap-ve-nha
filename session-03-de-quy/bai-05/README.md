# Lỗi đếm số cách đi trong trò chơi "Lì xì" trên ví MoMo

### 1. Bối cảnh nghiệp vụ

![Bản đồ nhiều ô làm màn hình trò chơi đứng yên, bản đồ ít ô thì đếm sai số cách đi.](minh_hoa.png)

*Bản đồ nhiều ô làm màn hình trò chơi đứng yên, bản đồ ít ô thì đếm sai số cách đi.*

Bạn là kỹ sư phần mềm trong nhóm trò chơi Tết của ví MoMo.

Trò chơi **"Lì xì"**: bản đồ có một số ô xếp thành một hàng, người chơi đứng trước ô đầu tiên. Mỗi lượt, người chơi chọn tiến **1 ô** hoặc **2 ô**, đi tới ô cuối cùng thì nhận lì xì. Mỗi **cách đi** là một dãy lượt khác nhau; ví dụ bản đồ 3 ô có 3 cách đi: 1-1-1, 1-2, 2-1. Màn hình trò chơi hiện **số cách đi** để người chơi biết bản đồ "khó" hay "dễ", và hệ thống dùng con số này để chia số phần quà.

Quy ước:

- Bản đồ **0 ô**: người chơi đã ở đích, có đúng **1 cách** (không đi lượt nào).
- Số ô âm không có ý nghĩa: 0 cách.
- Nhóm thiết kế đã tạo bản đồ tới **80 ô** cho sự kiện cuối năm.

Hàm `route_count(cells)` được viết bằng đệ quy: lượt đầu tiên tiến 1 ô thì còn lại bản đồ `cells - 1` ô; tiến 2 ô thì còn lại `cells - 2` ô. Số cách đi là tổng hai trường hợp đó.

Ngày khai mạc sự kiện có hàng trăm nghìn người chơi cùng lúc, nên màn hình phải hiện số cách đi ngay, không được chờ. Nhóm sản phẩm cần bản sửa trước khi mở bản đồ lớn.

Kịch bản kiểm tra (đoạn cuối tệp): bản đồ 1, 2, 5, 10 ô, bản đồ 0 ô, rồi bản đồ 40 ô và 80 ô.

Kết quả đúng cần hiển thị:

```plaintext
Bản đồ 1 ô: 1 cách đi
Bản đồ 2 ô: 2 cách đi
Bản đồ 5 ô: 8 cách đi
Bản đồ 10 ô: 89 cách đi
Bản đồ 0 ô (đã ở đích): 1 cách đi
Bản đồ 40 ô: 165580141 cách đi
Bản đồ 80 ô: 37889062373143906 cách đi
```

### 2. Vấn đề hiện tại

Nhóm kiểm thử phản ánh:

- Bản đồ 2 ô hiện **1 cách đi**, trong khi đếm tay được 2 cách (1-1 và 2). Bản đồ 5 ô hiện 5 cách thay vì 8.
- Bản đồ 0 ô hiện 0 cách.
- Mở bản đồ 40 ô thì màn hình **đứng yên**, không hiện gì; bản đồ 80 ô không bao giờ mở được.

Nhắc lại kiến thức (Lesson 01, Lesson 04):

- Mỗi hàm đệ quy phải trả lời đúng **ba câu hỏi** (Lesson 01): (1) trường hợp cơ sở trả đúng chưa; (2) từ kết quả của bài toán nhỏ hơn, phần ghép ra kết quả lớn đúng chưa; (3) mỗi lần gọi có tiến về trường hợp cơ sở không.
- Một hàm gọi chính nó **hai lần** trên hai bài toán con chồng lấn nhau thì cùng một bài toán con bị tính đi tính lại; số lời gọi tăng theo hàm mũ, cỡ O(2ⁿ).
- `@lru_cache(maxsize=None)` (từ `functools`) ghi nhớ kết quả theo tham số: mỗi giá trị chỉ tính một lần. Cũng có thể viết lại bằng vòng lặp đi từ bài toán nhỏ lên.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `li_xi.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
def route_count(cells):
    # Số cách đi hết bản đồ cells ô, mỗi lượt tiến 1 ô hoặc 2 ô.
    # Bản đồ 0 ô: đã ở đích, có đúng 1 cách (không đi). cells âm: 0 cách.
    if cells <= 1:
        return cells
    return route_count(cells - 1) + route_count(cells - 2)


for cells in (1, 2, 5, 10):
    print(f"Bản đồ {cells} ô:", route_count(cells), "cách đi")
print("Bản đồ 0 ô (đã ở đích):", route_count(0), "cách đi")
print("Bản đồ 40 ô:", route_count(40), "cách đi")
print("Bản đồ 80 ô:", route_count(80), "cách đi")
```

Kết quả hiển thị trên Console:

```plaintext
Bản đồ 1 ô: 1 cách đi
Bản đồ 2 ô: 1 cách đi
Bản đồ 5 ô: 5 cách đi
Bản đồ 10 ô: 55 cách đi
Bản đồ 0 ô (đã ở đích): 0 cách đi
(chương trình đứng yên, không in thêm gì; phải bấm Ctrl + C để dừng)
```

Đối chiếu với kết quả đúng: bản đồ 1 ô đúng, nhưng 2, 5, 10 ô và 0 ô đều sai; tới bản đồ 40 ô thì chương trình đứng yên.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Liệt kê tay mọi cách đi của bản đồ 2, 3, 4 ô. Từ đó trả lời: `route_count(0)` và `route_count(1)` phải bằng bao nhiêu? Trường hợp cơ sở `return cells` sai ở đâu?
- Trả lời ba câu hỏi kiểm tra cho `route_count` của mã hiện tại. Với `cells` âm thì hàm trả về gì?
- Vẽ cây lời gọi của `route_count(5)`. Lời gọi `route_count(3)` và `route_count(2)` xuất hiện bao nhiêu lần?
- Thêm một biến đếm toàn cục để đo số lời gọi của `route_count(n)` với n = 10, 20, 25. Ghi bảng kết quả. Vì sao bản đồ 40 ô làm màn hình đứng yên?
- Chọn một cách cải thiện (ghi nhớ kết quả hoặc vòng lặp). Sau khi sửa, `route_count(80)` cần bao nhiêu lần tính thật sự? Ghi Big-O thời gian.
- Ghi ba bộ dữ liệu thử bạn dùng, kèm kết quả mong đợi: bản đồ 0 ô, bản đồ 4 ô, số ô âm.

**(2) Sửa lỗi**

- Sửa hàm `route_count` trong `li_xi.py`. Không đổi tên hàm, tham số.
- Bản đồ 80 ô phải có kết quả trong vòng 2 giây.
- Chạy `python li_xi.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `python kiem_tra.py` phải đạt cả 4 mục.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex05`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-05 rồi chép các tệp vào kho: `li_xi.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `li_xi.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
