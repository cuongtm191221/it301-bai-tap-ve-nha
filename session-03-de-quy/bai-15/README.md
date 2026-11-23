# Phản biện mã do AI viết: thống kê chi tiêu theo nhóm lồng nhau trên MoMo

### 1. Bối cảnh & Vấn đề

![Trợ lý AI viết xong ba hàm đệ quy thống kê chi tiêu trong vài giây, bốn mục kiểm tra đều đạt. Có nên dùng ngay?](minh_hoa.png)

*Trợ lý AI viết xong ba hàm đệ quy thống kê chi tiêu trong vài giây, bốn mục kiểm tra đều đạt. Có nên dùng ngay?*

Màn hình **"Quản lý chi tiêu"** của ví MoMo cho người dùng tự xếp giao dịch vào **nhóm**, và nhóm có thể chứa **nhóm con** (ví dụ nhóm "Ăn uống" có nhóm con "Cà phê"). Dữ liệu một tháng là một list; mỗi phần tử là **một số tiền** (số nguyên, đồng) hoặc **một nhóm con** (list có cùng dạng):

```plaintext
[120000, [45000, -45000], [[250000], -50000]]
```

Số âm là **hoàn tiền** (đơn bị hủy, khuyến mãi trả lại) và phải được **trừ** vào tổng. Nhóm chỉ để sắp xếp, **không phải** giao dịch. Màn hình cần ba con số: tổng chi tiêu, số giao dịch, và số cấp sâu nhất (để thụt lề khi hiển thị; list không có nhóm con là 1 cấp).

Một đồng nghiệp đã nhờ trợ lý AI viết ba hàm đệ quy. AI trả về mã kèm tệp `kiem_tra.py` có bốn mục kiểm tra, cả bốn đều đạt, và đồng nghiệp đề nghị đưa vào bản cập nhật tuần này. Bạn là người **duyệt mã**. Quy định của nhóm: mã do AI sinh chỉ được dùng khi người duyệt đã tự chạy thử với dữ liệu của mình và chịu trách nhiệm về nó.

### 2. Mã do AI sinh

Tệp `chi_tieu_nhom.py` trong thư mục khởi đầu có ba hàm do AI viết:

```python
def total_spending(items):
    # Tổng tiền của mọi giao dịch trong items, kể cả giao dịch nằm trong các nhóm con.
    # Mỗi phần tử là một số tiền (số nguyên) hoặc một nhóm con (list).
    total = 0
    for item in items:
        if type(item) == list:
            total += total_spending(item)
        elif item > 0:
            total += item
    return total


def count_transactions(items):
    # Số giao dịch (số tiền) trong items, kể cả trong các nhóm con.
    count = 0
    for item in items:
        if type(item) == list:
            count += 1 + count_transactions(item)
        else:
            count += 1
    return count


def deepest_level(items):
    # Số cấp sâu nhất: list không có nhóm con là 1 cấp.
    deepest = 1
    for item in items:
        if type(item) == list:
            deepest = deepest_level(item) + 1
    return deepest
```

Lời giải thích AI gửi kèm: "Ba hàm đều đệ quy: gặp nhóm con thì gọi lại chính hàm đó. Đệ quy xử lý được mọi độ sâu lồng nhau. Đã kiểm tra với bốn trường hợp."

Bốn mục trong `kiem_tra.py`: tổng có một nhóm con, đếm giao dịch trên list không có nhóm, số cấp với nhóm lồng ở cuối list, tháng chưa có giao dịch. Chạy đoạn cuối tệp:

```plaintext
Tổng chi tiêu: 210000
Số giao dịch: 3
Số cấp sâu nhất: 3
Tháng chưa có giao dịch: 0
```

Kết quả trông đúng. Nhiệm vụ của bạn là tìm ra những dữ liệu mà đoạn mã này **không** xử lý đúng.

### 3. Các hướng cần kiểm chứng

Bốn mục kiểm tra của AI đều dùng dữ liệu "đẹp". Đề không cho biết tình huống nào làm lộ lỗi; bạn phải tự chạy tay hoặc chạy thử để biết.

**Hướng 1 — Hoàn tiền:** tháng có giao dịch số âm, ở cấp ngoài cùng và trong nhóm con.

**Hướng 2 — Nhóm và giao dịch:** đếm giao dịch khi có nhóm con, nhóm rỗng, nhóm lồng trong nhóm.

**Hướng 3 — Vị trí của nhóm sâu nhất:** nhóm lồng sâu nhất đứng đầu list, theo sau là nhóm nông hơn.

**Hướng 4 — Dữ liệu lồng rất sâu:** dữ liệu nhập từ ứng dụng cũ bị lỗi, lồng 5.000 cấp. Lời giải thích "xử lý được mọi độ sâu" có đúng không (Lesson 03)?

### 4. Yêu cầu

Với vai trò người duyệt mã, bạn phải thực hiện đầy đủ bốn phần sau:

**(1) Tìm dữ liệu làm lộ lỗi**

- Theo các hướng ở mục 3, tự nghĩ ra **ít nhất 6 bộ dữ liệu thử**. Với mỗi bộ: dự đoán kết quả đúng trước, rồi sửa đoạn chạy thử ở cuối `chi_tieu_nhom.py` để chạy hàm của AI và in kết quả.
- Ghi vào bảng trong `PHAN_TICH.md`. Các bộ dữ liệu phải làm lộ **ít nhất 3 lỗi khác nhau**.

**(2) Phân tích (viết vào `PHAN_TICH.md`)**

- Với mỗi lỗi: dòng lệnh gây lỗi, nguyên nhân, và bảng chạy tay trên bộ dữ liệu nhỏ nhất làm lộ lỗi đó. Trả lời ba câu hỏi kiểm tra (Lesson 01) cho hàm chứa lỗi.
- Với dữ liệu lồng d cấp, call stack sâu bao nhiêu tầng? Từ khoảng bao nhiêu cấp thì hàm báo `RecursionError`?
- Điền bảng **"Nhật ký giữ – sửa – loại bỏ"**: phần nào trong mã của AI bạn giữ, phần nào sửa, phần nào bỏ, kèm lý do.
- Đề xuất **giải pháp thứ hai** cho phép tính tổng, **không dùng đệ quy**, chạy được dữ liệu 5.000 cấp. So sánh hai giải pháp theo 5 tiêu chí: thời gian (Big-O), bộ nhớ phụ (Big-O), độ sâu dữ liệu chịu được, độ dễ đọc, mức phù hợp với dữ liệu thường (2–3 cấp) và dữ liệu lỗi (5.000 cấp). Nêu rõ bạn chọn giải pháp nào cho màn hình.

**(3) Sửa mã và cài giải pháp thứ hai (trong `chi_tieu_nhom.py`)**

- Sửa ba hàm của AI (giữ cách viết đệ quy) để hết mọi lỗi bạn tìm được.
- Viết thêm hàm `total_spending_loop(items)`: cùng kết quả với `total_spending`, không gọi đệ quy, chạy được dữ liệu lồng 5.000 cấp.
- Các hàm không được sửa list đầu vào.

**(4) Kiểm chứng sau khi sửa**

- Chạy lại toàn bộ các bộ dữ liệu thử ở phần (1) trên các hàm đã sửa, ghi vào cột "Sau khi sửa". Mọi dòng phải đúng.
- `python kiem_tra.py` vẫn đạt cả 4 mục của AI.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex15`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-15 rồi chép các tệp vào kho: `chi_tieu_nhom.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền `PHAN_TICH.md`, sửa và viết mã trong `chi_tieu_nhom.py`.
4. Mức AI của bài: AI-2 cho phần phản biện (đề đã cung cấp mã do AI sinh; bạn được hỏi AI để hiểu đoạn mã, nhưng dữ liệu thử, phân tích và mã sửa phải do bạn tự làm và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
