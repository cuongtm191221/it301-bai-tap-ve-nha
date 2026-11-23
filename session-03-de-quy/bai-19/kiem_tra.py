"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Mỗi mục in ĐẠT, CHƯA ĐẠT (kèm lý do), CHƯA LÀM hoặc LỖI. Không sửa tệp này.
"""
import threading as _threading


def run_limited(task, seconds, message):
    """Chạy task tối đa seconds giây; quá giờ thì mục kiểm tra CHƯA ĐẠT với lời nhắn message."""
    box, errors = [], []

    def target():
        try:
            box.append(task())
        except BaseException as error:
            errors.append(error)

    worker = _threading.Thread(target=target, daemon=True)
    worker.start()
    worker.join(seconds)
    if errors:
        raise errors[0]
    assert box, message
    return box


_threading.stack_size(64 * 1024 * 1024)   # luồng kiểm tra cần đủ chỗ cho đệ quy sâu


from danh_muc import category_total, report_lines, find_path, category_report

JUNE = ("Tháng 6", [
    ("Ăn uống", [120000, ("Cà phê", [45000, 30000, -30000]), 85000]),
    ("Di chuyển", [("Xe ôm", [25000, 40000]), ("Xăng", [100000])]),
    ("Hóa đơn", [350000, 220000]),
    ("Giải trí", []),
])


def check_total():
    assert category_total(JUNE) == 985000, category_total(JUNE)
    assert category_total(("Giải trí", [])) == 0
    assert category_total(("Cà phê", [45000, 30000, -30000])) == 45000, "hoàn tiền phải được trừ"


def check_lines():
    lines = report_lines(JUNE)
    assert lines[0] == "Tháng 6: 985.000đ" and lines[1] == "  Ăn uống: 250.000đ" and lines[2] == "    Cà phê: 45.000đ", lines[:3]
    assert len(lines) == 8 and lines[-1] == "  Giải trí: 0đ", lines


def check_path():
    assert find_path(JUNE, " xe  ÔM ") == "Tháng 6 > Di chuyển > Xe ôm"
    assert find_path(JUNE, "tháng 6") == "Tháng 6"
    assert find_path(JUNE, "Du lịch") is None


def check_duplicate_names():
    data = ("Gốc", [("A", [("Phí", [1000])]), ("Phí", [2000])])
    assert find_path(data, "phí") == "Gốc > A > Phí", "lấy danh mục đầu tiên theo thứ tự báo cáo"


def check_deep():
    node = ("Cấp 300", [1000])
    for level in range(299, 0, -1):
        node = (f"Cấp {level}", [node, 1000])
    assert category_total(node) == 300000
    assert find_path(node, "cấp 300").count(" > ") == 299
    assert len(report_lines(node)) == 300


def check_report():
    assert category_report(("Gốc", [1500, ("Con", [-500])])) == "Gốc: 1.000đ\n  Con: -500đ"


CHECKS = [
    ("tổng theo danh mục", check_total),
    ("dòng báo cáo và thụt lề", check_lines),
    ("tìm đường dẫn", check_path),
    ("tên danh mục trùng", check_duplicate_names),
    ("cây sâu 300 cấp", check_deep),
    ("báo cáo nhiều dòng, số âm", check_report),
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
