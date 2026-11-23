# Phân tích và thiết kế: tối ưu báo cáo phương án trả góp

## 1. Input / Output

| Hàm | Đầu vào (kiểu dữ liệu) | Trả về khi hợp lệ | Trả về trong các bẫy |
|---|---|---|---|
| `count_plans` | | | |
| `count_plans_limited` | | | |
| `plan_report` | | | |

## 2. Ba câu hỏi kiểm tra; độ sâu call stack; hàm viết bằng vòng lặp

| Hàm | Cơ sở | Phần ghép | Tiến về cơ sở | Độ sâu lớn nhất |
|---|---|---|---|---|
| | | | | |

## 3. Cây lời gọi count_plans_slow(5); các bài toán con bị tính lặp lại

## 4. Bài toán con của count_plans_limited; số lượng; độ sâu call stack

## 5. Độ phức tạp

| Hàm | Thời gian | Bộ nhớ (kể cả call stack) |
|---|---|---|
| count_plans_slow | | |
| count_plans | | |
| count_plans_limited | | |

## Nghiên cứu mở rộng

cProfile, pstats và cache_info:

| Số đo | Giá trị |
|---|---|
| Số lần gọi count_plans_slow(22) | |
| hits / misses / currsize với 22 | |

Vì sao misses bằng số bài toán con khác nhau; lập luận gửi bộ phận rủi ro:

Nguồn đã đọc:

1.
2.
