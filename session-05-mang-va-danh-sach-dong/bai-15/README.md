# Phản biện mã do AI viết: mảng động lưu đơn giao ghép GrabFood

### 1. Bối cảnh & Vấn đề

![Trợ lý AI viết thêm ba phương thức cho mảng động trong vài giây, ba test của AI đều xanh. Có nên dùng ngay?](minh_hoa.png)

*Trợ lý AI viết thêm ba phương thức cho mảng động trong vài giây, ba test của AI đều xanh. Có nên dùng ngay?*

Tài xế **giao ghép** GrabFood nhận nhiều đơn trong một chuyến. Ứng dụng tài xế chạy bản Python rút gọn nên danh sách đơn được lưu bằng lớp `OrderArray`, một mảng động tự cài theo Lesson 04. Các phương thức `append`, `pop(index)`, `_resize`, `items` đã có, đã được kiểm tra kỹ và đúng.

Nhóm cần thêm ba phương thức:

- `extend(values)`: nhận cả lô đơn từ nhà hàng, thêm vào cuối (một lô có thể tới vài chục đơn).
- `index_of(value)`: vị trí đơn đầu tiên có mã đó; **không có thì báo `ValueError`** (giống `list.index`).
- `remove_all(value)`: khách hủy thì xóa **mọi** đơn có mã đó (do lỗi đồng bộ, một mã có thể bị ghi nhiều lần, kể cả liền nhau); trả về số đơn đã xóa.

Một đồng nghiệp nhờ trợ lý AI viết ba phương thức. AI trả về mã kèm ba test, cả ba đều xanh, và đồng nghiệp đề nghị đưa vào bản cập nhật tuần này. Bạn là người **duyệt mã**. Quy định của nhóm: mã do AI sinh chỉ được dùng khi người duyệt đã tự chạy thử với dữ liệu của mình và chịu trách nhiệm về nó.

### 2. Mã do AI sinh

Phần AI viết thêm vào cuối lớp `OrderArray` trong `don_ghep.py`:

```python
    def extend(self, values):
        # Thêm mọi phần tử của values vào cuối.
        if self._size + len(values) > self._capacity:
            self._resize(2 * self._capacity)
        for value in values:
            self._data[self._size] = value
            self._size += 1

    def index_of(self, value):
        # Chỉ số của lần xuất hiện đầu tiên; không có thì báo ValueError.
        for j in range(self._size):
            if self._data[j] == value:
                return j
        return -1

    def remove_all(self, value):
        # Xóa mọi lần xuất hiện của value, trả về số phần tử đã xóa.
        removed = 0
        j = 0
        while j < self._size:
            if self._data[j] == value:
                self.pop(j)
                removed += 1
            j += 1
        return removed
```

Lời giải thích AI gửi kèm: "`extend` mở rộng khi cần rồi ghi lần lượt. `remove_all` duyệt một lượt nên O(n). Đã có test cho cả ba phương thức."

Ba test trong `test_don_ghep.py`: thêm lô 2 đơn vào mảng rỗng, tìm vị trí một mã có trong mảng, xóa một mã xuất hiện hai lần không liền nhau. Chạy đoạn cuối tệp:

```plaintext
Đơn đang giao: ['GF01', 'GF02', 'GF03']
Vị trí GF02: 1
Xóa GF02: 2 | còn: ['GF01', 'GF03']
```

Kết quả trông đúng. Nhiệm vụ của bạn là tìm ra những dữ liệu mà đoạn mã này **không** xử lý đúng.

### 3. Các hướng cần kiểm chứng

Đề không cho biết tình huống nào làm lộ lỗi; bạn phải tự chạy tay hoặc chạy thử để biết.

**Hướng 1 — Lô đơn lớn:** thêm lô 10 đơn vào mảng đang có 1 đơn.

**Hướng 2 — Mã không có:** tìm vị trí một mã không có trong mảng. Theo đặc tả phải xảy ra điều gì?

**Hướng 3 — Mã trùng liền nhau:** xóa mã xuất hiện nhiều lần **liền nhau**, kể cả ở cuối mảng.

**Hướng 4 — Dữ liệu lớn:** mảng 40.000 đơn, một nửa là mã cần xóa. Đo thời gian `remove_all`. Lời giải thích "duyệt một lượt nên O(n)" có đúng không? Mỗi lần gọi `pop(j)` phải làm gì?

### 4. Yêu cầu

Với vai trò người duyệt mã, bạn phải thực hiện đầy đủ bốn phần sau:

**(1) Tìm dữ liệu làm lộ lỗi**

- Theo các hướng ở mục 3, tự nghĩ ra **ít nhất 6 bộ dữ liệu thử**. Với mỗi bộ: dự đoán kết quả đúng trước, rồi chạy mã của AI và ghi kết quả.
- Ghi vào bảng trong `PHAN_TICH.md`. Các bộ dữ liệu phải làm lộ **ít nhất 3 lỗi khác nhau**.

**(2) Phân tích (viết vào `PHAN_TICH.md`)**

- Với mỗi lỗi: dòng lệnh gây lỗi, nguyên nhân, và bảng chạy tay (`_size`, `_capacity`, `_data`, chỉ số j) trên bộ dữ liệu nhỏ nhất làm lộ lỗi đó.
- Đếm số tham chiếu phải dịch của `remove_all` khi xóa m đơn trong mảng n đơn; kết luận Big-O thật. Ghi thời gian đo với 40.000 đơn.
- Điền bảng **"Nhật ký giữ – sửa – loại bỏ"**: phần nào trong mã của AI bạn giữ, phần nào sửa, phần nào bỏ, kèm lý do.
- Đề xuất **giải pháp thứ hai** cho việc xóa mọi đơn trùng mã, chỉ duyệt mảng một lượt. So sánh hai giải pháp theo 5 tiêu chí: thời gian (Big-O), bộ nhớ phụ (Big-O), thời gian đo, độ dễ đọc, mức phù hợp với chuyến 5 đơn và với bộ dữ liệu 200.000 đơn của máy chủ. Nêu rõ bạn chọn giải pháp nào.

**(3) Sửa mã và cài giải pháp thứ hai (trong `don_ghep.py`)**

- Sửa ba phương thức của AI để hết mọi lỗi bạn tìm được; `remove_all` vẫn dùng `pop`.
- Viết thêm `remove_all_fast(value)`: cùng kết quả với `remove_all`, một lượt duyệt, không gọi `pop`; ô thừa ở đuôi đặt về `None`.

**(4) Kiểm chứng sau khi sửa**

- Chạy lại toàn bộ bộ dữ liệu thử ở phần (1), ghi vào cột "Sau khi sửa". Mọi dòng phải đúng.
- `pytest -q` vẫn xanh cả 3 test của AI.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex15`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-15 rồi chép các tệp vào kho: `don_ghep.py`, `test_don_ghep.py`, `PHAN_TICH.md`.
3. Điền `PHAN_TICH.md`, sửa và viết mã trong `don_ghep.py`.
4. Mức AI của bài: AI-2 cho phần phản biện (đề đã cung cấp mã do AI sinh; bạn được hỏi AI để hiểu đoạn mã, nhưng dữ liệu thử, phân tích và mã sửa phải do bạn tự làm và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
