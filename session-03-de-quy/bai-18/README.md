# Kế hoạch tiết kiệm góp tăng dần cho "Heo đất" MoMo

### 1. Bối cảnh & Vấn đề

![Người dùng muốn góp ít lúc đầu rồi tăng dần mỗi tháng; ứng dụng phải lập lịch từng tháng và biết dừng khi kế hoạch không khả thi.](minh_hoa.png)

*Người dùng muốn góp ít lúc đầu rồi tăng dần mỗi tháng; ứng dụng phải lập lịch từng tháng và biết dừng khi kế hoạch không khả thi.*

Tính năng **"Heo đất"** của ví MoMo nâng cấp: người dùng không phải góp đều nữa mà chọn **mức góp tháng đầu** và **mức tăng mỗi tháng**. Ví dụ góp 500.000đ tháng đầu, mỗi tháng tăng 100.000đ: tháng 2 góp 600.000đ, tháng 3 góp 700.000đ... Ứng dụng hiện **lịch số dư từng tháng** và câu tóm tắt "Cần N tháng".

Quy tắc của nhóm sản phẩm:

- Mức góp tháng thứ k = mức góp tháng đầu + (k - 1) × mức tăng. Mức tăng có thể là 0 (góp đều).
- Tháng nào mức góp **không dương** (người dùng chọn mức đầu âm để "nghỉ góp" vài tháng) thì tháng đó không góp, số dư giữ nguyên, nhưng vẫn tính là một tháng.
- Dừng ở tháng đầu tiên số dư **bằng hoặc vượt** mục tiêu.
- Kế hoạch không đạt trong **600 tháng** (50 năm) được coi là không khả thi.

Bài này tổng hợp kiến thức cả buổi: chọn trường hợp cơ sở, bảo đảm mỗi lời gọi tiến về cơ sở, tránh lỗi quên `return`, và chọn đệ quy hay vòng lặp dựa trên độ sâu tối đa. Hàm `money(amount)` (có sẵn) in số tiền có dấu chấm.

### 2. Yêu cầu nghiệp vụ

Bạn viết ba hàm trong `ke_hoach.py`.

**2.1. `savings_schedule(balance, goal, monthly, step)`**: list các bộ `(tháng, số dư cuối tháng)` từ tháng 1 tới tháng đạt mục tiêu; đã đủ từ đầu thì `[]`; không đạt trong 600 tháng thì `None`.

**2.2. `months_needed(balance, goal, monthly, step)`**: số tháng cần góp; đã đủ thì 0; không khả thi thì `None`.

**2.3. `plan_message(balance, goal, monthly, step)`**: một trong bốn thông báo:

```plaintext
Cần 5 tháng, tháng cuối góp 800.000đ, số dư 5.000.000đ.
Đã đủ mục tiêu.
Không đạt mục tiêu trong 600 tháng, hãy tăng mức góp.
Dữ liệu không hợp lệ.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Đã đủ từ đầu.** Số dư bằng hoặc vượt mục tiêu: lịch rỗng, 0 tháng, "Đã đủ mục tiêu."

**Bẫy 2 — Tháng nghỉ góp.** Số dư 0, mục tiêu 3.000.000đ, góp -200.000đ tăng 100.000đ: ba tháng đầu không góp, cần 11 tháng.

**Bẫy 3 — Không bao giờ đạt.** Góp 0đ, tăng 0đ: không được chạy mãi, kết quả là không khả thi.

**Bẫy 4 — Đúng 600 tháng và trên 600 tháng.** Góp đều 100.000đ, mục tiêu 60 triệu: đúng 600 tháng, vẫn đạt; mục tiêu 500 triệu: không khả thi. Mục tiêu 1.000 tỷ góp 1.000đ cũng phải trả lời trong 2 giây.

**Bẫy 5 — Dữ liệu sai.** Mục tiêu từ 0 trở xuống hoặc số dư âm: "Dữ liệu không hợp lệ."

**Kịch bản chạy thử.** Chạy `python ke_hoach.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Cần 5 tháng, tháng cuối góp 800.000đ, số dư 5.000.000đ.
Cần 11 tháng, tháng cuối góp 1.500.000đ, số dư 11.000.000đ.
[(1, 500000), (2, 1100000), (3, 1800000), (4, 2600000)]
Đã đủ mục tiêu.
Cần 11 tháng, tháng cuối góp 800.000đ, số dư 3.600.000đ.
Không đạt mục tiêu trong 600 tháng, hãy tăng mức góp.
Không đạt mục tiêu trong 600 tháng, hãy tăng mức góp.
Dữ liệu không hợp lệ.
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, trong trường hợp thường và trong từng bẫy.
- Với mỗi hàm đệ quy: ba câu hỏi kiểm tra (Lesson 01) và độ sâu call stack lớn nhất trong bối cảnh của bài. Với mỗi hàm bạn chọn viết bằng vòng lặp: vì sao không dùng đệ quy.
- Nếu viết `savings_schedule` bằng đệ quy theo tháng: liệt kê các trường hợp cơ sở, chỉ ra tham số nào tiến về cơ sở ở mỗi lời gọi, và độ sâu call stack lớn nhất. Giới hạn 600 tháng ảnh hưởng thế nào tới lựa chọn đệ quy hay vòng lặp?
- Chạy tay bẫy 2 bốn tháng đầu: mức góp, có góp hay không, số dư.
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ (kể cả call stack nếu dùng đệ quy) của ba hàm theo m (số tháng, tối đa 600).

**(2) Triển khai code**

- Viết mã trong `ke_hoach.py`; được thêm hàm phụ; không đổi tên và tham số đã có trong khung; hàm ghi "Có sẵn" giữ nguyên.
- Được chọn đệ quy hoặc vòng lặp cho từng hàm, nhưng phải giải thích lựa chọn ở phần (1). Dùng lại `savings_schedule` trong hai hàm sau, không viết lặp lại phần tính lịch.
- Xử lý đủ 5 bẫy; `python ke_hoach.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 5 mục.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu `sys.getrecursionlimit()` và `sys.setrecursionlimit()`: giới hạn này bảo vệ chương trình khỏi điều gì; tăng giới hạn quá cao có thể gây hậu quả gì mà `RecursionError` không báo trước.
- Tạo `nghien_cuu.py`: tìm độ sâu đệ quy lớn nhất chạy được với giới hạn mặc định, rồi với giới hạn 5.000; ghi phiên bản Python. Nếu sau này nhóm nâng giới hạn kế hoạch lên 5.000 tháng, bạn đề xuất sửa `savings_schedule` thế nào?
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex18`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-18 rồi chép các tệp vào kho: `ke_hoach.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Viết mã trong `ke_hoach.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần nghiên cứu.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
