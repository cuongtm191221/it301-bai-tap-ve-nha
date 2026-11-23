# Tối ưu báo cáo phương án trả góp "Ví Trả Sau" MoMo

### 1. Bối cảnh & Vấn đề

![Báo cáo phương án trả góp chạy hàng giờ mỗi đêm vì một hàm đệ quy cũ; nhóm cần bản nhanh, đúng và có số đo để chứng minh.](minh_hoa.png)

*Báo cáo phương án trả góp chạy hàng giờ mỗi đêm vì một hàm đệ quy cũ; nhóm cần bản nhanh, đúng và có số đo để chứng minh.*

Tính năng **"Ví Trả Sau"** của MoMo cho khách chia một khoản chi tiêu (tính theo triệu đồng) thành nhiều **kỳ trả**, mỗi kỳ trả **1, 2 hoặc 3 triệu**. Hai phương án khác nhau nếu dãy số tiền các kỳ khác nhau, kể cả chỉ khác thứ tự (1 + 2 khác 2 + 1). Mỗi đêm, hệ thống in **báo cáo phương án** cho danh sách khoản vay để bộ phận rủi ro theo dõi: tổng số phương án, và số phương án hoàn tất trong **không quá `max_terms` kỳ**.

Hàm cũ `count_plans_slow(amount)` (có sẵn trong tệp, không được sửa) viết bằng đệ quy ba nhánh, đúng nhưng rất chậm: khoản 22 triệu đã cần hơn một triệu lời gọi, khoản 30 triệu chạy rất lâu, khoản lớn hơn thì không bao giờ xong. Bộ phận rủi ro muốn báo cáo được các khoản tới **3.000 triệu**.

Bài này tổng hợp kiến thức cả buổi: viết đệ quy đúng, nhận ra bài toán con lặp lại, ghi nhớ kết quả, chuyển sang vòng lặp khi độ sâu vượt giới hạn, và dùng số đo để chứng minh.

### 2. Yêu cầu nghiệp vụ

Bạn viết ba hàm trong `tra_gop.py`.

**2.1. `count_plans(amount)`**: cùng kết quả với `count_plans_slow`, khoản tới 3.000 triệu trong 2 giây, không gọi lại `count_plans_slow`.

**2.2. `count_plans_limited(amount, max_terms)`**: số phương án trả hết `amount` triệu trong không quá `max_terms` kỳ. Khoản 200 triệu, tối đa 120 kỳ phải có kết quả trong 2 giây.

**2.3. `plan_report(amounts, max_terms)`**: list dòng báo cáo, mỗi khoản một dòng:

```plaintext
Khoản 5 triệu: 13 cách trả, 8 cách trong tối đa 3 kỳ.
Khoản 0 triệu: số tiền không hợp lệ.
Khoản 4 triệu: số kỳ tối đa không hợp lệ.
```

### 3. Edge Cases (Bẫy dữ liệu)

**Bẫy 1 — Khớp bản cũ.** Với mọi khoản từ 0 đến 15 triệu, `count_plans` cho đúng kết quả của `count_plans_slow`; khoản âm là 0 phương án.

**Bẫy 2 — Khoản rất lớn.** 3.000 triệu cho một số có 794 chữ số; không được báo `RecursionError`.

**Bẫy 3 — Không đủ kỳ.** 10 triệu trong tối đa 3 kỳ: 0 phương án (3 kỳ chỉ trả được tối đa 9 triệu). Khoản 0 với 0 kỳ: 1 phương án.

**Bẫy 4 — Dữ liệu sai trong báo cáo.** Khoản từ 0 trở xuống: "số tiền không hợp lệ."; `max_terms` từ 0 trở xuống: "số kỳ tối đa không hợp lệ."

**Bẫy 5 — Giới hạn kỳ bằng số tiền.** `count_plans_limited(5, 5)` phải bằng `count_plans(5)`, vì không phương án nào cần quá 5 kỳ.

**Kịch bản chạy thử.** Chạy `python tra_gop.py` (đoạn chạy thử có sẵn ở cuối tệp) phải in ra đúng:

```plaintext
Khoản 1 triệu: 1 cách trả, 1 cách trong tối đa 3 kỳ.
Khoản 3 triệu: 4 cách trả, 4 cách trong tối đa 3 kỳ.
Khoản 5 triệu: 13 cách trả, 8 cách trong tối đa 3 kỳ.
Khoản 10 triệu: 274 cách trả, 0 cách trong tối đa 3 kỳ.
Khoản 0 triệu: số tiền không hợp lệ.
Khoản -2 triệu: số tiền không hợp lệ.
Khoản 4 triệu: số kỳ tối đa không hợp lệ.
Khoản 30 triệu: 53798080 cách
Khoản 3.000 triệu có 794 chữ số
```

### 4. Yêu cầu

Bạn phụ trách trọn tính năng và phải thực hiện đủ ba phần:

**(1) Phân tích và thiết kế (viết vào `PHAN_TICH.md`)**

- Input/Output của từng hàm, trong trường hợp thường và trong từng bẫy.
- Với mỗi hàm đệ quy: ba câu hỏi kiểm tra (Lesson 01) và độ sâu call stack lớn nhất trong bối cảnh của bài. Với mỗi hàm bạn chọn viết bằng vòng lặp: vì sao không dùng đệ quy.
- Vẽ cây lời gọi của `count_plans_slow(5)` tới hết, đánh dấu các bài toán con bị tính lặp lại. Có bao nhiêu lời gọi?
- `count_plans_limited` cần nhớ những gì về bài toán con (bao nhiêu tham số)? Có tối đa bao nhiêu bài toán con khác nhau với khoản 200 triệu, 120 kỳ? Độ sâu call stack lớn nhất là bao nhiêu?
- Độ phức tạp: ghi Big-O thời gian và bộ nhớ của `count_plans_slow`, `count_plans`, `count_plans_limited` theo n (số triệu) và t (số kỳ tối đa).

**(2) Triển khai code**

- Viết mã trong `tra_gop.py`; được thêm hàm phụ; không đổi tên và tham số đã có trong khung; hàm ghi "Có sẵn" giữ nguyên.
- `count_plans` không được gọi `count_plans_slow`. Không dùng `set`, `dict` (sẽ học ở buổi bảng băm); được dùng `functools.lru_cache`.
- Xử lý đủ 5 bẫy; `python tra_gop.py` in đúng kịch bản chạy thử; `python kiem_tra.py` đạt cả 5 mục.

**(3) Nghiên cứu mở rộng (viết vào mục cuối của `PHAN_TICH.md`)**

- Tìm hiểu module `cProfile` (và `pstats`) để đo số lần gọi từng hàm, và phương thức `cache_info()` của hàm có `lru_cache` (ý nghĩa `hits`, `misses`, `currsize`).
- Tạo `nghien_cuu.py`: chạy `cProfile` trên `count_plans_slow(22)` và ghi số lần gọi; viết một bản đệ quy có `lru_cache` của cùng bài toán, gọi với 22 rồi in `cache_info()`. Giải thích vì sao `misses` bằng đúng số bài toán con khác nhau và dùng các số đo này để chứng minh với bộ phận rủi ro rằng bản mới nhanh hơn.
- Được tra cứu tài liệu và hỏi AI để tìm hiểu; phải ghi nguồn và viết lại bằng lời của bạn.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex20`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-20 rồi chép các tệp vào kho: `tra_gop.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Viết mã trong `tra_gop.py`, điền phần phân tích và phần nghiên cứu mở rộng vào `PHAN_TICH.md`. Tạo thêm `nghien_cuu.py` cho phần nghiên cứu.
4. Mức AI của bài: AI-0 cho phần phân tích và mã chính (tự làm, không dùng AI); AI-1 cho phần nghiên cứu mở rộng (được hỏi AI để tìm hiểu, phải ghi nguồn và tự kiểm chứng).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
