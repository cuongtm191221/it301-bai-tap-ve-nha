# Lỗi hoàn tác, làm lại trong trình soạn mô tả sản phẩm Tiki

### 1. Bối cảnh nghiệp vụ

![Người bán bấm hoàn tác khi chưa viết gì thì trình soạn sập; viết mới xong bấm làm lại thì chữ cũ hiện lại.](minh_hoa.png)

*Người bán bấm hoàn tác khi chưa viết gì thì trình soạn sập; viết mới xong bấm làm lại thì chữ cũ hiện lại.*

Bạn là kỹ sư phần mềm trong nhóm công cụ người bán của Tiki.

Người bán soạn **mô tả sản phẩm** theo từng cụm từ. Trình soạn có nút **Hoàn tác** (gỡ cụm vừa viết) và **Làm lại** (viết lại cụm vừa gỡ). Lớp `DescriptionEditor` dùng hai ngăn xếp theo Lesson 02:

- `write(part)`: thêm cụm từ vào cuối mô tả.
- `undo()`: gỡ cụm từ vừa viết gần nhất.
- `redo()`: viết lại cụm từ vừa gỡ gần nhất.
- `text()`: mô tả hiện tại, các cụm nối bằng dấu cách.
- Không còn gì để hoàn tác hoặc làm lại thì giữ nguyên, **không báo lỗi** (người bán hay bấm liên tục).

Mô tả sản phẩm được duyệt trước khi đăng; nếu hoàn tác, làm lại sai, người bán đăng nhầm nội dung đã xóa (ví dụ thông số cũ) và bị khiếu nại vì mô tả sai sự thật.

Người bán thường soạn nhanh rồi bấm Hoàn tác, Làm lại liên tục để so hai cách viết, nên trình soạn phải chịu được mọi thứ tự bấm, kể cả bấm khi không còn gì để làm.

Kịch bản kiểm tra (đoạn cuối tệp): viết ba cụm; hoàn tác; làm lại rồi hoàn tác; viết cụm mới rồi bấm làm lại; bấm hoàn tác 5 lần liên tiếp.

Kết quả đúng cần hiển thị:

```plaintext
Hoàn tác: Tai nghe không dây
Làm lại rồi hoàn tác: Tai nghe không dây
Viết mới rồi làm lại: Tai nghe không dây pin 30 giờ
Hoàn tác 5 lần: ''
```

### 2. Vấn đề hiện tại

Người bán phản ánh:

- Bấm Làm lại rồi Hoàn tác thì cụm từ không bị gỡ.
- Hoàn tác một cụm, viết cụm mới, rồi bấm Làm lại thì **cụm đã xóa hiện lại** sau cụm mới.
- Bấm Hoàn tác nhiều lần (khi đã gỡ hết) thì trình soạn báo lỗi và mất nội dung đang soạn.

Nhắc lại kiến thức (Lesson 02):

- Viết cụm mới: push vào `undo_stack`, **xóa sạch** `redo_stack`.
- Hoàn tác: pop từ `undo_stack`, push sang `redo_stack`.
- Làm lại: pop từ `redo_stack`, push **về** `undo_stack`.
- "Không xóa ngăn xếp làm lại khi có thao tác mới" là lỗi thường gặp: thao tác cũ đã bỏ lại quay về sau thao tác mới.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `soan_mo_ta.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Trình soạn mô tả sản phẩm có hoàn tác và làm lại cho người bán Tiki."""
class DescriptionEditor:
    # Trình soạn mô tả sản phẩm cho người bán trên Tiki: viết từng cụm từ, hoàn tác, làm lại.
    # undo() và redo() khi không có gì để làm thì giữ nguyên, không báo lỗi.
    def __init__(self):
        self.parts = []
        self.undo_stack = []
        self.redo_stack = []

    def write(self, part):
        self.parts.append(part)
        self.undo_stack.append(part)

    def undo(self):
        part = self.undo_stack.pop()
        self.parts.pop()
        self.redo_stack.append(part)

    def redo(self):
        if self.redo_stack:
            part = self.redo_stack.pop()
            self.parts.append(part)

    def text(self):
        return " ".join(self.parts)


ed = DescriptionEditor()
for part in ("Tai nghe", "không dây", "chống ồn"):
    ed.write(part)
ed.undo()
print("Hoàn tác:", ed.text())
ed.redo()
ed.undo()
print("Làm lại rồi hoàn tác:", ed.text())
ed.write("pin 30 giờ")
ed.redo()
print("Viết mới rồi làm lại:", ed.text())
for _ in range(5):
    ed.undo()
print("Hoàn tác 5 lần:", repr(ed.text()))
```

Kết quả hiển thị trên Console:

```plaintext
Hoàn tác: Tai nghe không dây
Làm lại rồi hoàn tác: Tai nghe không dây
Viết mới rồi làm lại: Tai nghe không dây pin 30 giờ không dây
Traceback (most recent call last):
  ...
    part = self.undo_stack.pop()
IndexError: pop from empty list
```

Dòng đầu đúng. Lần "làm lại rồi hoàn tác" gây `IndexError` vì `undo_stack` đã rỗng, nên các dòng sau không được in.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Chạy tay kịch bản với mã hiện tại: ghi `parts`, `undo_stack`, `redo_stack` sau mỗi thao tác cho tới dòng gây lỗi. Vì sao `undo_stack` rỗng dù mô tả còn hai cụm?
- Sửa `redo` theo quy tắc. Kiểm tra lại bằng chuỗi thao tác "viết A, B; hoàn tác; làm lại; hoàn tác".
- Với mã hiện tại (sau khi sửa `redo`), chạy tay "viết A, B; hoàn tác; viết X; làm lại". Kết quả sai thế nào? Sửa `write`.
- Sửa `undo` để không báo lỗi khi không còn gì để hoàn tác. Vì sao không nên dùng `try/except` bao quanh toàn bộ hàm?
- Ghi Big-O của `write`, `undo`, `redo`, `text` theo n (số cụm).
- Ghi bốn bộ dữ liệu thử, kèm kết quả mong đợi: hoàn tác khi chưa viết; làm lại khi chưa hoàn tác; hoàn tác hết rồi làm lại hết; viết mới xen giữa.
- Vì sao hai ngăn xếp phù hợp với hoàn tác, làm lại hơn là một hàng đợi? Gợi ý: thao tác nào được gỡ trước?

**(2) Sửa lỗi**

- Sửa lớp `DescriptionEditor` trong `soan_mo_ta.py`. Không đổi tên lớp, phương thức, thuộc tính.
- Chạy `python soan_mo_ta.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex03`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-03 rồi chép các tệp vào kho: `soan_mo_ta.py`, `test_soan_mo_ta.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `soan_mo_ta.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
