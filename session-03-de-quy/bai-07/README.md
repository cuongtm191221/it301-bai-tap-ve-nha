# Lỗi tính số dư tiết kiệm online tự tái tục trên ví MoMo

### 1. Bối cảnh nghiệp vụ

![Số dư dự kiến sau 3 năm thấp hơn ngân hàng tính, lịch sử số dư báo lỗi, gửi rồi rút ngay thì ứng dụng sập.](minh_hoa.png)

*Số dư dự kiến sau 3 năm thấp hơn ngân hàng tính, lịch sử số dư báo lỗi, gửi rồi rút ngay thì ứng dụng sập.*

Bạn là kỹ sư phần mềm trong nhóm tính năng "Tiết kiệm online" của ví MoMo, liên kết với ngân hàng đối tác.

Người dùng gửi một khoản tiền, kỳ hạn 1 năm, **tự tái tục**: hết mỗi năm, lãi được cộng vào số dư và cả số dư mới tiếp tục gửi năm sau (lãi kép). Quy định của ngân hàng:

- Lãi của một năm = **số dư đầu năm** × lãi suất (%) // 100, **làm tròn xuống tới đồng ngay trong năm đó**, rồi cộng vào số dư.
- Sau **0 năm** (rút ngay trong năm đầu, không hưởng lãi), số dư bằng số tiền gửi.

Ví dụ gửi 10.000.000đ, lãi 6%/năm: hết năm 1 được 10.600.000đ; năm 2 lãi tính trên 10.600.000đ nên được 11.236.000đ.

Nhóm viết hai hàm bằng đệ quy:

- `balance_after(principal, rate, years)`: số dư sau `years` năm. Số dư sau n năm tính từ số dư sau n - 1 năm.
- `history(principal, rate, years)`: list số dư từ năm 0 đến năm `years`, để vẽ biểu đồ tăng trưởng. Lịch sử n năm là lịch sử n - 1 năm thêm một phần tử ở cuối.

Kịch bản kiểm tra (đoạn cuối tệp): số dư sau 1 năm, sau 3 năm, lịch sử 3 năm, rồi số dư sau 0 năm.

Kết quả đúng cần hiển thị:

```plaintext
Gửi 10.000.000đ, lãi 6%/năm, sau 1 năm: 10600000
Gửi 10.000.000đ, lãi 6%/năm, sau 3 năm: 11910160
Lịch sử 3 năm: [10000000, 10600000, 11236000, 11910160]
Rút ngay trong năm đầu (0 năm): 10000000
```

### 2. Vấn đề hiện tại

Người dùng và ngân hàng đối tác phản ánh:

- Số dư dự kiến sau 1 năm khớp với ngân hàng, nhưng sau 3 năm ứng dụng hiện **11.800.000đ**, thấp hơn số ngân hàng tính.
- Mở biểu đồ tăng trưởng thì ứng dụng báo lỗi.
- Người dùng chọn rút ngay trong năm đầu thì ứng dụng báo `RecursionError`.

Nhắc lại kiến thức (Lesson 01, Lesson 03):

- Mỗi hàm đệ quy phải trả lời đúng **ba câu hỏi** (Lesson 01): (1) trường hợp cơ sở trả đúng chưa; (2) từ kết quả của bài toán nhỏ hơn, phần ghép ra kết quả lớn đúng chưa; (3) mỗi lần gọi có tiến về trường hợp cơ sở không.
- Cơ sở phải là **đầu vào hợp lệ nhỏ nhất**. Nếu đầu vào nhỏ nhất bị bỏ sót, lời gọi với đầu vào đó đi mãi về phía số âm cho tới khi gặp `RecursionError`.
- Phần ghép phải trả về **giá trị**. Lưu ý: `list.append(x)` sửa list tại chỗ và trả về `None`; viết `return lst.append(x)` là trả về `None` cho tầng trên.

### 3. Mã nguồn hiện tại (Legacy Code)

Toàn bộ tệp `tiet_kiem_online.py` trong thư mục khởi đầu (đoạn cuối tệp là kịch bản chạy thử):

```python
def balance_after(principal, rate, years):
    # Số dư sau years năm. Mỗi năm: lãi = số dư đầu năm * rate // 100, cộng vào số dư.
    if years == 1:
        return principal + principal * rate // 100
    return balance_after(principal, rate, years - 1) + principal * rate // 100


def history(principal, rate, years):
    # List số dư cuối mỗi năm, từ năm 0 (số tiền gửi ban đầu) đến năm years.
    if years == 0:
        return [principal]
    return history(principal, rate, years - 1).append(balance_after(principal, rate, years))


print("Gửi 10.000.000đ, lãi 6%/năm, sau 1 năm:", balance_after(10000000, 6, 1))
print("Gửi 10.000.000đ, lãi 6%/năm, sau 3 năm:", balance_after(10000000, 6, 3))
print("Lịch sử 3 năm:", history(10000000, 6, 3))
print("Rút ngay trong năm đầu (0 năm):", balance_after(10000000, 6, 0))
```

Kết quả hiển thị trên Console:

```plaintext
Gửi 10.000.000đ, lãi 6%/năm, sau 1 năm: 10600000
Gửi 10.000.000đ, lãi 6%/năm, sau 3 năm: 11800000
Traceback (most recent call last):
  ...
    return history(principal, rate, years - 1).append(balance_after(principal, rate, years))
AttributeError: 'NoneType' object has no attribute 'append'
```

Đối chiếu với kết quả đúng: 1 năm đúng; 3 năm thiếu 110.160đ; lịch sử 3 năm gây lỗi `AttributeError`, nên dòng 0 năm không được chạy tới (chạy riêng thì gặp `RecursionError`).

### 4. Yêu cầu

Với vai trò kỹ sư phần mềm của nhóm, hãy thực hiện:

**(1) Phân tích lỗi** (trả lời vào `PHAN_TICH.md`)

- Chạy tay `balance_after(10000000, 6, 3)` của mã hiện tại: ghi giá trị trả về ở mỗi tầng. Lãi mỗi năm đang được tính trên số tiền nào? Vì sao năm 1 vẫn đúng?
- Viết lại phần ghép của `balance_after` theo đúng quy định lãi kép. Kiểm tra lại với 3 năm.
- Với `years = 0`, lời gọi tiếp theo của mã hiện tại là gì? Sửa trường hợp cơ sở thế nào?
- Chạy tay `history(10000000, 6, 2)` của mã hiện tại: tầng nào trả về `None`, vì sao? Tầng nào gây `AttributeError`?
- Sửa `history` để trả về list đúng. Bản sửa của bạn có gọi lại `balance_after` ở mỗi tầng không? Nếu có, với `years = n` tổng số lời gọi là bao nhiêu; có cách nào chỉ cần n lời gọi?
- Vì sao phải làm tròn xuống từng năm thay vì tính một lần ở cuối? Tìm một bộ (số tiền, lãi suất, số năm) mà hai cách cho kết quả khác nhau.

**(2) Sửa lỗi**

- Sửa hai hàm trong `tiet_kiem_online.py`, giữ cách viết đệ quy. Không đổi tên hàm, tham số; chỉ dùng số nguyên (không dùng số thực).
- Chạy `python tiet_kiem_online.py` phải in đúng phần "Kết quả đúng cần hiển thị" ở mục 1.
- Chạy `python kiem_tra.py` phải đạt cả 5 mục.

### 5. Quy định nộp bài

1. Tạo một kho GitHub riêng cho bài này, đặt tên theo mẫu `[Tên Lớp]_IT301_Session03_Ex07`.
2. Tải thư mục khởi đầu tại https://github.com/cuongtm191221/it301-bai-tap-ve-nha/tree/main/session-03-de-quy/bai-07 rồi chép các tệp vào kho: `tiet_kiem_online.py`, `kiem_tra.py`, `PHAN_TICH.md`.
3. Điền phần phân tích vào `PHAN_TICH.md`, sửa mã trong `tiet_kiem_online.py`.
4. Mức AI của bài: AI-0 (tự làm, không dùng AI).
5. Đưa bài làm lên kho và nộp đường dẫn kho lên hệ thống.
