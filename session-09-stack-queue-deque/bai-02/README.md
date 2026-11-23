# Lỗi kiểm tra dấu ngoặc trong mẫu tin nhắn của Tiki

### 1. Bối cảnh nghiệp vụ

![Mẫu tin nhắn sai ngoặc lọt qua kiểm tra và gửi tới hàng nghìn khách, còn có mẫu làm công cụ kiểm tra bị sập.](minh_hoa.png)

*Mẫu tin nhắn sai ngoặc lọt qua kiểm tra và gửi tới hàng nghìn khách, còn có mẫu làm công cụ kiểm tra bị sập.*

Bạn là kỹ sư phần mềm trong nhóm chăm sóc khách hàng của Tiki.

Tin nhắn gửi khách được sinh từ **mẫu** có chỗ điền thông tin trong ngoặc nhọn và ngoặc vuông, ví dụ:

```plaintext
Chào {ten}, đơn [{ma_don}] đã giao (dự kiến {ngay}).
```

Mẫu do nhân viên nhập tay. Nếu dấu ngoặc sai (thiếu, thừa, lệch cặp), hệ thống điền thông tin không thay được chỗ điền, và khách nhận tin nhắn còn nguyên `{ma_giam]`. Trước khi lưu mẫu, công cụ chạy `is_balanced(template)` để chặn mẫu sai:

- Mỗi dấu mở `(`, `[`, `{` phải có đúng dấu đóng cùng loại; dấu nào mở sau phải đóng trước.
- `matches(open_ch, close_ch)` cho biết hai dấu có phải một cặp không.
- Chuỗi không có ngoặc nào là hợp lệ.

Mỗi tuần nhóm nhập hàng trăm mẫu cho các chương trình khuyến mãi, và mỗi mẫu được gửi tới hàng nghìn khách.

Công cụ kiểm tra chạy cho cả lô mẫu một lần; chỉ một mẫu làm công cụ dừng giữa chừng là mọi mẫu phía sau không được kiểm và có thể bị gửi đi mà chưa ai xem.

Kịch bản kiểm tra (đoạn cuối tệp): năm mẫu gồm mẫu đúng, mẫu lệch cặp, mẫu thiếu dấu đóng, mẫu thừa dấu đóng, mẫu không có ngoặc.

Kết quả đúng cần hiển thị:

```plaintext
Hợp lệ | Chào {ten}, đơn [{ma_don}] đã giao (dự kiến {ngay}).
Sai ngoặc | Mã {ma_giam] giảm 10%
Sai ngoặc | Đơn (dự kiến {ngay}
Sai ngoặc | Hoàn tiền) cho đơn {ma_don}
Hợp lệ | Không có ngoặc
```

### 2. Vấn đề hiện tại

Nhóm nội dung phản ánh:

- Mẫu `Mã {ma_giam] giảm 10%` (mở ngoặc nhọn, đóng ngoặc vuông) **lọt qua** kiểm tra.
- Mẫu thiếu dấu đóng ở cuối cũng được báo hợp lệ.
- Mẫu có dấu đóng thừa làm công cụ kiểm tra **báo lỗi và dừng**, các mẫu sau không được kiểm.

Nhắc lại kiến thức (Lesson 02):

- Kiểm tra dấu ngoặc bằng ngăn xếp: gặp dấu mở thì `push`; gặp dấu đóng thì `pop` dấu mở gần nhất và so cặp.
- Ba kiểu sai: **lệch cặp** (dấu đóng không khớp dấu mở vừa lấy ra), **đóng thừa** (gặp dấu đóng khi ngăn xếp rỗng), **mở thừa** (hết chuỗi mà ngăn xếp còn phần tử).
- "Quên kiểm tra ngăn xếp lúc hết chuỗi" là lỗi thường gặp: chuỗi chỉ có dấu mở vẫn bị coi là đúng.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `mau_tin.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
"""Kiểm tra dấu ngoặc trong mẫu tin nhắn gửi khách hàng Tiki."""
def matches(open_ch, close_ch):
    # True nếu dấu mở open_ch và dấu đóng close_ch là một cặp: (), [] hoặc {}.
    return open_ch in "([{" and close_ch in ")]}"


def is_balanced(template):
    # True nếu mọi dấu ngoặc trong mẫu tin nhắn mở, đóng đúng cặp và đúng thứ tự lồng nhau.
    stack = []
    for ch in template:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            top = stack.pop()
            if not matches(top, ch):
                return False
    return True


templates = [
    "Chào {ten}, đơn [{ma_don}] đã giao (dự kiến {ngay}).",
    "Mã {ma_giam] giảm 10%",
    "Đơn (dự kiến {ngay}",
    "Hoàn tiền) cho đơn {ma_don}",
    "Không có ngoặc",
]
for t in templates:
    print("Hợp lệ" if is_balanced(t) else "Sai ngoặc", "|", t)
```

Kết quả hiển thị trên Console:

```plaintext
Hợp lệ | Chào {ten}, đơn [{ma_don}] đã giao (dự kiến {ngay}).
Hợp lệ | Mã {ma_giam] giảm 10%
Hợp lệ | Đơn (dự kiến {ngay}
Traceback (most recent call last):
  ...
    top = stack.pop()
IndexError: pop from empty list
```

Đối chiếu với kết quả đúng: mẫu thứ hai và thứ ba bị báo "Hợp lệ"; mẫu thứ tư gây `IndexError`, nên mẫu cuối không được kiểm.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- `matches("{", "]")` của mã hiện tại trả gì? Viết lại `matches` để chỉ ba cặp đúng trả `True`.
- Chạy tay `is_balanced("Đơn (dự kiến {ngay}")` của mã hiện tại: ghi ngăn xếp sau mỗi dấu ngoặc. Hết chuỗi ngăn xếp còn gì, hàm trả gì?
- Chạy tay `is_balanced("Hoàn tiền) cho đơn {ma_don}")`: dòng nào gây lỗi, vì sao? Sửa thế nào?
- Ghép ba kiểu sai (lệch cặp, đóng thừa, mở thừa) với ba dòng trong hàm sửa xong.
- Với mẫu dài n ký tự, hàm làm nhiều nhất bao nhiêu lần `push`, `pop`? Big-O thời gian và bộ nhớ phụ?
- Ghi năm bộ dữ liệu thử: chuỗi rỗng, `([)]`, `)(`, ngoặc lồng sâu ba tầng, chuỗi chỉ có dấu mở; kèm kết quả mong đợi.
- Một đồng nghiệp đề xuất chỉ đếm số dấu mở và số dấu đóng, bằng nhau là hợp lệ. Tìm một mẫu làm cách này sai.

**(2) Sửa lỗi**

- Sửa hai hàm trong `mau_tin.py`. Không đổi tên hàm, tham số.
- Chạy `python mau_tin.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `pytest -q` phải xanh cả 4 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session09_Ex02`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-09-stack-queue-deque/bai-02 rồi chép các tệp vào kho: `mau_tin.py`, `test_mau_tin.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `mau_tin.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
