# Bài tập về nhà Session 07: Danh sách liên kết

Ngân hàng 20 bài, 5 mức: Cài lại (K1–K4), Cơ bản (C1–C4), Nâng cao (N1–N4), Phân tích (P1–P4), Sáng tạo (S1–S4). Giảng viên chọn bài giao trên hệ thống; đề giao mặc định gồm 8 bài: 2 Cài lại, 2 Cơ bản, 2 Nâng cao, 1 Phân tích, 1 Sáng tạo.

Bối cảnh chung: phòng đào tạo (chị Lan, anh Hùng) lưu một số dữ liệu bằng danh sách liên kết: lộ trình khóa học, hàng chờ chấm bài, các phiên bản bản nháp bài nộp.

**Cách làm và tự kiểm tra**

- Mỗi bài có tệp `bai_xx.py` trong thư mục `starter/`. Viết vào đúng hàm hoặc biến đã cho, không đổi tên.
- Bốn bài Cài lại (K1–K4) tự viết lớp trong tệp của bài, không dùng `lien_ket.py`. Từ mức Cơ bản trở đi: `lien_ket.py` chứa đúng các lớp `Node`, `LinkedList`, `DNode`, `DoublyLinkedList` của bài đọc Session 07 cùng hai hàm tạo nhanh `make_list(values)`, `make_dlist(values)`. Dùng lại, không sửa tệp này.
- Chạy `pytest -q` trong `starter/` để kiểm mọi bài, hoặc `pytest -q test_bai_c1.py` để kiểm một bài (cài trước bằng `pip install pytest`). Lúc mới nhận đề, mọi test đều đỏ.
- Cần Python 3.10 trở lên. Đo thời gian bằng `timeit` trên máy của bạn, không đo trong khung chạy của bài đọc.
- Giảng viên chấm thêm bằng một bộ kiểm tra ẩn: dữ liệu khác đề, danh sách rỗng, một phần tử, thao tác trúng `head` hoặc `tail`, liên kết hai chiều.
- Mỗi thao tác thêm, xóa phải để `head`, `tail` (và `prev` với danh sách đôi) đúng. Vẽ trước, viết mã sau.

---

## Mức Cài lại

Bốn bài này yêu cầu bạn **tự viết lại** các thao tác đã học ở Session 07, từ khung lớp rỗng. Mỗi tệp `bai_kx.py` có sẵn lớp node, hàm khởi tạo và phần ghi chú của từng phương thức; thân phương thức đang là `raise NotImplementedError`. Viết bằng trí nhớ và hình vẽ của bạn: không nhập `lien_ket.py`, không chép từ bài đọc. Từ K2, lớp có thêm thuộc tính `size` (số node) mà bài đọc không có; mỗi thao tác thêm, xóa phải giữ `size` đúng.

### K1. Cài lại các thao tác duyệt

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_k1.py`

Lộ trình học là một danh sách liên kết đơn các mã khóa học. Viết bốn phương thức của lớp `LinkedList`, đều duyệt bằng biến `current` và không làm thay đổi danh sách:

1. `count()`: trả về số node.
2. `find(value)`: trả về vị trí (tính từ 0) của node đầu tiên có giá trị `value`; không có thì trả `None`.
3. `get(position)`: trả về giá trị ở vị trí `position`; vị trí âm hoặc từ số node trở lên thì báo `IndexError("vị trí ngoài phạm vi")`.
4. `to_text()`: trả về chuỗi dạng `"KH1 -> KH2 -> None"`.

| Danh sách | Gọi | Kết quả |
|---|---|---|
| KH1 → KH2 → KH3 | `count()`, `find("KH3")`, `get(0)` | `3`, `2`, `"KH1"` |
| KH1 → KH2 → KH3 | `find("KH9")` | `None` |
| KH1 → KH2 | `get(2)` | `IndexError: vị trí ngoài phạm vi` |
| danh sách rỗng | `count()`, `to_text()` | `0`, `"None"` |

### K2. Cài lại thao tác thêm ở đầu và ở cuối

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_k2.py`

Hàng chờ hỗ trợ nhận phiếu thường ở cuối và phiếu gấp ở đầu. Viết hai phương thức của lớp `LinkedList` có `head`, `tail`, `size`:

1. `add_first(value)`: thêm vào đầu trong O(1).
2. `add_last(value)`: thêm vào cuối trong O(1) nhờ `tail`, không duyệt từ `head`.

Sau mỗi lần thêm: `head` là node đầu, `tail` là node cuối, `size` tăng đúng 1. Thêm vào danh sách rỗng thì `head` và `tail` cùng trỏ tới node mới.

| Các lệnh (chạy nối tiếp trên danh sách rỗng) | `to_text()` | `tail.value` | `size` |
|---|---|---|---|
| `add_last("YC2")` | `"YC2 -> None"` | `"YC2"` | 1 |
| `add_first("YC1")` | `"YC1 -> YC2 -> None"` | `"YC2"` | 2 |
| `add_last("YC3")` | `"YC1 -> YC2 -> YC3 -> None"` | `"YC3"` | 3 |

### K3. Cài lại thao tác xóa

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_k3.py`

Nhân viên lấy phiếu ở đầu hàng chờ để xử lý, và học viên có thể hủy một phiếu bất kỳ. Viết hai phương thức (tệp đã cho sẵn `add_last` và `to_text`):

1. `remove_first()`: xóa node đầu và trả về giá trị của nó; danh sách rỗng thì báo `IndexError("danh sách rỗng, không có phần tử để lấy")`.
2. `remove(value)`: xóa node đầu tiên có giá trị `value`, trả `True`; không có thì trả `False` và danh sách giữ nguyên.

Bốn trường hợp phải đúng: danh sách rỗng; xóa node duy nhất (`head` và `tail` đều là `None`); xóa node đầu; xóa node cuối (`tail` lùi về node đứng trước). `size` giảm đúng 1 mỗi lần xóa được.

| Danh sách | Gọi | Kết quả |
|---|---|---|
| YC1 → YC2 → YC3 | `remove_first()` | `"YC1"`, còn YC2 → YC3, `size` 2 |
| YC1 → YC2 → YC3 | `remove("YC3")` | `True`, `tail.value` là `"YC2"`, `size` 2 |
| YC1 | `remove_first()` | `"YC1"`, `head` và `tail` là `None`, `size` 0 |
| YC1 → YC2 | `remove("YC9")` | `False`, không đổi |

### K4. Cài lại danh sách liên kết đôi

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_k4.py`

Các phiên bản nháp bài nộp cần xem được từ cũ đến mới và từ mới về cũ. Viết năm phương thức của lớp `DoublyLinkedList` có `head`, `tail`, `size` (tệp đã cho sẵn `DNode` và `to_text`):

1. `add_first(value)`, `add_last(value)`: thêm ở hai đầu trong O(1), nối đủ cả `next` và `prev`.
2. `remove_first()`, `remove_last()`: xóa ở hai đầu trong O(1), trả về giá trị đã xóa; danh sách rỗng thì báo `IndexError("danh sách rỗng, không có phần tử để xóa")`.
3. `to_text_backward()`: trả về chuỗi các giá trị từ `tail` về `head`, đi theo `prev`.

Sau mỗi thao tác: `prev` của `head` là `None`, `next` của `tail` là `None`; xóa node duy nhất thì `head` và `tail` đều là `None`.

| Danh sách | Gọi | Kết quả |
|---|---|---|
| V1 ⇄ V2 ⇄ V3 | `to_text_backward()` | `"V3 -> V2 -> V1 -> None"` |
| V1 ⇄ V2 ⇄ V3 | `remove_last()` | `"V3"`, `tail.value` là `"V2"`, `size` 2 |
| V1 ⇄ V2 ⇄ V3 | `remove_first()` | `"V1"`, `prev` của `head` mới là `None` |
| V1 | `remove_last()` | `"V1"`, `head` và `tail` là `None` |

---

## Mức Cơ bản

### C1. Tổng thời lượng một lộ trình học

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_c1.py`

Mỗi lộ trình học là một `LinkedList`, mỗi node giữ số phút của một bài học. Viết `total_minutes(path)` trả về bộ (tổng số phút, số node đã đi qua). Duyệt bằng biến `current`; sau khi gọi, lộ trình phải còn nguyên.

| Đầu vào (giá trị các node) | Đầu ra |
|---|---|
| 45 → 30 → 60 | `(135, 3)` |
| danh sách rỗng | `(0, 0)` |

### C2. Dựng hàng chờ chấm bài từ danh sách mã

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_c2.py`

Hệ thống chấm bài nhận một list Python các mã bài nộp theo thứ tự đến. Viết `from_codes(codes)` trả về một `LinkedList` mới chứa các mã đúng thứ tự đó: mã đầu ở `head`, mã cuối ở `tail`.

| Đầu vào | `to_text()` của kết quả | `tail.value` |
|---|---|---|
| `["BN201", "BN202", "BN203"]` | `"BN201 -> BN202 -> BN203 -> None"` | `"BN203"` |
| `[]` | `"None"` | (tail là `None`) |

### C3. Big-O của sáu thao tác

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_c3.py`

Ghi Big-O thời gian (trường hợp xấu nhất) của từng thao tác vào dict `ANSWERS`, dạng `"O(1)"` hoặc `"O(n)"`. n là số phần tử.

| Khóa | Thao tác |
|---|---|
| `"a"` | `add_first` trên `LinkedList` |
| `"b"` | `add_last` trên `LinkedList` có `tail` |
| `"c"` | `find` trên `LinkedList` |
| `"d"` | `insert(0, x)` trên list Python |
| `"e"` | đọc giá trị ở vị trí k (k gần n) trên `LinkedList` |
| `"f"` | `remove_last` trên `DoublyLinkedList` |

### C4. Đọc các phiên bản nháp từ mới đến cũ

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_c4.py`

Các phiên bản nháp bài nộp lưu trong `DoublyLinkedList`, cũ nhất ở `head`, mới nhất ở `tail`. Viết `to_list_backward(drafts)` trả list Python các giá trị từ `tail` về `head`. Phải đi theo liên kết `prev`; không duyệt xuôi rồi đảo ngược.

| Đầu vào | Đầu ra |
|---|---|
| V1 ⇄ V2 ⇄ V3 | `["V3", "V2", "V1"]` |
| danh sách rỗng | `[]` |

---

## Mức Nâng cao

### N1. Chèn khóa bổ trợ ngay sau khóa nền

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_n1.py`

Lộ trình học là `LinkedList` các mã khóa học. Anh Hùng cần chèn một khóa bổ trợ ngay sau một khóa nền. Viết `insert_after(path, target, value)`: chèn `value` ngay sau node **đầu tiên** có giá trị `target`, trả `True`; không có `target` thì trả `False` và lộ trình giữ nguyên. Chèn sau node cuối thì `tail` phải chuyển sang node mới.

| Lộ trình | Gọi | Kết quả |
|---|---|---|
| KH1 → KH2 → KH3 | `insert_after(p, "KH2", "KH9")` | `True`, KH1 → KH2 → KH9 → KH3 |
| KH1 → KH2 → KH3 | `insert_after(p, "KH3", "KH8")` | `True`, `tail.value` là `"KH8"` |
| KH1 | `insert_after(p, "KH5", "KH9")` | `False`, không đổi |

### N2. Rút mọi bài nộp của một học viên

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_n2.py`

Hàng chờ chấm bài là `LinkedList` các mã học viên; một học viên có thể nộp nhiều bài. Khi học viên rút khỏi khóa, chị Lan cần xóa mọi bài của người đó. Viết `remove_all(queue, code)` xóa mọi node có giá trị `code`, trả về số node đã xóa. `head` và `tail` phải đúng; xóa hết thì cả hai là `None`.

| Hàng chờ | Gọi | Kết quả |
|---|---|---|
| HV1 → HV7 → HV2 → HV7 | `remove_all(q, "HV7")` | `2`, HV1 → HV2, `tail` là HV2 |
| HV7 → HV7 | `remove_all(q, "HV7")` | `2`, `head` và `tail` là `None` |

### N3. Đưa yêu cầu ưu tiên lên đầu hàng

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_n3.py`

Viết `move_to_front(queue, code)`: đưa node đầu tiên có giá trị `code` lên đầu hàng chờ, trả `True`; đã ở đầu thì giữ nguyên và vẫn trả `True`; không có thì trả `False`, hàng chờ không đổi. Được dùng lại các phương thức của `LinkedList`.

| Hàng chờ | Gọi | Kết quả |
|---|---|---|
| A → B → C | `move_to_front(q, "C")` | `True`, C → A → B, `tail` là B |
| A → B | `move_to_front(q, "Z")` | `False`, không đổi |

### N4. Chỉ giữ k phiên bản nháp mới nhất

Tầng: Bắt buộc · Mức AI: AI-0 · Tệp: `bai_n4.py`

Để tiết kiệm bộ nhớ, hệ thống chỉ giữ k phiên bản nháp mới nhất. Viết `keep_latest(drafts, k)` trên `DoublyLinkedList`: bỏ các phiên bản cũ ở đầu cho tới khi còn nhiều nhất k node, trả về số node đã bỏ. k âm thì báo `ValueError("số phiên bản giữ lại không được âm")`. Duyệt xuôi và duyệt ngược đều phải đúng.

| Phiên bản | Gọi | Kết quả |
|---|---|---|
| V1 ⇄ V2 ⇄ V3 ⇄ V4 ⇄ V5 | `keep_latest(d, 3)` | `2`, còn V3 ⇄ V4 ⇄ V5 |
| V1 ⇄ V2 | `keep_latest(d, 5)` | `0`, không đổi |

---

## Mức Phân tích

### P1. Phản biện mã AI cho hàng chờ chấm bài

Tầng: Nâng cao (tùy chọn) · Mức AI: AI-2 · Tệp: `bai_p1.py`, `ai_danh_sach.py`, `nhat_ky_phan_bien.md`

Anh Hùng nhờ AI viết ba hàm trong `ai_danh_sach.py`; mỗi hàm có một dòng nhận xét của AI. Với một lần gọi trên dữ liệu thường, cả ba đều trả kết quả đúng. Việc của bạn:

1. Đọc từng hàm, thử gọi hai lần liên tiếp, đối chiếu với nhận xét. Ghi `"đúng"` hoặc `"sai"` vào dict `CLAIMS`.
2. Viết `count_waiting_fixed(queue)` và `newest_submission_fixed(queue)`: cùng kết quả với bản của AI, không làm thay đổi `queue`, và `newest_submission_fixed` chạy trong O(1).
3. Điền bảng giữ – sửa – loại bỏ trong `nhat_ky_phan_bien.md`, mỗi hàm một dòng.

### P2. Đo tỉ lệ thời gian chèn ở đầu

Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Tệp: `bai_p2.py`

Viết `time_front_inserts(kind, n, number=1000)` trả số mili giây cho `number` lần chèn ở đầu vào cấu trúc có sẵn n phần tử: `kind == "list"` dùng `list.insert(0, x)`, `kind == "linked"` dùng `add_first`. Tạo cấu trúc trong phần chuẩn bị (`setup`) của `timeit`, đo 5 lần, lấy lần nhỏ nhất. Chạy `python bai_p2.py` với n = 50.000 và 100.000, rồi ghi vào `RATIOS` thời gian gấp khoảng bao nhiêu lần khi n gấp đôi: `"x1"`, `"x2"` hoặc `"x4"`.

### P3. Dựng dữ liệu tốt nhất và xấu nhất

Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Tệp: `bai_p3.py`

Viết ba hàm, mỗi hàm trả bộ (list n mã, mã cần dùng):

- `best_case_find(n)`: `find` chỉ so sánh 1 lần.
- `worst_case_find(n)`: `find` so sánh đủ n lần rồi trả `None`.
- `tail_case_remove(n)` (n ≥ 2): `remove` xóa đúng node cuối, nên `tail` phải lùi về node đứng trước.

Ghi Big-O của `find` trong trường hợp xấu nhất vào `FIND_WORST`.

### P4. Chọn cấu trúc cho năm tình huống

Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Tệp: `bai_p4.py`

Với mỗi tình huống, ghi vào `CHOICES` một trong ba giá trị `"list"`, `"don"` (danh sách liên kết đơn có `tail`), `"doi"` (danh sách liên kết đôi), và một câu lý do vào `LY_DO`.

| Khóa | Tình huống |
|---|---|
| `t1` | Bảng điểm 5.000 bài, giảng viên thường mở bài thứ k bất kỳ |
| `t2` | Hàng chờ phỏng vấn mentor: liên tục chen ứng viên ưu tiên lên đầu và lấy người ở đầu; không cần đi lùi |
| `t3` | Hàng chờ chấm lại: bài gấp chen lên đầu, bài thường thêm ở cuối; giảng viên lấy bài ở đầu để chấm, và hay hủy bài vừa thêm ở cuối khi học viên nộp nhầm (hàng có hàng nghìn bài) |
| `t4` | Danh sách phiếu hỗ trợ đã xử lý của quầy, giữ 20.000 phiếu gần nhất: mỗi phiếu vừa xử lý thêm vào đầu (mới nhất đứng đầu); quá 20.000 phiếu thì bỏ phiếu cũ nhất ở cuối; trang "Xem lại từ đầu ca" in từ cũ nhất đến mới nhất |
| `t5` | Danh sách khóa học: chỉ thêm ở cuối, duyệt từ đầu, thỉnh thoảng lấy khóa thứ k |

---

## Mức Sáng tạo

Mỗi bài Sáng tạo gồm ba phần:

- Bạn tự chọn cách làm, ghi lý do và Big-O vào `GIAI_THICH`.
- Bạn tự viết hàm `tu_kiem_tra()`, có ít nhất 3 lệnh `assert`, trong đó có trường hợp biên (rỗng, một phần tử, trúng `head` hoặc `tail`).
- Giảng viên chấm 10 điểm:
  - 4 điểm: chạy đúng bộ kiểm tra ẩn.
  - 2 điểm: đạt yêu cầu về thời gian và bộ nhớ.
  - 2 điểm: `tu_kiem_tra()` đủ trường hợp biên.
  - 2 điểm: giải thích đúng Big-O.

### S1. Gộp các lượt nộp trùng liền kề

Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Tệp: `bai_s1.py`

Học viên bấm nộp nhiều lần liên tiếp nên hàng chờ có các node trùng nhau đứng cạnh nhau. Viết `dedupe_adjacent(queue)` bỏ mọi node có giá trị bằng node đứng ngay trước nó, trả về số node đã bỏ. Yêu cầu: một lần duyệt, không tạo list Python mới (bộ nhớ phụ O(1)), `tail` đúng.

| Đầu vào | Đầu ra |
|---|---|
| S1 → S1 → S2 → S2 → S2 → S3 | `3`, S1 → S2 → S3 |

### S2. Tách bảng điểm thành đạt và chưa đạt

Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Tệp: `bai_s2.py`

Viết `split_by_score(scores, threshold)` trả bộ (passed, failed) là hai `LinkedList` mới: passed gồm điểm ≥ threshold, failed gồm điểm còn lại, giữ đúng thứ tự cũ. Không làm thay đổi `scores`; thời gian O(n).

| Đầu vào | threshold | Đầu ra |
|---|---|---|
| 7 → 4 → 9 → 5 → 3 | 5 | passed 7 → 9 → 5, failed 4 → 3 |

### S3. Lịch sử bản nháp có lùi và tiến

Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Tệp: `bai_s3.py`

Viết lớp `DraftHistory` dùng các `DNode` nối hai chiều, với `save(text)`, `back()`, `forward()`, `current()` như docstring trong tệp. Lưu bản mới sau khi đã lùi thì các bản đứng sau bản đang xem bị bỏ. Mỗi thao tác O(1).

| Thao tác | Kết quả |
|---|---|
| save v1, v2, v3; back(); back(); back() | `"v2"`, `"v1"`, `None` |
| forward(); save v4; forward(); current() | `"v2"`, (không trả), `None`, `"v4"` |

### S4. Chèn điểm vào bảng đã xếp tăng dần

Tầng: Nâng cao (tùy chọn) · Mức AI: AI-0 · Tệp: `bai_s4.py`

Bảng điểm là `LinkedList` đã xếp tăng dần. Viết `insert_sorted(scores, value)` chèn `value` sao cho bảng vẫn tăng dần; giá trị bằng nhau thì node mới đứng sau các node bằng nó. `head` và `tail` phải đúng. Không dùng `sort()`, `sorted()`.

| Bảng | Gọi | Kết quả |
|---|---|---|
| 3 → 5 → 9 | `insert_sorted(s, 7)` | 3 → 5 → 7 → 9 |
| 3 → 5 → 7 → 9 | `insert_sorted(s, 1)` rồi `insert_sorted(s, 10)` | `head` là 1, `tail` là 10 |
