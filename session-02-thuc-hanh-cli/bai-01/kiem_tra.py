"""Tự kiểm tra bài làm. Chạy trong thư mục của bài: python kiem_tra.py

Các mục đầu kiểm tra hàm nghiệp vụ; mục cuối chạy main.py, tự gõ lần lượt các phím trong KEYS
(cuối tệp) và kiểm tra các dòng thông báo bắt buộc xuất hiện đúng thứ tự. Không sửa tệp này.
"""
import os as _os
import subprocess as _sp
import sys as _sys
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
    return box[0]


def run_cli(seconds=10):
    """Chạy python main.py, tự gõ các phím trong KEYS (mỗi dòng một lần Enter); trả về toàn bộ chữ in ra."""
    keys = "\n".join(KEYS) + "\n"
    env = dict(_os.environ, PYTHONIOENCODING="utf-8")
    try:
        r = _sp.run([_sys.executable, "main.py"], input=keys, capture_output=True, text=True,
                    encoding="utf-8", timeout=seconds, env=env)
    except _sp.TimeoutExpired:
        raise AssertionError("main.py không dừng: kiểm tra chức năng Thoát và vòng lặp menu")
    if "NotImplementedError" in r.stderr:
        raise NotImplementedError
    assert "Traceback" not in r.stderr, "main.py dừng vì lỗi: " + r.stderr.strip().split("\n")[-1]
    return r.stdout


def appear_in_order(out, lines):
    """Mỗi dòng trong lines phải xuất hiện trong out, theo đúng thứ tự."""
    pos = 0
    for line in lines:
        k = out.find(line, pos)
        assert k >= 0, f'không thấy "{line}" (hoặc xuất hiện sai thứ tự)'
        pos = k + len(line)


from don_hang import make_orders, total_cod, find_order, add_order, count_by_district


def check_total():
    got = total_cod(make_orders())
    assert got == (5, 2149000), f"5 đơn mẫu ra {got}"
    assert total_cod([]) == (0, 0), f"danh sách rỗng ra {total_cod([])}"


def check_find():
    orders = make_orders()
    got = [(o[0] if o else None, s) for o, s in (find_order(orders, c) for c in ["GH1001", "GH1005", "GH9999"])]
    assert got == [("GH1001", 1), ("GH1005", 5), (None, 5)], f"tìm mã đầu, cuối, không có ra {got}"


def check_find_normalize():
    order, steps = find_order(make_orders(), "  gh1003 ")
    assert order is not None and order[0] == "GH1003" and steps == 3, f'tìm "  gh1003 " ra {(order, steps)}'


def check_add():
    orders = make_orders()
    order = add_order(orders, " gh1006 ", " Lê Văn Cường ", "Cầu Giấy", "120000")
    assert order == ["GH1006", "Lê Văn Cường", "Cầu Giấy", 120000], f"đơn mới là {order}"
    assert len(orders) == 6 and orders[-1] is order, "đơn mới phải nằm cuối danh sách"


def check_add_invalid():
    cases = [
        (("   ", "An", "Hà Đông", "1000"), "Mã đơn không được để trống"),
        (("gh1001", "An", "Hà Đông", "1000"), "Mã đơn GH1001 đã tồn tại"),
        (("GH1007", "  ", "Hà Đông", "1000"), "Người nhận không được để trống"),
        (("GH1007", "An", "", "1000"), "Quận không được để trống"),
        (("GH1007", "An", "Hà Đông", "-5000"), "Tiền thu hộ phải là số nguyên không âm"),
        (("GH1007", "An", "Hà Đông", "12.5"), "Tiền thu hộ phải là số nguyên không âm"),
        (("GH1007", "An", "Hà Đông", "abc"), "Tiền thu hộ phải là số nguyên không âm"),
    ]
    for args, message in cases:
        orders = make_orders()
        try:
            add_order(orders, *args)
        except ValueError as error:
            assert str(error) == message, f"{args} báo \"{error}\", cần \"{message}\""
        else:
            raise AssertionError(f"{args} phải báo lỗi \"{message}\"")
        assert orders == make_orders(), f"{args}: danh sách bị thay đổi dù dữ liệu sai"


def check_district():
    orders = make_orders()
    got = [count_by_district(orders, d) for d in ["cầu giấy", "  HÀ ĐÔNG ", "Ba Đình"]]
    assert got == [2, 1, 0], f"đếm Cầu Giấy, Hà Đông, Ba Đình ra {got}"


def check_large():
    orders = [[f"GH{k}", "Khách", "Cầu Giấy", 1000] for k in range(100000)]
    got = run_limited(lambda: find_order(orders, "GH99999"), 2, "tra cứu 100.000 đơn quá 2 giây")
    assert got[1] == 100000, f"mã cuối trong 100.000 đơn phải so sánh 100000 lần, ra {got[1]}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "5. GH1005 | Hoàng Văn Em | Thanh Xuân | 460.000đ", "Tổng: 5 đơn, thu hộ 2.149.000đ",
        "Tìm thấy: GH1003 | Lê Minh Châu | Hà Đông | 1.250.000đ (đã so sánh 3 mã).",
        "Không tìm thấy đơn GH9999 (đã so sánh 5 mã).",
        "Đã thêm đơn GH1006. Hiện có 6 đơn.",
        "Lỗi: Mã đơn GH1001 đã tồn tại", "Lỗi: Người nhận không được để trống",
        "Lỗi: Tiền thu hộ phải là số nguyên không âm",
        "Quận cầu giấy có 3 đơn.",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.",
        "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.",
        "Tổng: 6 đơn, thu hộ 2.269.000đ", "Đã lưu ca làm việc. Tạm biệt!",
    ])


CHECKS = [
    ("tổng số đơn và tiền thu hộ", check_total),
    ("tra cứu mã đầu, mã cuối, mã không có và số lần so sánh", check_find),
    ("tra cứu mã viết thường, có khoảng trắng", check_find_normalize),
    ("thêm đơn hợp lệ vào cuối", check_add),
    ("thêm đơn sai dữ liệu: đúng thông báo, danh sách giữ nguyên", check_add_invalid),
    ("đếm đơn theo quận", check_district),
    ("tra cứu trong 100.000 đơn", check_large),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '3',
    '  gh1003 ',
    '3',
    'GH9999',
    '2',
    'GH1006',
    'Lê Văn Cường',
    'Cầu Giấy',
    '120000',
    '2',
    'gh1001',
    'Ngô Thị Giang',
    'Hà Đông',
    '50000',
    '2',
    'GH1007',
    '   ',
    'Hà Đông',
    '50000',
    '2',
    'GH1007',
    'Ngô Thị Giang',
    'Hà Đông',
    '-5000',
    '4',
    '  cầu giấy ',
    'abc',
    '7',
    '',
    '1',
    '5',
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
