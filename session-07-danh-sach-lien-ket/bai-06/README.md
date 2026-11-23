# Lỗi tính năng "Phát ngay" trên Zing MP3

### 1. Bối cảnh nghiệp vụ

![Người nghe bấm Phát ngay, danh sách phát xuất hiện bài trùng và một bài lạ không hề có.](minh_hoa.png)

*Người nghe bấm Phát ngay, danh sách phát xuất hiện bài trùng và một bài lạ không hề có.*

Bạn là kỹ sư phần mềm trong nhóm xây dựng tính năng danh sách phát của ứng dụng nghe nhạc Zing MP3.

Trong danh sách phát, mỗi bài có nút **"Phát ngay"**. Khi người nghe bấm nút này, bài đó được **chuyển lên đầu** danh sách để phát trước, các bài còn lại giữ nguyên thứ tự. Danh sách phát lưu bằng **danh sách liên kết đơn** có `head`, `tail`, `size`; mỗi node giữ mã một bài.

Ví dụ, danh sách đang là:

```plaintext
ZM001  ->  ZM002  ->  ZM003  ->  ZM004  ->  None        size = 4
```

Bấm "Phát ngay" ở bài `ZM003` thì danh sách phải thành:

```plaintext
ZM003  ->  ZM001  ->  ZM002  ->  ZM004  ->  None        size = 4
```

Hàm `play_now(playlist, code)` thực hiện việc này và phải đúng trong mọi trường hợp:

- Bài có trong danh sách: chuyển lên đầu, trả về `True`. Số bài **không đổi**.
- Bài đang đứng **cuối**: sau khi chuyển, `tail` phải là bài đứng trước nó.
- Bài **đã ở đầu**: không làm gì, vẫn trả về `True`.
- Bài **không có** trong danh sách (ví dụ đã bị gỡ khỏi kho nhạc): danh sách giữ nguyên, trả về `False`.
- Danh sách **rỗng**: trả về `False`.

Kịch bản kiểm tra của nhóm: danh sách `ZM001` đến `ZM004`; lần lượt "Phát ngay" `ZM003`, `ZM004`, `ZM004` lần nữa, `ZM999`; thêm `ZM005` vào cuối; cuối cùng "Phát ngay" trên một danh sách mới tạo.

Kết quả đúng cần hiển thị:

```plaintext
Phát ngay ZM003: True
Danh sách phát: ZM003 -> ZM001 -> ZM002 -> ZM004 -> None | số bài: 4
Phát ngay ZM004: True
Danh sách phát: ZM004 -> ZM003 -> ZM001 -> ZM002 -> None | bài cuối: ZM002
Phát ngay ZM004 lần nữa: True
Phát ngay ZM999: False
Danh sách phát: ZM004 -> ZM003 -> ZM001 -> ZM002 -> ZM005 -> None | số bài: 5
Phát ngay trên danh sách mới: False
```

### 2. Vấn đề hiện tại

Người nghe phản ánh: sau vài lần bấm "Phát ngay", danh sách phát có **bài bị lặp**, xuất hiện cả **bài không tồn tại**, số bài hiển thị **tăng dần**, và bài thêm vào sau đó **không hiện ra**.

Lập trình viên trước đã viết `play_now` theo ý "gỡ bài ra rồi thêm lại ở đầu", nhưng chưa xử lý đủ các trường hợp của thao tác gỡ một node:

- Gỡ một node ở giữa: nối node đứng trước sang node đứng sau, và **giảm `size`**; nếu không, lần `add_first` ngay sau đó làm `size` tăng thêm 1.
- Gỡ node **cuối**: `tail` phải lùi về node đứng trước.
- Node cần gỡ là **`head`**: vòng lặp tìm theo `prev.next` không bao giờ xét tới `head`.
- **Không tìm thấy**: phải dừng và trả về `False`, không được thêm gì vào danh sách.

### 3. Mã nguồn hiện tại (Legacy Code)

Tệp `phat_ngay.py` trong thư mục khởi đầu có sẵn lớp `Node`, lớp `Playlist` (các phương thức `add_first`, `add_last`, `find`, `to_text` đã đúng, không cần sửa). Phần cần xem xét là hàm `play_now` và đoạn chạy thử:

```python
def play_now(playlist, code):
    # Chuyển bài có mã code lên đầu danh sách phát. Trả True nếu bài có trong danh sách, False nếu không.
    prev = playlist.head
    while prev.next is not None:
        if prev.next.value == code:
            prev.next = prev.next.next
            break
        prev = prev.next
    playlist.add_first(code)
    return True


playlist = Playlist()
for code in ["ZM001", "ZM002", "ZM003", "ZM004"]:
    playlist.add_last(code)
print("Phát ngay ZM003:", play_now(playlist, "ZM003"))
print("Danh sách phát:", playlist.to_text(), "| số bài:", playlist.size)
print("Phát ngay ZM004:", play_now(playlist, "ZM004"))
print("Danh sách phát:", playlist.to_text(), "| bài cuối:", playlist.tail.value)
print("Phát ngay ZM004 lần nữa:", play_now(playlist, "ZM004"))
print("Phát ngay ZM999:", play_now(playlist, "ZM999"))
playlist.add_last("ZM005")
print("Danh sách phát:", playlist.to_text(), "| số bài:", playlist.size)

# Danh sách mới tạo, chưa có bài nào
empty = Playlist()
print("Phát ngay trên danh sách mới:", play_now(empty, "ZM001"))

```

Kết quả hiển thị trên Console:

```plaintext
Phát ngay ZM003: True
Danh sách phát: ZM003 -> ZM001 -> ZM002 -> ZM004 -> None | số bài: 5
Phát ngay ZM004: True
Danh sách phát: ZM004 -> ZM003 -> ZM001 -> ZM002 -> None | bài cuối: ZM004
Phát ngay ZM004 lần nữa: True
Phát ngay ZM999: True
Danh sách phát: ZM999 -> ZM004 -> ZM004 -> ZM003 -> ZM001 -> ZM002 -> None | số bài: 9
Traceback (most recent call last):
  ...
    while prev.next is not None:
AttributeError: 'NoneType' object has no attribute 'next'
```

Chương trình dừng ở lần gọi trên danh sách mới. Trước đó, đối chiếu với kết quả đúng: số bài sau lần đầu là 5 thay vì 4; bài cuối sau lần hai là `ZM004` thay vì `ZM002`; "Phát ngay" `ZM999` trả về `True`; danh sách cuối cùng có `ZM999`, có hai bài `ZM004`, không có `ZM005`, và số bài là 9.

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Sau lần gọi đầu tiên, danh sách in ra đúng thứ tự nhưng số bài là 5. Dòng lệnh nào làm `size` tăng, và thiếu dòng lệnh nào để bù lại?
- Ở lần gọi thứ hai (`ZM004` đang đứng cuối), sau khi gỡ thì `tail` đang trỏ tới node nào? Cần thêm lệnh gì, ở đâu?
- Ở lần gọi thứ ba (`ZM004` đang ở đầu), vòng `while` có xét tới node `head` không? Vì sao danh sách có hai bài `ZM004`?
- Ở lần gọi với `ZM999`, vòng `while` kết thúc như thế nào? Vì sao `ZM999` vẫn được thêm vào và hàm vẫn trả về `True`?
- Vì sao `ZM005` không xuất hiện khi duyệt từ `head`, dù `add_last` đã chạy? (Gợi ý: xem lại câu trả lời về `tail`.)
- Vì sao gọi `play_now` trên danh sách rỗng báo `AttributeError`?
- Liệt kê theo thứ tự các trường hợp mà `play_now` phải kiểm tra trước khi gỡ node, và giá trị trả về của từng trường hợp.
- Big-O thời gian của `play_now` là gì (n là số bài)? Phần nào của hàm quyết định chi phí đó?

**(2) Sửa lỗi**

- Viết lại hàm `play_now` trong `phat_ngay.py`. Không đổi tên hàm, tham số; không sửa lớp `Playlist`; không dùng list Python để lưu các bài.
- Chạy `python phat_ngay.py` phải cho đúng kết quả:

```plaintext
Phát ngay ZM003: True
Danh sách phát: ZM003 -> ZM001 -> ZM002 -> ZM004 -> None | số bài: 4
Phát ngay ZM004: True
Danh sách phát: ZM004 -> ZM003 -> ZM001 -> ZM002 -> None | bài cuối: ZM002
Phát ngay ZM004 lần nữa: True
Phát ngay ZM999: False
Danh sách phát: ZM004 -> ZM003 -> ZM001 -> ZM002 -> ZM005 -> None | số bài: 5
Phát ngay trên danh sách mới: False
```

- Chạy `pytest -q` phải xanh cả 5 test.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex06`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-06 rồi chép các tệp vào kho: `phat_ngay.py`, `test_phat_ngay.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong tệp mã nguồn.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
