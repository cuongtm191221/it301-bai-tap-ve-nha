# Ước lượng thời gian chạy báo cáo đêm của Shopee

### 1. Bối cảnh & Vấn đề

![Nhóm hạ tầng phải biết trước báo cáo nào chạy kịp trong khung 2 giờ sáng, chỉ từ độ phức tạp và số dữ liệu.](minh_hoa.png)

*Nhóm hạ tầng phải biết trước báo cáo nào chạy kịp trong khung 2 giờ sáng, chỉ từ độ phức tạp và số dữ liệu.*

Mỗi đêm từ 0 giờ đến 2 giờ, Shopee chạy hàng trăm báo cáo cho người bán. Trước khi đưa một báo cáo mới vào lịch, nhóm hạ tầng cần biết nó có chạy **kịp trong khung giờ** hay không. Đội phát triển chỉ cung cấp hai thông tin: **độ phức tạp thời gian** (ví dụ `"O(n log n)"`) và **số lượng dữ liệu** n.

Bạn được giao viết công cụ ước lượng trong `uoc_luong.py`, dựa trên bảng các lớp độ phức tạp ở Lesson 02. Số bước ước lượng của mỗi lớp:

| Độ phức tạp | Số bước ước lượng |
|---|---|
| `O(1)` | 1 |
| `O(log n)` | số lần chia đôi n cho đến khi còn 1 (hàm `halvings` có sẵn) |
| `O(n)` | n |
| `O(n log n)` | n × số lần chia đôi n |
| `O(n^2)` | n × n |

Ví dụ với n = 1.000.000: O(log n) khoảng 19 bước, O(n²) tới 10¹² bước.

### 2. Yêu cầu nghiệp vụ

**2.1. Chuẩn hóa cách viết: `normalize(complexity)`**

Đội phát triển viết độ phức tạp không thống nhất. Hàm trả về một trong năm dạng chuẩn của list `SUPPORTED`, hoặc `None` nếu không hỗ trợ.

**2.2. Số bước: `estimate_steps(complexity, n)`**

Trả về số bước theo bảng ở mục 1, **ít nhất là 1**; trả về `None` nếu độ phức tạp không hỗ trợ hoặc n không dương.

**2.3. Tỉ lệ tăng: `growth_ratio(complexity, n1, n2)`**

Trả về số bước với n2 chia cho số bước với n1, làm tròn 1 chữ số thập phân (hàm `round`); `None` nếu một trong hai ước lượng là `None`. Ví dụ `growth_ratio("O(n^2)", 1000, 10000)` là `100.0`.

**2.4. Có kịp không: `fits_window(complexity, n, steps_per_second, seconds)`**

Số bước cho phép = `steps_per_second` × `seconds`. Trả về một trong hai thông báo:

```plaintext
Kịp: cần khoảng 40000000 bước, khung giờ cho phép 72000000000 bước.
Không kịp: cần khoảng 4000000000000 bước, vượt 3928000000000 bước.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Cách viết không thống nhất**

- `" o(log N) "`, `"O( n log n )"`, `"O(n²)"` phải được nhận ra là `"O(log n)"`, `"O(n log n)"`, `"O(n^2)"`: bỏ mọi khoảng trắng, chữ `o` đầu thành `O`, chữ `N` thành `n`, `²` thành `^2`.

**Bẫy 2 — Độ phức tạp không hỗ trợ**

- `"O(n^3)"`, `"O(2^n)"`: `normalize` trả về `None`, `fits_window` trả về (giữ nguyên cách viết, chỉ bỏ khoảng trắng hai đầu):

```plaintext
Không hỗ trợ độ phức tạp O(2^n).
```

**Bẫy 3 — n bằng 1**

- Số lần chia đôi của 1 là 0, nên O(log n) và O(n log n) sẽ ra 0 bước. Báo cáo chạy vẫn tốn ít nhất 1 bước: kết quả phải là 1.

**Bẫy 4 — n không dương**

- `estimate_steps` trả về `None`; `fits_window` trả về:

```plaintext
Số lượng dữ liệu phải lớn hơn 0.
```

**Bẫy 5 — Số rất lớn**

- O(n²) với n = 2.000.000 là 4 × 10¹² bước. Dùng số nguyên của Python để tính chính xác, không dùng `math.log` hay số thực cho số bước.

**Kịch bản chạy thử.** Chạy `python uoc_luong.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
O(1)       n = 1.000.000: 1
O(log n)   n = 1.000.000: 19
O(n)       n = 1.000.000: 1000000
O(n log n) n = 1.000.000: 19000000
O(n^2)     n = 1.000.000: 1000000000000
Tăng khi n từ 1.000 lên 10.000, O(n^2): 100.0
Tăng khi n từ 1.000 lên 10.000, O(log n): 1.4
O(n log n) với n = 1: 1
Kịp: cần khoảng 40000000 bước, khung giờ cho phép 72000000000 bước.
Không kịp: cần khoảng 4000000000000 bước, vượt 3928000000000 bước.
Không hỗ trợ độ phức tạp O(2^n).
Số lượng dữ liệu phải lớn hơn 0.
```

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm, bạn phải thực hiện đầy đủ hai phần sau:

**(1) Phân tích và thiết kế giải pháp (bắt buộc, viết vào `PHAN_TICH.md`)**

- Phân tích Input/Output: với từng hàm, nêu dữ liệu đầu vào (kiểu dữ liệu) và giá trị trả về trong trường hợp thường và trong từng bẫy.
- Thiết kế giải pháp: liệt kê theo thứ tự các bước biến một chuỗi bất kỳ thành dạng chuẩn trong `normalize`; với mỗi cách viết ở bẫy 1, ghi chuỗi sau từng bước.
- Viết mã giả cho `estimate_steps`. Vì sao phải dùng lại `halvings` thay vì tự tính log?
- Từ bảng số bước, giải thích vì sao `growth_ratio` của O(n) luôn bằng n2 / n1, còn của O(log n) thì gần 1.
- Độ phức tạp: ghi Big-O thời gian của `halvings` và của `estimate_steps` theo n. Vì sao công cụ ước lượng O(n²) với n = 2.000.000 vẫn chạy tức thì?

**(2) Triển khai code**

- Viết thân các hàm trong `uoc_luong.py`. Không đổi tên hàm, tham số.
- Không dùng `math.log`; chỉ dùng phép tính số nguyên và hàm `halvings` có sẵn.
- Xử lý đủ 5 bẫy ở mục 3; `python uoc_luong.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 6 mục.
- Mã sạch, dễ đọc, tên biến theo snake_case, có chú thích ở những chỗ quyết định độ phức tạp.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session01_Ex12`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-01-tong-quan-do-phuc-tap/bai-12 rồi chép các tệp vào kho: `uoc_luong.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, viết mã trong `uoc_luong.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
