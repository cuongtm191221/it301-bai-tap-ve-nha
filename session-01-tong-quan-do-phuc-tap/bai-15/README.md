# Phản biện mã do AI viết: báo cáo khách hàng thân thiết trên Shopee

### 1. Bối cảnh & Vấn đề

![Trợ lý AI viết xong báo cáo khách thân thiết trong vài giây, ba mục kiểm tra đều đạt. Có nên dùng ngay?](minh_hoa.png)

*Trợ lý AI viết xong báo cáo khách thân thiết trong vài giây, ba mục kiểm tra đều đạt. Có nên dùng ngay?*

Mỗi quý, gian hàng trên Shopee gửi **quà tặng** cho khách hàng thân thiết: những khách có **từ `min_orders` đơn trở lên** trong quý. Dữ liệu là list mã khách của từng đơn, theo thứ tự đặt:

```plaintext
["KH03", "KH01", "kh03 ", "KH02", " kh01", "KH03"]
```

Mã khách được nhập từ nhiều kênh nên có thể bị viết thường hoặc thừa khoảng trắng: `"kh03 "` và `"KH03"` là **cùng một khách**. Báo cáo trả về list mã khách thân thiết đã chuẩn hóa (chữ hoa, không khoảng trắng), **xếp tăng dần theo mã** để bộ phận kho đóng quà theo thứ tự. Gian hàng lớn có tới **50.000 đơn** mỗi quý.

Một đồng nghiệp đã nhờ trợ lý AI viết hàm này. AI trả về đoạn mã kèm tệp `kiem_tra.py` có ba mục kiểm tra, cả ba đều đạt, và đồng nghiệp đề nghị đưa vào báo cáo quý này. Bạn là người **duyệt mã**. Quy định của nhóm: mã do AI sinh chỉ được dùng khi người duyệt đã tự chạy thử với dữ liệu của mình và chịu trách nhiệm về nó.

### 2. Mã do AI sinh

Tệp `than_thiet.py` trong thư mục khởi đầu có hàm do AI viết:

```python
def loyal_customers(buyers, min_orders):
    """Trả về list mã khách có từ min_orders đơn trở lên, xếp tăng dần theo mã."""
    # Duyệt từng đơn, đếm số đơn của khách đó, thêm vào kết quả nếu đủ điều kiện.
    # Độ phức tạp: O(n), bộ nhớ phụ O(1).
    result = []
    for b in buyers:
        if buyers.count(b) > min_orders and b not in result:
            result.append(b)
    return result
```

Lời giải thích AI gửi kèm: "Hàm duyệt từng đơn một lần, dùng `count()` để đếm số đơn của khách. Độ phức tạp O(n), bộ nhớ phụ O(1). Đã kiểm tra với ba trường hợp."

Ba mục trong `kiem_tra.py`: ví dụ 5 đơn với ngưỡng 2, danh sách không có khách đủ ngưỡng, danh sách rỗng. Chạy đoạn cuối tệp:

```plaintext
Danh sách đơn: ['KH01', 'KH02', 'KH01', 'KH03', 'KH01']
Khách có từ 2 đơn: ['KH01']
```

Kết quả trông đúng. Nhiệm vụ của bạn là tìm ra những dữ liệu mà đoạn mã này **không** xử lý đúng.

### 3. Các hướng cần kiểm chứng

Ba mục kiểm tra của AI đều dùng dữ liệu "đẹp". Hãy kiểm chứng đoạn mã với các tình huống có thật trong nghiệp vụ. Đề không cho biết tình huống nào làm lộ lỗi; bạn phải tự chạy tay hoặc chạy thử để biết.

**Hướng 1 — Ngưỡng:** khách có **đúng** `min_orders` đơn.

**Hướng 2 — Cách viết mã khách:** cùng một khách nhưng viết thường hoặc thừa khoảng trắng.

**Hướng 3 — Thứ tự kết quả:** khách đặt đơn đầu tiên không theo thứ tự mã (ví dụ `KH09` đặt trước `KH02`).

**Hướng 4 — Dữ liệu lớn:** 50.000 đơn của 25.000 khách. Đo thời gian chạy (có thể mất vài chục giây). Lời giải thích "O(n), bộ nhớ phụ O(1)" có đúng không? Phương thức `count()` của list phải làm gì mỗi lần được gọi?

### 4. Yêu cầu

Với vai trò người duyệt mã, bạn phải thực hiện đầy đủ bốn phần sau:

**(1) Tìm dữ liệu làm lộ lỗi**

- Theo các hướng ở mục 3, tự nghĩ ra **ít nhất 6 bộ dữ liệu thử**. Với mỗi bộ: dự đoán kết quả đúng trước, rồi sửa đoạn chạy thử ở cuối `than_thiet.py` để chạy hàm của AI và in kết quả.
- Ghi vào bảng trong `PHAN_TICH.md`: dữ liệu, kết quả đúng, kết quả thực tế, đúng hay sai. Các bộ dữ liệu phải làm lộ **ít nhất 3 lỗi khác nhau**.

**(2) Phân tích (viết vào `PHAN_TICH.md`)**

- Với mỗi lỗi: dòng lệnh gây lỗi, nguyên nhân, và bảng chạy tay trên bộ dữ liệu nhỏ nhất làm lộ lỗi đó.
- Đếm số lần so sánh mà `count()` và `in result` thực hiện với n đơn của n khách khác nhau; kết luận Big-O thời gian và bộ nhớ phụ thật của hàm. Ghi thời gian đo với 50.000 đơn.
- Điền bảng **"Nhật ký giữ – sửa – loại bỏ"**: phần nào trong mã của AI bạn giữ, phần nào sửa, phần nào bỏ, kèm lý do.
- Đề xuất **giải pháp thứ hai** nhanh hơn cho gian hàng lớn. So sánh hai giải pháp theo 5 tiêu chí: thời gian (Big-O), bộ nhớ phụ (Big-O), thời gian đo với 50.000 đơn, độ dễ đọc, mức phù hợp với gian hàng 100 đơn và 50.000 đơn. Nêu rõ bạn chọn giải pháp nào cho báo cáo quý.

**(3) Sửa mã và cài giải pháp thứ hai (trong `than_thiet.py`)**

- Sửa `loyal_customers` (giữ cách đếm bằng `count()`) để hết mọi lỗi bạn tìm được.
- Viết `loyal_customers_fast` theo giải pháp thứ hai: cùng kết quả, chạy 50.000 đơn trong vài giây. Không dùng `set`, `dict` hay `collections` (sẽ học ở buổi bảng băm).
- Cả hai hàm không được sửa list đầu vào.

**(4) Kiểm chứng sau khi sửa**

- Chạy lại toàn bộ các bộ dữ liệu thử ở phần (1) trên cả hai hàm, ghi vào cột "Sau khi sửa". Mọi dòng phải đúng.
- `python kiem_tra.py` vẫn đạt cả 3 mục của AI.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session01_Ex15`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-01-tong-quan-do-phuc-tap/bai-15 rồi chép các tệp vào kho: `than_thiet.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền `PHAN_TICH.md`, sửa và viết mã trong `than_thiet.py`.
4. Mức AI của bài: AI-2 cho phần phản biện (đề đã cung cấp mã do AI sinh; bạn được hỏi AI để hiểu đoạn mã, nhưng dữ liệu thử, phân tích và mã sửa phải do bạn tự làm và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
