# Mảng động biết thu gọn cho bộ đệm cuốc xe của tài xế Grab

### 1. Bối cảnh & Vấn đề

![Giờ cao điểm bộ đệm phình to; hết giờ cao điểm, bộ nhớ vẫn bị giữ nguyên trên chiếc điện thoại cũ của tài xế.](minh_hoa.png)

*Giờ cao điểm bộ đệm phình to; hết giờ cao điểm, bộ nhớ vẫn bị giữ nguyên trên chiếc điện thoại cũ của tài xế.*

Ứng dụng tài xế Grab giữ một **bộ đệm cuốc xe** chờ gửi lên máy chủ: lúc mất sóng thì cuốc được thêm vào cuối bộ đệm, có sóng lại thì lấy dần từ cuối ra để gửi. Giờ cao điểm bộ đệm có thể lên hàng nghìn cuốc; hết giờ cao điểm chỉ còn vài cuốc. Nhiều tài xế dùng điện thoại cũ, bộ nhớ ít, nên nhóm muốn bộ đệm **trả bớt bộ nhớ** khi không cần.

Thiết bị chạy bản Python rút gọn, nên nhóm tự cài lớp `ShrinkArray` theo Lesson 04, có thêm phần **thu gọn**:

- Đầy thì cấp vùng gấp đôi (như Lesson 04).
- Sau khi lấy một phần tử, nếu số phần tử còn lại **không quá một phần tư** số ô và vùng có hơn 1 ô, thì cấp vùng **bằng một nửa** và chép các phần tử sang.

Một bạn trong nhóm đề xuất thu gọn ngay khi còn **một nửa** cho tiết kiệm hơn. Trưởng nhóm từ chối và yêu cầu bạn giải thích bằng số liệu vì sao ngưỡng là một phần tư (bẫy 3).

Bài này tổng hợp kiến thức cả buổi: ADT và kiểm tra chỉ số, mảng động và O(1) khấu hao, chi phí chép khi đổi vùng lưu trữ.

### 2. Yêu cầu nghiệp vụ

**2.1. `size()`, `capacity()`, `items()`**: số phần tử; số ô của vùng lưu trữ; list các phần tử theo thứ tự.

**2.2. `get(i)`**: phần tử tại chỉ số i (âm tính từ cuối); chỉ số không phải số nguyên báo `TypeError`, ngoài phạm vi báo `IndexError("Chỉ số ngoài phạm vi phần tử")`.

**2.3. `append(value)`, `pop()`**: thêm vào cuối; lấy và xóa phần tử cuối, rồi thu gọn theo quy tắc trên. Lấy từ mảng rỗng báo `IndexError("Mảng rỗng")`. `copies` đếm mọi tham chiếu đã chép khi đổi vùng.

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Thu gọn đúng ngưỡng.** 9 phần tử (16 ô), lấy 7 lần còn 2 phần tử trong 4 ô; lấy thêm 1 còn 2 ô; lấy hết còn 1 ô.

**Bẫy 2 — Lấy từ mảng rỗng.** Báo đúng lỗi, mảng giữ nguyên.

**Bẫy 3 — Thêm rồi lấy liên tục ở ngưỡng.** Mảng 8 phần tử (8 ô), lặp 1.000 lần "thêm một, lấy một": tổng số tham chiếu chép thêm không quá 32.

**Bẫy 4 — Không giữ tham chiếu thừa.** Mọi ô từ chỉ số `size()` trở đi là `None`.

**Bẫy 5 — Chi phí tuyến tính.** Thêm 100.000 rồi lấy hết: tổng số tham chiếu đã chép không quá 400.000, cuối cùng còn 1 ô.

**Kịch bản chạy thử.** Chạy `python mang_thu_gon.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Sau 9 lần thêm: 9 phần tử, 16 ô
Sau 7 lần lấy: ['CX1', 'CX2'] | 4 ô
1.000 lần thêm rồi lấy ở ngưỡng, số tham chiếu chép thêm: 0
Lấy từ mảng rỗng: Mảng rỗng
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, phương thức, trong trường hợp thường và trong từng bẫy.
- Lập bảng `size`, `capacity`, số tham chiếu chép thêm qua từng lần lấy ở bẫy 1.
- Với ngưỡng một nửa (thu gọn khi size ≤ capacity / 2), chạy tay bẫy 3 với 8 phần tử trong 8 ô: mỗi lần "thêm một, lấy một" chép bao nhiêu tham chiếu? Tổng sau 1.000 lần? So với ngưỡng một phần tư.
- Giải thích vì sao với ngưỡng một phần tư, sau mỗi lần đổi vùng phải có ít nhất cỡ capacity / 4 thao tác nữa mới đổi vùng lần sau, và từ đó append, pop đều O(1) khấu hao.
- Độ phức tạp: ghi Big-O thời gian (trường hợp xấu nhất và khấu hao) của `append`, `pop`, `get`, và bộ nhớ dự phòng lớn nhất so với số phần tử.

**(2) Triển khai code**

- Viết mã trong `mang_thu_gon.py`; được thêm thuộc tính, hàm phụ; không đổi tên và tham số đã có trong khung; hàm ghi "Có sẵn" giữ nguyên.
- Vùng lưu trữ chỉ được đọc, gán từng ô; chỉ `_resize` tạo vùng mới. Không dùng `append`, `pop`, `insert` trên `_data`.
- Xử lý đủ 5 bẫy; `python mang_thu_gon.py` in đúng kịch bản chạy thử; `pytest -q` xanh cả 7 test có sẵn.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu cách list của CPython mở rộng và thu gọn (tài liệu, mã nguồn `listobject.c` hoặc bài viết giải thích).
- Tạo `nghien_cuu.py`: dùng `sys.getsizeof` để in các mốc list đổi kích thước khi append 1 đến 70 phần tử, rồi khi pop hết. CPython tăng theo hệ số bao nhiêu (gần đúng)? Khi nào list thu gọn? So với quy tắc gấp đôi và ngưỡng một phần tư của bạn.
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session05_Ex17`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-05-mang-va-danh-sach-dong/bai-17 rồi chép các tệp vào kho: `mang_thu_gon.py`, `test_mang_thu_gon.py`, `PHAN_TICH.md`.
3. Viết mã trong `mang_thu_gon.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần nghiên cứu.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
