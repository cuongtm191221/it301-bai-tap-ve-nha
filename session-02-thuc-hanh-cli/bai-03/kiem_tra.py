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


from check_in import make_passengers, normalize_code, parse_count, first_k, last_k, find_linear, find_early_stop, check_in, baggage_stats


def raises(message, task):
    try:
        task()
    except ValueError as error:
        assert str(error) == message, f'báo "{error}", cần "{message}"'
        return
    raise AssertionError(f'phải báo lỗi "{message}"')


def codes(ps):
    return [p[0] for p in ps]


def check_normalize():
    assert normalize_code(" dn452 ") == "DN452", "normalize_code(\" dn452 \") phải ra DN452"
    for bad in ["A1234", "ABC12", "AB12", "AB1234", ""]:
        raises("Mã đặt chỗ phải gồm 2 chữ cái và 3 chữ số", lambda: normalize_code(bad))
    assert parse_count(" 3 ") == 3
    for bad in ["0", "-1", "2.5", "ba", ""]:
        raises("Số hành khách phải là số nguyên dương", lambda: parse_count(bad))


def check_slices():
    ps = make_passengers()
    assert codes(first_k(ps, 2)) == ["AB123", "BK207"], "2 người đầu sai"
    assert codes(last_k(ps, 2)) == ["HV518", "QT609"], "2 người cuối sai"
    assert len(first_k(ps, 10)) == 6 and len(last_k(ps, 10)) == 6, "k lớn hơn số người phải trả tất cả"
    assert ps == make_passengers(), "xem danh sách làm đổi dữ liệu"


def check_find():
    ps = make_passengers()
    got = [(p[0] if p else None, s) for p, s in (find_linear(ps, c) for c in ["DN452", "CA000", "ZZ999"])]
    assert got == [("DN452", 4), (None, 6), (None, 6)], f"tìm tuần tự ra {got}"
    got = [(p[0] if p else None, s) for p, s in (find_early_stop(ps, c) for c in ["DN452", "CA000", "AA000", "ZZ999"])]
    assert got == [("DN452", 4), (None, 3), (None, 1), (None, 6)], f"tìm có dừng sớm ra {got}"


def check_checkin():
    ps = make_passengers()
    assert check_in(ps, " cm211", "Bùi Ngọc Lan", "18") == 4, "CM211 phải vào vị trí 4"
    assert check_in(ps, "AA001", "Hồ An", "0") == 1 and check_in(ps, "ZZ999", "Hồ Vy", "40") == 9, "chèn đầu và cuối sai"
    assert codes(ps) == sorted(codes(ps)) and len(ps) == 9, f"danh sách không còn tăng dần: {codes(ps)}"


def check_checkin_invalid():
    cases = [(("ab123", "Lý Hải", "10"), "Mã đặt chỗ AB123 đã check-in"), (("A1234", "Lý Hải", "10"), "Mã đặt chỗ phải gồm 2 chữ cái và 3 chữ số"),
             (("XY999", "  ", "10"), "Họ tên không được để trống"), (("XY999", "Lý Hải", "41"), "Hành lý phải là số nguyên từ 0 đến 40 kg"),
             (("XY999", "Lý Hải", "-1"), "Hành lý phải là số nguyên từ 0 đến 40 kg"), (("XY999", "Lý Hải", "7.5"), "Hành lý phải là số nguyên từ 0 đến 40 kg")]
    for args, message in cases:
        ps = make_passengers()
        raises(message, lambda: check_in(ps, *args))
        assert ps == make_passengers(), f"{args}: danh sách bị thay đổi dù dữ liệu sai"


def check_stats():
    assert baggage_stats(make_passengers()) == (97, 2), f"thống kê mẫu ra {baggage_stats(make_passengers())}"
    assert baggage_stats([]) == (0, 0)


def check_large():
    ps = [[f"{chr(65 + k // 26 % 26)}{chr(65 + k % 26)}{k % 1000:03d}", "Khách", 10] for k in range(600)]
    ps.sort()
    target = ps[300][0]
    got = run_limited(lambda: (find_linear(ps, target)[1], find_early_stop(ps, "ZZ999")[1], find_early_stop(ps, "AB000")[1]), 2, "tra cứu quá 2 giây")
    assert got == (301, 600, 2), f"số bước trên 600 hành khách ra {got}"


def check_cli():
    out = run_cli()
    appear_in_order(out, [
        "3. CK310 | Lê Hoàng Cường | 7 kg", "Tìm tuần tự: DN452 | Phạm Ngọc Dung | 20 kg (so sánh 4 mã).",
        "Tìm có dừng sớm: DN452 | Phạm Ngọc Dung | 20 kg (so sánh 4 mã).", "Tìm có dừng sớm: không có CA000 (so sánh 3 mã).",
        "Tìm tuần tự: không có CA000 (so sánh 6 mã).", "Đã check-in CM211 ở vị trí 4/7.",
        "7. QT609 | Đỗ Quang Tùng | 0 kg", "Lỗi: Mã đặt chỗ AB123 đã check-in", "Lỗi: Mã đặt chỗ phải gồm 2 chữ cái và 3 chữ số",
        "Lỗi: Hành lý phải là số nguyên từ 0 đến 40 kg", "Lỗi: Số hành khách phải là số nguyên dương", "Lựa chọn không hợp lệ.",
        "Tổng hành lý: 115 kg. Vượt 20 kg: 2 hành khách.", "Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 5.",
        "Đóng quầy check-in. Chúc chuyến bay tốt đẹp!",
    ])


CHECKS = [
    ("kiểm tra mã đặt chỗ và số hành khách", check_normalize),
    ("xem k người đầu, k người cuối", check_slices),
    ("tìm tuần tự và tìm có dừng sớm, số lần so sánh", check_find),
    ("check-in giữ danh sách tăng dần", check_checkin),
    ("check-in sai dữ liệu: đúng thông báo, danh sách giữ nguyên", check_checkin_invalid),
    ("thống kê hành lý", check_stats),
    ("số bước trên 600 hành khách", check_large),
    ("chạy thử main.py với các thao tác mẫu", check_cli),
]


# Các phím mục cuối tự gõ vào main.py, theo thứ tự (chuỗi rỗng là bấm Enter không nhập gì).
KEYS = [
    '1',
    '2',
    '3',
    '3',
    '1',
    'DN452',
    '3',
    '2',
    'DN452',
    '3',
    '2',
    'CA000',
    '3',
    '1',
    'CA000',
    '2',
    'cm211',
    'Bùi Ngọc Lan',
    '18',
    '1',
    '2',
    '10',
    '2',
    'ab123',
    'Lý Hải',
    '10',
    '2',
    'A1234',
    'Lý Hải',
    '10',
    '2',
    'XY999',
    'Lý Hải',
    '41',
    '1',
    '2',
    '0',
    '3',
    '5',
    '4',
    '9',
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
