# Chế độ "Phát ngược" cho danh sách phát Zing MP3

### 1. Bối cảnh & Vấn đề

![Người nghe muốn nghe danh sách phát theo thứ tự ngược lại: xem trước, rồi áp dụng hẳn.](minh_hoa.png)

*Người nghe muốn nghe danh sách phát theo thứ tự ngược lại: xem trước, rồi áp dụng hẳn.*

Trong ứng dụng nghe nhạc Zing MP3, người nghe hay thêm bài mới vào cuối danh sách phát, nên các bài mới nhất luôn phải chờ lâu nhất. Nhóm sản phẩm bổ sung chế độ **"Phát ngược"**, gồm hai nút:

- **"Xem trước"**: hiện một bản đảo ngược của danh sách phát để người nghe xem thử. Danh sách phát đang dùng không được thay đổi.
- **"Áp dụng"**: đảo hẳn thứ tự của danh sách phát đang dùng.

Danh sách phát là **danh sách liên kết đơn có `head`, `tail`, `size`**, mỗi node giữ một mã bài:

```plaintext
Trước:   ZM001 -> ZM002 -> ZM003 -> ZM004 -> None      (head là ZM001, tail là ZM004)
Sau:     ZM004 -> ZM003 -> ZM002 -> ZM001 -> None      (head là ZM004, tail là ZM001)
```

Vấn đề: danh sách liên kết đơn chỉ đi được một chiều, không thể "đi lùi từ cuối về đầu" để đọc ngược. Một danh sách phát của người dùng trả phí có thể tới 10.000 bài, và nút "Áp dụng" chạy ngay trên điện thoại, nên nhóm quan tâm cả thời gian lẫn **bộ nhớ dùng thêm**.

Bạn được giao thiết kế và viết hai chức năng này. Trưởng nhóm yêu cầu bạn đề xuất ít nhất hai cách đảo thứ tự, so sánh, rồi quyết định cách nào dùng cho nút nào.

### 2. Yêu cầu nghiệp vụ

Tệp `dao_nguoc.py` có sẵn lớp `Node` và lớp `Playlist` (với `add_last`, `to_text` đã đúng). Bạn viết hai hàm.

**2.1. Xem trước: `reversed_copy(playlist)`**

- Trả về một **`Playlist` mới** chứa các bài của `playlist` theo thứ tự ngược lại, với `head`, `tail`, `size` đúng.
- `playlist` gốc giữ nguyên: đúng các node cũ, đúng thứ tự cũ.
- Hai danh sách **không dùng chung node nào**: sau đó thêm bài vào danh sách này không làm đổi danh sách kia.
- Chi phí thời gian yêu cầu: O(n).

**2.2. Áp dụng: `reverse_in_place(playlist)`**

- Đảo thứ tự ngay trên `playlist`, **không tạo node mới**: sau khi đảo, danh sách vẫn gồm đúng các node cũ, chỉ có các liên kết `next`, `head`, `tail` thay đổi.
- Hàm không trả về gì (`None`).
- Chi phí yêu cầu: thời gian O(n), bộ nhớ dùng thêm O(1).

Ràng buộc cho cả hai hàm: không chép các bài sang list, tuple, dict hay chuỗi; không dùng đệ quy.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Bản xem trước dính vào danh sách gốc**

- Tạo bản đảo của `ZM001`, `ZM002`, `ZM003`, rồi thêm `ZM009` vào bản đảo và thêm `ZM004` vào danh sách gốc. Kết quả đúng:

```plaintext
Bản đảo:        ZM003 -> ZM002 -> ZM001 -> ZM009 -> None
Danh sách gốc:  ZM001 -> ZM002 -> ZM003 -> ZM004 -> None
```

- Nếu bản đảo dùng lại node của danh sách gốc, một trong hai dòng trên sẽ sai.

**Bẫy 2 — "Áp dụng" lại tạo node mới**

- Bộ test giữ lại các node trước khi đảo và so sánh **chính các node đó** sau khi đảo. Cách "tạo bản đảo rồi gán `head` của nó cho danh sách cũ" không vượt qua được test này.

**Bẫy 3 — Quên `tail` sau khi đảo**

- Sau khi đảo `ZM001`, `ZM002`, `ZM003`, node `ZM001` phải là `tail` và `tail.next` phải là `None`. Nếu `tail` vẫn chỉ vào `ZM003` (lúc này là node đầu), lệnh `add_last("ZM004")` sẽ nối bài mới vào sau node đầu và làm mất hai bài `ZM002`, `ZM001`. Kết quả đúng sau khi thêm:

```plaintext
ZM003 -> ZM002 -> ZM001 -> ZM004 -> None
```

**Bẫy 4 — Danh sách trống hoặc chỉ có một bài**

- Cả hai hàm không được báo lỗi. Danh sách trống: `head` và `tail` vẫn là `None`, bản đảo là một `Playlist` trống. Danh sách một bài: giữ nguyên, `head` và `tail` cùng chỉ một node, và thêm bài sau đó vẫn đúng.

**Bẫy 5 — Mất phần sau của danh sách khi đổi chiều liên kết**

- Khi đổi `next` của một node để nó trỏ về node đứng trước, nếu chưa giữ lại node đứng sau thì phần còn lại của danh sách không còn đường tới. Dấu hiệu: danh sách sau khi đảo chỉ còn một hoặc hai bài. Bộ test có trường hợp đảo hai lần liên tiếp phải ra đúng thứ tự ban đầu, đủ năm bài.

**Kịch bản chạy thử.** Chạy `python dao_nguoc.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Bản đảo: ZM004 -> ZM003 -> ZM002 -> ZM001 -> None
Danh sách gốc: ZM001 -> ZM002 -> ZM003 -> ZM004 -> None
Bản đảo sau khi thêm ZM005: ZM004 -> ZM003 -> ZM002 -> ZM001 -> ZM005 -> None | số bài: 5
Danh sách gốc: ZM001 -> ZM002 -> ZM003 -> ZM004 -> None | số bài: 4
Đảo tại chỗ: ZM004 -> ZM003 -> ZM002 -> ZM001 -> None
Bài đầu: ZM004 | bài cuối: ZM001
Sau khi thêm ZM006: ZM004 -> ZM003 -> ZM002 -> ZM001 -> ZM006 -> None | số bài: 5
Danh sách trống: None | None
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ ba phần sau:

**(1) Đề xuất và phân tích nhiều giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output của hai hàm: kiểu dữ liệu đầu vào, giá trị trả về, trạng thái của danh sách gốc sau khi gọi, trong trường hợp thường và trong từng bẫy.
- Đề xuất **ít nhất hai giải pháp** khác nhau về cách làm cho việc đảo thứ tự một danh sách liên kết đơn. Với mỗi giải pháp: mô tả ý tưởng trong 2–3 câu, vẽ hình minh họa trên ví dụ ở mục 1, viết mã giả.
- So sánh các giải pháp theo bảng 5 tiêu chí: thời gian (Big-O), bộ nhớ dùng thêm (Big-O), có giữ nguyên danh sách gốc hay không, độ dễ đọc và dễ bảo trì, mức phù hợp với bối cảnh của bài.
- Chọn giải pháp dùng cho từng nút ("Xem trước", "Áp dụng") và nêu lý do dựa trên bảng so sánh. Lựa chọn không có lý do không được tính điểm.
- Với danh sách 10.000 bài, ước lượng số node được tạo thêm của từng giải pháp.

**(2) Chạy tay**

- Lập bảng chạy tay giải pháp đảo tại chỗ trên danh sách `ZM001`, `ZM002`, `ZM003`: sau mỗi vòng lặp, ghi giá trị của từng biến con trỏ và vẽ lại các liên kết.

**(3) Triển khai code**

- Viết thân hai hàm trong `dao_nguoc.py`. Không đổi tên hàm, tham số; không sửa lớp `Playlist`.
- Xử lý đủ 5 bẫy ở mục 3; `python dao_nguoc.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 8 test.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ đổi chiều liên kết.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session07_Ex14`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-07-danh-sach-lien-ket/bai-14 rồi chép các tệp vào kho: `dao_nguoc.py`, `test_dao_nguoc.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `dao_nguoc.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
