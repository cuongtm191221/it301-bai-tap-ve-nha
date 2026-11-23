# Phản biện mã do AI viết: hàng đợi phiếu trả hàng Tiki bằng hai ngăn xếp

### 1. Bối cảnh & Vấn đề

![Trợ lý AI cài hàng đợi bằng hai ngăn xếp trong vài giây, ba test của AI đều xanh. Có nên dùng ngay?](minh_hoa.png)

*Trợ lý AI cài hàng đợi bằng hai ngăn xếp trong vài giây, ba test của AI đều xanh. Có nên dùng ngay?*

Khách trả hàng trên Tiki tạo **phiếu trả hàng**; kho xử lý phiếu theo thứ tự tạo (vào trước, ra trước). Hệ thống cũ của kho chỉ có cấu trúc **ngăn xếp** (list với `append`, `pop`), nên một đồng nghiệp nhờ trợ lý AI cài **hàng đợi bằng hai ngăn xếp**: một ngăn nhận phiếu mới, một ngăn để lấy phiếu ra. Ý tưởng: đổ ngăn nhận sang ngăn lấy thì thứ tự bị đảo một lần, phiếu cũ nhất nằm trên cùng.

Đặc tả của `TwoStackQueue` (giống hàng đợi ở Lesson 03):

- `enqueue(ticket)`: thêm phiếu vào cuối hàng.
- `dequeue()`: lấy phiếu **đầu hàng**; `peek()`: xem phiếu đầu hàng; rỗng thì cả hai báo `IndexError("hàng đợi rỗng")`.
- `size()`: số phiếu đang chờ.

Phiếu được thêm và xử lý **xen kẽ** suốt ngày. AI trả về mã kèm ba test, cả ba đều xanh, và đồng nghiệp đề nghị đưa vào bản cập nhật tuần này. Bạn là người **duyệt mã**. Quy định của nhóm: mã do AI sinh chỉ được dùng khi người duyệt đã tự chạy thử với dữ liệu của mình và chịu trách nhiệm về nó.

### 2. Mã do AI sinh

Tệp `tra_hang.py` trong thư mục khởi đầu:

```python
class TwoStackQueue:
    # Hàng đợi phiếu trả hàng của Tiki, AI đề xuất cài bằng hai ngăn xếp (list):
    # _in nhận phiếu mới, _out để lấy phiếu ra.
    def __init__(self):
        self._in = []
        self._out = []

    def enqueue(self, ticket):
        self._in.append(ticket)

    def dequeue(self):
        # Đổ hết _in sang _out (đảo thứ tự) rồi lấy phiếu trên cùng của _out.
        while self._in:
            self._out.append(self._in.pop())
        if not self._out:
            raise IndexError("hàng đợi rỗng")
        return self._out.pop()

    def peek(self):
        if not self._out:
            raise IndexError("hàng đợi rỗng")
        return self._out[-1]

    def size(self):
        return len(self._in)
```

Lời giải thích AI gửi kèm: "Mỗi lần lấy phiếu, đổ ngăn nhận sang ngăn lấy để phiếu cũ nhất lên trên. Thứ tự luôn đúng, mỗi phiếu chỉ được chép một lần nên chi phí khấu hao O(1)."

Ba test trong `test_tra_hang.py`: thêm ba phiếu rồi lấy ba phiếu; thêm ba, lấy một rồi xem đầu hàng; thêm hai rồi đếm. Chạy đoạn cuối tệp:

```plaintext
Xử lý: TH01 TH02
Đầu hàng: TH03
Xử lý: TH03
```

Kết quả trông đúng. Nhiệm vụ của bạn là tìm ra những dữ liệu mà đoạn mã này **không** xử lý đúng.

### 3. Các hướng cần kiểm chứng

Đề không cho biết tình huống nào làm lộ lỗi; bạn phải tự chạy tay hoặc chạy thử để biết.

**Hướng 1 — Thêm và lấy xen kẽ:** thêm hai phiếu, lấy một, thêm hai phiếu nữa, rồi lấy hết. Thứ tự có đúng không?

**Hướng 2 — Xem đầu hàng khi chưa lấy lần nào.**

**Hướng 3 — Đếm sau khi đã lấy:** thêm ba phiếu, lấy một, rồi đếm.

**Hướng 4 — So với một hàng đợi chuẩn:** chạy 2.000 thao tác ngẫu nhiên trên cả mã AI và một list dùng `append` / `pop(0)` làm đối chứng; ghi thao tác đầu tiên hai bên khác nhau.

### 4. Yêu cầu

Với vai trò người duyệt mã, bạn phải thực hiện đầy đủ bốn phần sau:

**(1) Tìm dữ liệu làm lộ lỗi**

- Theo các hướng ở mục 3, tự nghĩ ra **ít nhất 6 bộ dữ liệu thử** (chuỗi thao tác). Với mỗi bộ: dự đoán kết quả đúng trước, rồi chạy mã của AI và ghi kết quả.
- Ghi vào bảng trong `PHAN_TICH.md`. Các bộ dữ liệu phải làm lộ **cả 3 lỗi** của mã AI.

**(2) Phân tích (viết vào `PHAN_TICH.md`)**

- Với mỗi lỗi: dòng lệnh gây lỗi, nguyên nhân, và bảng chạy tay (`_in`, `_out` sau mỗi thao tác) trên chuỗi thao tác ngắn nhất làm lộ lỗi.
- Lời giải thích "mỗi phiếu chỉ được chép một lần" đúng với điều kiện nào? Sau khi sửa, giải thích vì sao chi phí khấu hao là O(1) và trường hợp xấu nhất của một lần `dequeue` là bao nhiêu.
- Điền bảng **"Nhật ký giữ – sửa – loại bỏ"**: phần nào trong mã của AI bạn giữ, phần nào sửa, phần nào bỏ, kèm lý do.
- Đề xuất **giải pháp thứ hai** không dùng hai ngăn xếp (ví dụ một cấu trúc đã học ở Lesson 03, 04). So sánh hai giải pháp theo 5 tiêu chí: thời gian (Big-O, xấu nhất và khấu hao), bộ nhớ phụ, thời gian đo, độ dễ đọc, mức phù hợp với hệ thống kho. Nêu rõ bạn chọn giải pháp nào.

**(3) Sửa mã và cài giải pháp thứ hai (trong `tra_hang.py`)**

- Sửa `TwoStackQueue` (vẫn dùng hai ngăn xếp) để hết mọi lỗi bạn tìm được.
- Viết thêm lớp `DequeQueue` theo giải pháp thứ hai, cùng năm thao tác và cùng thông báo lỗi.

**(4) Kiểm chứng sau khi sửa**

- Chạy lại toàn bộ bộ dữ liệu thử ở phần (1) trên cả hai lớp, ghi vào cột "Sau khi sửa". Mọi dòng phải đúng.
- `pytest -q` vẫn xanh cả 3 test của AI.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex15`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-15 rồi chép các tệp vào kho: `tra_hang.py`, `test_tra_hang.py`, `PHAN_TICH.md`.
3. Điền `PHAN_TICH.md`, sửa và viết mã trong `tra_hang.py`.
4. Mức AI của bài: AI-2 cho phần phản biện (đề đã cung cấp mã do AI sinh; bạn được hỏi AI để hiểu đoạn mã, nhưng dữ liệu thử, phân tích và mã sửa phải do bạn tự làm và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
