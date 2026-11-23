"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
import inspect
from khung_gio import parse_hour, count_by_hour, peak_hour_message

TIMES = ["20:15", " 09:05 ", "20:47", "13:30", "24:10", "21:02", "07:60", "20:59", "9:05", "13:01", "21:40"]


def check_parse():
    got = [parse_hour(t) for t in ("20:15", " 09:05 ", "00:00", "23:59")]
    assert got == [20, 9, 0, 23], f"giờ hợp lệ ra {got}"
    bad = [parse_hour(t) for t in ("24:10", "07:60", "9:05", "ab:cd", "", "12-30", "123:4")]
    assert bad == [None] * 7, f"chuỗi không hợp lệ ra {bad}"


def check_count():
    counts, invalid = count_by_hour(TIMES)
    assert len(counts) == 24, "phải có đúng 24 ô đếm"
    assert (counts[20], counts[13], counts[21], counts[9], invalid) == (3, 2, 2, 1, 3), "số đếm theo giờ hoặc số dòng lỗi chưa đúng"


def check_peak():
    assert peak_hour_message(TIMES) == "Giờ cao điểm: 20:00 - 20:59 (3 đơn). Bỏ qua 3 dòng lỗi.", peak_hour_message(TIMES)


def check_tie_and_padding():
    assert peak_hour_message(["13:10", "08:00", "13:55", "08:30"]) == "Giờ cao điểm: 08:00 - 08:59 (2 đơn). Bỏ qua 0 dòng lỗi.", "bằng nhau phải chọn khung giờ sớm hơn"
    assert peak_hour_message(["00:05", "23:59", "00:40"]) == "Giờ cao điểm: 00:00 - 00:59 (2 đơn). Bỏ qua 0 dòng lỗi.", "giờ 0 phải hiển thị 00:00 - 00:59"


def check_no_valid():
    assert peak_hour_message(["25:00", "ab:cd"]) == "Chưa có đơn hàng hợp lệ. Bỏ qua 2 dòng lỗi."
    assert peak_hour_message([]) == "Chưa có đơn hàng hợp lệ. Bỏ qua 0 dòng lỗi."


def check_space():
    src = inspect.getsource(count_by_hour) + inspect.getsource(peak_hour_message)
    assert "sort" not in src and "append" not in src and "dict(" not in src and "{}" not in src, "không lưu lại từng đơn, chỉ dùng 24 ô đếm"
    times = ["10:00"] * 200000
    assert count_by_hour(times)[0][10] == 200000, "200.000 đơn đếm sai"


CHECKS = [
    ("đọc giờ từ chuỗi HH:MM", check_parse),
    ("đếm đơn theo giờ và số dòng lỗi", check_count),
    ("thông báo giờ cao điểm", check_peak),
    ("bằng nhau chọn giờ sớm hơn; giờ 0 hiển thị 00", check_tie_and_padding),
    ("không có đơn hợp lệ", check_no_valid),
    ("chỉ dùng 24 ô đếm, chạy được 200.000 đơn", check_space),
]


if __name__ == "__main__":
    passed = 0
    for name, check in CHECKS:
        try:
            check()
            print("ĐẠT      |", name)
            passed += 1
        except NotImplementedError:
            print("CHƯA LÀM |", name)
        except AssertionError as error:
            print("CHƯA ĐẠT |", name, "-", error)
        except Exception as error:
            print("LỖI      |", name, "-", type(error).__name__, error)
    print(f"Kết quả: {passed}/{len(CHECKS)} mục đạt")
